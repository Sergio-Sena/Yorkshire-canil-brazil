"""
prompt_manager.py — CRUD do system prompt via SSM Parameter Store
Endpoints:
  GET  /prompt           → retorna prompt ativo + backup + metadados
  PUT  /prompt           → valida + salva novo (move atual para backup)
  POST /prompt/rollback  → restaura backup como ativo
"""

import json
import logging
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from zoneinfo import ZoneInfo
from config import AWS_REGION, FOLLOWUP_TIMEZONE

logger = logging.getLogger()
logger.setLevel(logging.INFO)

_ssm = boto3.client("ssm", region_name=AWS_REGION)
TZ   = ZoneInfo(FOLLOWUP_TIMEZONE)

PARAM_ACTIVE = "/yorkshire-bot/prompt/active"
PARAM_BACKUP = "/yorkshire-bot/prompt/backup"
PARAM_META   = "/yorkshire-bot/prompt/meta"

_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json"
}

# Actions que o Claude precisa conhecer para responder corretamente
REQUIRED_ACTIONS = ["reply", "transfer", "close", "archive", "send_media"]

# Seções estruturais que garantem o comportamento correto do bot
REQUIRED_SECTIONS = [
    "IDENTIDADE E COMPORTAMENTO",
    "SEGURANÇA E LIMITES",
    "FORMATO DE RESPOSTA",
]

MIN_LENGTH = 500
MAX_LENGTH = 15_000


# ── Validação ─────────────────────────────────────────────────────────────────

def validate_prompt(prompt: str) -> list:
    """Retorna lista de erros. Lista vazia = prompt válido e seguro para deploy."""
    errors = []

    if len(prompt) < MIN_LENGTH:
        errors.append(f"Prompt muito curto ({len(prompt)} chars). Mínimo: {MIN_LENGTH}.")

    if len(prompt) > MAX_LENGTH:
        errors.append(f"Prompt muito longo ({len(prompt)} chars). Máximo: {MAX_LENGTH}.")

    for action in REQUIRED_ACTIONS:
        if action not in prompt:
            errors.append(f"Action obrigatória ausente no prompt: {action}")

    for section in REQUIRED_SECTIONS:
        if section not in prompt:
            errors.append(f"Seção obrigatória ausente: {section}")

    return errors


# ── SSM helpers ───────────────────────────────────────────────────────────────

def _get_param(name: str):
    try:
        resp = _ssm.get_parameter(Name=name, WithDecryption=False)
        return resp["Parameter"]["Value"]
    except ClientError as e:
        if e.response["Error"]["Code"] == "ParameterNotFound":
            return None
        raise


def _put_param(name: str, value: str) -> None:
    _ssm.put_parameter(Name=name, Value=value, Type="String", Overwrite=True, Tier="Advanced")


def _get_meta() -> dict:
    raw = _get_param(PARAM_META)
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except Exception:
        return {}


def _save_meta(meta: dict) -> None:
    _ssm.put_parameter(Name=PARAM_META, Value=json.dumps(meta), Type="String", Overwrite=True)


def _now() -> str:
    return datetime.now(TZ).isoformat()


# ── Handlers ──────────────────────────────────────────────────────────────────

def _handle_get() -> dict:
    active = _get_param(PARAM_ACTIVE)
    backup = _get_param(PARAM_BACKUP)
    meta   = _get_meta()

    return {
        "statusCode": 200,
        "headers": _HEADERS,
        "body": json.dumps({
            "active":          active or "",
            "backup":          backup or "",
            "has_backup":      backup is not None,
            "active_saved_at": meta.get("active_saved_at"),
            "backup_saved_at": meta.get("backup_saved_at"),
            "saved_by":        meta.get("saved_by", "unknown"),
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
            "headers": _HEADERS,
            "body": json.dumps({"ok": False, "errors": errors})
        }

    # Move ativo atual para backup antes de salvar o novo
    current_active = _get_param(PARAM_ACTIVE)
    meta           = _get_meta()

    if current_active:
        _put_param(PARAM_BACKUP, current_active)
        meta["backup_saved_at"] = meta.get("active_saved_at", _now())

    _put_param(PARAM_ACTIVE, new_prompt)
    meta["active_saved_at"] = _now()
    meta["saved_by"]        = saved_by
    _save_meta(meta)

    logger.info(f"Prompt atualizado por {saved_by} | chars={len(new_prompt)}")

    return {
        "statusCode": 200,
        "headers": _HEADERS,
        "body": json.dumps({
            "ok":              True,
            "chars":           len(new_prompt),
            "active_saved_at": meta["active_saved_at"],
            "backup_created":  current_active is not None,
        })
    }


def _handle_rollback(body: dict) -> dict:
    saved_by = body.get("saved_by", "sergio")
    backup   = _get_param(PARAM_BACKUP)

    if not backup:
        return _error(404, "Nenhum backup disponível para rollback.")

    errors = validate_prompt(backup)
    if errors:
        return _error(422, f"Backup corrompido — não pode ser restaurado: {'; '.join(errors)}")

    current_active = _get_param(PARAM_ACTIVE)
    meta           = _get_meta()

    # Swap: backup → ativo, ativo → backup
    _put_param(PARAM_ACTIVE, backup)
    if current_active:
        _put_param(PARAM_BACKUP, current_active)
        meta["backup_saved_at"] = meta.get("active_saved_at", _now())

    meta["active_saved_at"] = _now()
    meta["saved_by"]        = f"rollback:{saved_by}"
    _save_meta(meta)

    logger.info(f"Rollback executado por {saved_by}")

    return {
        "statusCode": 200,
        "headers": _HEADERS,
        "body": json.dumps({
            "ok":              True,
            "active_saved_at": meta["active_saved_at"],
            "message":         "Backup restaurado com sucesso.",
        })
    }


def _error(status: int, message: str) -> dict:
    return {
        "statusCode": status,
        "headers": _HEADERS,
        "body": json.dumps({"ok": False, "error": message})
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
