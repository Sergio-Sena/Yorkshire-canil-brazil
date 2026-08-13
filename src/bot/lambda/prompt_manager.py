"""
prompt_manager.py — CRUD do system prompt via S3 (com fallback SSM)
Endpoints:
  GET  /prompt           → retorna prompt ativo + metadados + versões disponíveis
  PUT  /prompt           → valida + salva no S3 (versionamento automático)
  POST /prompt/rollback  → restaura versão anterior via S3 Versioning

Estratégia de migração sem downtime:
  - Leitura: tenta S3 primeiro → fallback para SSM se S3 falhar ou estiver vazio
  - Escrita: salva no S3 (SSM não é mais atualizado)
  - Após validação em produção: remover fallback SSM
"""

import json
import logging
import os
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from zoneinfo import ZoneInfo
from config import AWS_REGION, FOLLOWUP_TIMEZONE

logger = logging.getLogger()
logger.setLevel(logging.INFO)

_s3  = boto3.client("s3",  region_name=AWS_REGION)
_ssm = boto3.client("ssm", region_name=AWS_REGION)
TZ   = ZoneInfo(FOLLOWUP_TIMEZONE)

# ── Configuração S3 ───────────────────────────────────────────────────────────
PROMPT_BUCKET     = os.environ.get("PROMPT_BUCKET", "")
PROMPT_KEY_ACTIVE = os.environ.get("PROMPT_KEY_ACTIVE", "active/prompt.txt")
PROMPT_KEY_BACKUP = os.environ.get("PROMPT_KEY_BACKUP", "backup/prompt.txt")

# ── Fallback SSM (remover após validação em produção) ─────────────────────────
PARAM_ACTIVE = "/yorkshire-bot/prompt/active"
PARAM_BACKUP = "/yorkshire-bot/prompt/backup"
PARAM_META   = "/yorkshire-bot/prompt/meta"

_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json"
}

# ── Validação ─────────────────────────────────────────────────────────────────

REQUIRED_ACTIONS  = ["reply", "transfer", "close", "archive", "send_media"]
REQUIRED_SECTIONS = [
    "IDENTIDADE E COMPORTAMENTO",
    "SEGURANÇA E LIMITES",
    "FORMATO DE RESPOSTA",
]
MIN_LENGTH = 500
MAX_LENGTH = 50_000  # S3 não tem limite prático — aumentado de 15k para 50k


def validate_prompt(prompt: str) -> list:
    errors = []
    if len(prompt) < MIN_LENGTH:
        errors.append(f"Prompt muito curto ({len(prompt)} chars). Mínimo: {MIN_LENGTH}.")
    if len(prompt) > MAX_LENGTH:
        errors.append(f"Prompt muito longo ({len(prompt)} chars). Máximo: {MAX_LENGTH}.")
    for action in REQUIRED_ACTIONS:
        if action not in prompt:
            errors.append(f"Action obrigatória ausente: {action}")
    for section in REQUIRED_SECTIONS:
        if section not in prompt:
            errors.append(f"Seção obrigatória ausente: {section}")
    return errors


# ── S3 helpers ────────────────────────────────────────────────────────────────

def _s3_get(key: str) -> str | None:
    """Lê objeto do S3. Retorna None se não existir ou bucket não configurado."""
    if not PROMPT_BUCKET:
        return None
    try:
        resp = _s3.get_object(Bucket=PROMPT_BUCKET, Key=key)
        return resp["Body"].read().decode("utf-8")
    except ClientError as e:
        if e.response["Error"]["Code"] in ("NoSuchKey", "NoSuchBucket"):
            return None
        logger.error(f"S3 get_object erro: {e}")
        return None


def _s3_put(key: str, value: str, metadata: dict = None) -> str | None:
    """Salva objeto no S3. Retorna VersionId criado ou None em caso de erro."""
    if not PROMPT_BUCKET:
        logger.error("PROMPT_BUCKET não configurado — não foi possível salvar no S3")
        return None
    try:
        kwargs = {
            "Bucket":      PROMPT_BUCKET,
            "Key":         key,
            "Body":        value.encode("utf-8"),
            "ContentType": "text/plain; charset=utf-8",
        }
        if metadata:
            kwargs["Metadata"] = {k: str(v) for k, v in metadata.items()}
        resp = _s3.put_object(**kwargs)
        return resp.get("VersionId")
    except ClientError as e:
        logger.error(f"S3 put_object erro: {e}")
        return None


