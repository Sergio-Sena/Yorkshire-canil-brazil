"""
conversations_manager.py — Gerenciamento de conversas para os painéis
Endpoints:
  GET  /conversations                      — lista conversas
  GET  /conversations/{phone}              — histórico completo
  POST /conversations/{phone}/takeover     — pausa o bot
  POST /conversations/{phone}/release      — devolve pro bot
  PATCH /conversations/{phone}/status      — atualiza status (painel Thiago)
"""

import json
import logging
import boto3
from datetime import datetime
from zoneinfo import ZoneInfo
from config import AWS_REGION, DYNAMODB_TABLE

logger = logging.getLogger()
logger.setLevel(logging.INFO)

_dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
_table    = _dynamodb.Table(DYNAMODB_TABLE)

TZ = ZoneInfo("America/Sao_Paulo")

SK_CONV = "CONV"
SK_ARCH = "ARCHIVED"

VALID_STATUSES = ["novo", "em_contato", "em_negociacao", "venda_realizada", "perdido"]


def lambda_handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")
    path   = event.get("rawPath", "").replace("/dev", "").replace("/prod", "")

    if method == "GET" and path == "/conversations":
        return _list_conversations()

    if method == "GET" and "/conversations/" in path and not _has_suffix(path):
        phone = _extract_phone(path)
        return _get_conversation(phone)

    if method == "POST" and path.endswith("/takeover"):
        return _set_takeover(_extract_phone(path, "/takeover"), True)

    if method == "POST" and path.endswith("/release"):
        return _set_takeover(_extract_phone(path, "/release"), False)

    if method == "PATCH" and path.endswith("/status"):
        body = _parse_body(event)
        return _update_status(_extract_phone(path, "/status"), body)

    return _resp(404, {"error": "Rota não encontrada"})


# ── Handlers ──────────────────────────────────────────────────────────────────

def _list_conversations():
    try:
        result = _table.scan(
            FilterExpression="record_type = :conv OR record_type = :arch",
            ExpressionAttributeValues={":conv": SK_CONV, ":arch": SK_ARCH},
            ProjectionExpression="phone, record_type, lead_data, human_takeover, #st, turns, updated_at, archived_at",
            ExpressionAttributeNames={"#st": "status"}
        )
        items = result.get("Items", [])
        conversations = []
        for item in items:
            lead = item.get("lead_data", {})
            conversations.append({
                "phone":          item["phone"],
                "type":           item["record_type"],
                "name":           lead.get("name", "Desconhecido"),
                "city":           lead.get("city", ""),
                "state":          lead.get("state", ""),
                "preference":     lead.get("preference", "indefinido"),
                "payment":        lead.get("payment", "indefinido"),
                "status":         item.get("status", "novo"),
                "lead_status":    lead.get("status", ""),
                "human_takeover": item.get("human_takeover", False),
                "turns":          item.get("turns", 0),
                "updated_at":     item.get("updated_at") or item.get("archived_at", ""),
            })
        conversations.sort(key=lambda x: x["updated_at"] or "", reverse=True)
        return _resp(200, {"conversations": conversations, "total": len(conversations)})
    except Exception as e:
        logger.error(f"Erro ao listar conversas: {e}")
        return _resp(500, {"error": str(e)})


def _get_conversation(phone: str):
    if not phone:
        return _resp(400, {"error": "phone obrigatório"})
    try:
        for sk in (SK_CONV, SK_ARCH):
            resp = _table.get_item(Key={"phone": phone, "record_type": sk})
            item = resp.get("Item")
            if item:
                return _resp(200, {
                    "phone":          item["phone"],
                    "type":           item["record_type"],
                    "lead_data":      item.get("lead_data", {}),
                    "human_takeover": item.get("human_takeover", False),
                    "status":         item.get("status", "novo"),
                    "turns":          item.get("turns", 0),
                    "updated_at":     item.get("updated_at", ""),
                    "history":        item.get("history", []),
                    "status_log":     item.get("status_log", []),
                })
        return _resp(404, {"error": "Conversa não encontrada"})
    except Exception as e:
        logger.error(f"Erro ao buscar conversa {phone}: {e}")
        return _resp(500, {"error": str(e)})


def _set_takeover(phone: str, takeover: bool):
    if not phone:
        return _resp(400, {"error": "phone obrigatório"})
    try:
        _table.update_item(
            Key={"phone": phone, "record_type": SK_CONV},
            UpdateExpression="SET human_takeover = :v, updated_at = :ts",
            ExpressionAttributeValues={
                ":v":  takeover,
                ":ts": datetime.now(TZ).isoformat()
            }
        )
        action = "pausado" if takeover else "devolvido ao bot"
        logger.info(f"Bot {action} para {phone}")
        return _resp(200, {"ok": True, "phone": phone, "human_takeover": takeover})
    except Exception as e:
        logger.error(f"Erro ao setar takeover {phone}: {e}")
        return _resp(500, {"error": str(e)})


def _update_status(phone: str, body: dict):
    if not phone:
        return _resp(400, {"error": "phone obrigatório"})

    new_status = body.get("status", "")
    changed_by = body.get("changed_by", "thiago")
    note       = body.get("note", "")

    if new_status not in VALID_STATUSES:
        return _resp(400, {"error": f"Status inválido. Use: {', '.join(VALID_STATUSES)}"})

    try:
        now = datetime.now(TZ).isoformat()

        # Busca status_log atual
        resp = _table.get_item(
            Key={"phone": phone, "record_type": SK_CONV},
            ProjectionExpression="status_log, #st",
            ExpressionAttributeNames={"#st": "status"}
        )
        item = resp.get("Item", {})
        log  = item.get("status_log", [])

        log.append({
            "status":     new_status,
            "changed_by": changed_by,
            "changed_at": now,
            "note":       note,
        })

        _table.update_item(
            Key={"phone": phone, "record_type": SK_CONV},
            UpdateExpression="SET #st = :s, status_log = :l, updated_at = :ts",
            ExpressionAttributeNames={"#st": "status"},
            ExpressionAttributeValues={
                ":s":  new_status,
                ":l":  log,
                ":ts": now,
            }
        )
        logger.info(f"Status atualizado {phone} → {new_status} por {changed_by}")
        return _resp(200, {"ok": True, "status": new_status, "changed_at": now})
    except Exception as e:
        logger.error(f"Erro ao atualizar status {phone}: {e}")
        return _resp(500, {"error": str(e)})


# ── Helpers ───────────────────────────────────────────────────────────────────

def _extract_phone(path: str, suffix: str = "") -> str:
    p = path.replace("/conversations/", "").replace(suffix, "")
    return p.strip("/")

def _has_suffix(path: str) -> bool:
    return any(path.endswith(s) for s in ["/takeover", "/release", "/status"])

def _parse_body(event: dict) -> dict:
    try:
        return json.loads(event.get("body") or "{}")
    except Exception:
        return {}

def _resp(status: int, body: dict) -> dict:
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,PATCH,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type,x-api-key",
        },
        "body": json.dumps(body, default=str)
    }