def _s3_list_versions(key: str, max_versions: int = 10) -> list:
    """Lista versões anteriores de um objeto S3 (exclui a versão atual)."""
    if not PROMPT_BUCKET:
        return []
    try:
        resp = _s3.list_object_versions(Bucket=PROMPT_BUCKET, Prefix=key)
        versions = resp.get("Versions", [])
        # Ordena por data desc, pula a mais recente (índice 0 = atual)
        versions.sort(key=lambda v: v["LastModified"], reverse=True)
        return versions[1:max_versions + 1]
    except ClientError as e:
        logger.error(f"S3 list_object_versions erro: {e}")
        return []


def _s3_get_version(key: str, version_id: str) -> str | None:
    """Lê uma versão específica de um objeto S3."""
    if not PROMPT_BUCKET:
        return None
    try:
        resp = _s3.get_object(Bucket=PROMPT_BUCKET, Key=key, VersionId=version_id)
        return resp["Body"].read().decode("utf-8")
    except ClientError as e:
        logger.error(f"S3 get_object version erro: {e}")
        return None


# ── SSM helpers (fallback — remover após validação) ───────────────────────────

def _ssm_get(name: str) -> str | None:
    try:
        resp = _ssm.get_parameter(Name=name, WithDecryption=False)
        return resp["Parameter"]["Value"]
    except ClientError as e:
        if e.response["Error"]["Code"] == "ParameterNotFound":
            return None
        logger.warning(f"SSM get_parameter erro: {e}")
        return None


def _get_meta() -> dict:
    raw = _ssm_get(PARAM_META)
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except Exception:
        return {}


def _save_meta(meta: dict) -> None:
    try:
        _ssm.put_parameter(
            Name=PARAM_META, Value=json.dumps(meta),
            Type="String", Overwrite=True
        )
    except Exception as e:
        logger.warning(f"SSM save_meta erro (não crítico): {e}")


def _now() -> str:
    return datetime.now(TZ).isoformat()


# ── Leitura com fallback ──────────────────────────────────────────────────────

def _read_active_prompt() -> tuple[str | None, str]:
    """
    Lê prompt ativo. Retorna (prompt, fonte) onde fonte é 's3' ou 'ssm'.
    Tenta S3 primeiro — fallback para SSM se S3 falhar ou estiver vazio.
    """
    prompt = _s3_get(PROMPT_KEY_ACTIVE)
    if prompt:
        return prompt, "s3"

    logger.info("Prompt não encontrado no S3 — tentando SSM (fallback)")
    prompt = _ssm_get(PARAM_ACTIVE)
    if prompt:
        return prompt, "ssm"

    return None, "none"


# ── Handlers ──────────────────────────────────────────────────────────────────

def _handle_get() -> dict:
    active, fonte = _read_active_prompt()
    meta          = _get_meta()

    # Lista versões anteriores disponíveis para rollback
    versions = []
    if PROMPT_BUCKET:
        raw_versions = _s3_list_versions(PROMPT_KEY_ACTIVE)
        versions = [
            {
                "version_id":   v["VersionId"],
                "saved_at":     v["LastModified"].isoformat(),
                "size_bytes":   v["Size"],
            }
            for v in raw_versions
        ]

    return {
        "statusCode": 200,
        "headers":    _HEADERS,
        "body":       json.dumps({
            "active":          active or "",
            "has_backup":      len(versions) > 0 or bool(_s3_get(PROMPT_KEY_BACKUP)),
            "active_saved_at": meta.get("active_saved_at"),
            "saved_by":        meta.get("saved_by", "unknown"),
            "source":          fonte,
            "versions":        versions,
        })
    }


def _handle_put(body: dict) -> dict:
    new_prompt = (body.get("prompt") or "").strip()
    saved_by   = body.get("saved_by", "sergio")

    if not new_prompt:
        return _error(400, "Campo 'prompt' é obrigatório.")

    errors = validate_prompt(new_prompt)
    if errors:
        return {
            "statusCode": 422,
            "headers":    _HEADERS,
            "body":       json.dumps({"ok": False, "errors": errors})
        }

    # Copia prompt atual para backup antes de sobrescrever
    current = _s3_get(PROMPT_KEY_ACTIVE)
    if current:
        _s3_put(PROMPT_KEY_BACKUP, current, metadata={"backed_up_at": _now(), "backed_up_by": saved_by})

    now = _now()
    version_id = _s3_put(
        PROMPT_KEY_ACTIVE,
        new_prompt,
        metadata={"saved_by": saved_by, "saved_at": now}
    )

    if version_id is None:
        return _error(500, "Falha ao salvar no S3. Verifique PROMPT_BUCKET.")

    # Atualiza metadados no SSM
    meta = _get_meta()
    meta["active_saved_at"] = now
    meta["saved_by"]        = saved_by
    meta["last_version_id"] = version_id
    _save_meta(meta)

    logger.info(f"Prompt salvo no S3 por {saved_by} | chars={len(new_prompt)} | version={version_id}")

    return {
        "statusCode": 200,
        "headers":    _HEADERS,
        "body":       json.dumps({
            "ok":              True,
            "chars":           len(new_prompt),
            "active_saved_at": now,
            "version_id":      version_id,
            "backup_created":  True,  # S3 Versioning mantém automaticamente
        })
    }


def _handle_rollback(body: dict) -> dict:
    saved_by   = body.get("saved_by", "sergio")
    version_id = body.get("version_id")  # opcional — se não informado, usa a versão anterior

    if not PROMPT_BUCKET:
        return _error(500, "PROMPT_BUCKET não configurado.")

    # Se não informou version_id, pega a versão imediatamente anterior
    if not version_id:
        versions = _s3_list_versions(PROMPT_KEY_ACTIVE, max_versions=1)
        if not versions:
            return _error(404, "Nenhuma versão anterior disponível para rollback.")
        version_id = versions[0]["VersionId"]

    # Lê a versão alvo
    backup = _s3_get_version(PROMPT_KEY_ACTIVE, version_id)
    if not backup:
        return _error(404, f"Versão {version_id} não encontrada.")

    errors = validate_prompt(backup)
    if errors:
        return _error(422, f"Versão corrompida — não pode ser restaurada: {'; '.join(errors)}")

    # Salva a versão antiga como nova versão ativa (cria nova entrada no histórico)
    now        = _now()
    new_ver_id = _s3_put(
        PROMPT_KEY_ACTIVE,
        backup,
        metadata={"saved_by": f"rollback:{saved_by}", "saved_at": now, "restored_from": version_id}
    )

    if new_ver_id is None:
        return _error(500, "Falha ao restaurar versão no S3.")

    meta = _get_meta()
    meta["active_saved_at"] = now
    meta["saved_by"]        = f"rollback:{saved_by}"
    meta["last_version_id"] = new_ver_id
    _save_meta(meta)

    logger.info(f"Rollback executado por {saved_by} | restored_from={version_id} | new_version={new_ver_id}")

    return {
        "statusCode": 200,
        "headers":    _HEADERS,
        "body":       json.dumps({
            "ok":              True,
            "active_saved_at": now,
            "restored_from":   version_id,
            "new_version_id":  new_ver_id,
            "message":         "Versão restaurada com sucesso.",
        })
    }


def _error(status: int, message: str) -> dict:
    return {
        "statusCode": status,
        "headers":    _HEADERS,
        "body":       json.dumps({"ok": False, "error": message})
    }


# ── Entry point ───────────────────────────────────────────────────────────────

def lambda_handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")
    path   = event.get("rawPath", "").replace("/dev", "").replace("/prod", "")

    try:
        if method == "GET":
            return _handle_get()

        body = {}
        if event.get("body"):
            try:
                body = json.loads(event["body"])
            except Exception:
                return _error(400, "Body inválido — esperado JSON.")

        if method == "POST" and path.endswith("/rollback"):
            return _handle_rollback(body)

        if method == "PUT":
            return _handle_put(body)

        return _error(405, "Método não permitido.")

    except Exception as e:
        logger.error(f"Erro no prompt_manager: {e}")
        return _error(500, f"Erro interno: {str(e)}")
