"""
dynamodb.py — Histórico de conversas, leads e follow-up
Tabela única: yorkshire-bot-conversations (PK: phone, SK: record_type)
"""

import logging
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import boto3
from boto3.dynamodb.conditions import Key
from config import AWS_REGION, DYNAMODB_TABLE, FOLLOWUP_1_HOUR, FOLLOWUP_TIMEZONE, CONVERSATION_TTL_DAYS

logger = logging.getLogger()

_dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
_table    = _dynamodb.Table(DYNAMODB_TABLE)

TZ        = ZoneInfo(FOLLOWUP_TIMEZONE)
SK_CONV     = "CONV"       # conversa ativa
SK_ARCH     = "ARCHIVED"   # conversa arquivada
SK_MSGID    = "MSGID"      # controle de idempotência
SK_FOLLOWUP = "FOLLOWUP"   # registro dedicado de follow-up (independente de CONV/ARCH)


# ── Leitura ──────────────────────────────────────────────────────────────────

def is_duplicate_message(message_id: str) -> bool:
    """
    Verifica se message_id já foi processado (idempotência).
    Usa conditional write — se já existe retorna True (duplicata).
    """
    try:
        _table.put_item(
            Item={
                "phone":       f"MSGID#{message_id}",
                "record_type": SK_MSGID,
                "ttl":         int(time.time()) + 86400  # expira em 24h
            },
            ConditionExpression="attribute_not_exists(phone)"
        )
        return False  # inseriu — mensagem nova
    except _dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
        return True   # já existia — duplicata


def get_conversation(phone: str) -> dict | None:
    """Retorna conversa ativa ou None se não existir."""
    resp = _table.get_item(Key={"phone": phone, "record_type": SK_CONV})
    return resp.get("Item")


def recover_lead(phone: str) -> dict | None:
    """Recupera lead arquivado e o reativa como nova conversa."""
    resp = _table.get_item(Key={"phone": phone, "record_type": SK_ARCH})
    item = resp.get("Item")
    if not item:
        return None

    # Reativa mantendo histórico e lead_data anteriores
    conversation = {
        "phone":          phone,
        "record_type":    SK_CONV,
        "history":        item.get("history", []),
        "lead_data":      item.get("lead_data", {}),
        "human_takeover": False,
        "status":         "recovered",
        "turns":          0,
        "updated_at":     _now()
    }
    _table.put_item(Item=conversation)
    _table.delete_item(Key={"phone": phone, "record_type": SK_ARCH})
    logger.info(f"Lead recuperado: {phone}")
    return conversation


# ── Escrita ──────────────────────────────────────────────────────────────────

def save_conversation(
    phone: str,
    message_in: str,
    message_out: str,
    lead_data: dict | None = None
) -> None:
    """
    Atualiza histórico e lead_data da conversa ativa.
    Incrementa turns e persiste timestamp.
    """
    conv = get_conversation(phone) or {
        "phone":          phone,
        "record_type":    SK_CONV,
        "history":        [],
        "lead_data":      {},
        "human_takeover": False,
        "status":         "active",
        "turns":          0
    }

    # Append ao histórico apenas se houver conteúdo
    if message_in:
        conv["history"].append({"role": "user",      "content": message_in,  "ts": _now()})
    if message_out:
        conv["history"].append({"role": "assistant", "content": message_out, "ts": _now()})

    # Mantém histórico em no máximo 40 entradas (20 turns) para controlar tamanho do item
    conv["history"] = conv["history"][-40:]

    if lead_data:
        conv["lead_data"] = {**conv.get("lead_data", {}), **lead_data}

    conv["turns"]      = conv.get("turns", 0) + (1 if message_in else 0)
    conv["updated_at"] = _now()
    conv["ttl"]        = int(time.time()) + (CONVERSATION_TTL_DAYS * 86400)  # LGPD

    _table.put_item(Item=conv)


def archive_lead(phone: str) -> None:
    """Move conversa ativa para registro arquivado (lead frio / sem interesse)."""
    conv = get_conversation(phone)
    if not conv:
        return

    conv["record_type"] = SK_ARCH
    conv["archived_at"] = _now()
    conv["ttl"]         = int(time.time()) + (CONVERSATION_TTL_DAYS * 86400)  # mantém TTL LGPD

    _table.put_item(Item=conv)
    _table.delete_item(Key={"phone": phone, "record_type": SK_CONV})
    logger.info(f"Lead arquivado: {phone}")


# ── Follow-up ────────────────────────────────────────────────────────────────

def schedule_followup(phone: str, followup_number: int) -> None:
    """
    Cria SK=FOLLOWUP dedicado — independente de CONV ou ARCHIVED.
    Garante que o follow-up sobrevive ao archive_lead().
    followup_number: 1 = D+1 às 11h | 2 = D+30 às 11h
    EventBridge faz scan por status='pending' neste SK para disparar.
    """
    now  = datetime.now(TZ)
    days = 1 if followup_number == 1 else 30
    target = (now + timedelta(days=days)).replace(
        hour=FOLLOWUP_1_HOUR, minute=0, second=0, microsecond=0
    )

    # Busca lead_data atual de qualquer SK disponível
    conv = get_conversation(phone)
    if not conv:
        conv = _table.get_item(Key={"phone": phone, "record_type": SK_ARCH}).get("Item", {})

    _table.put_item(Item={
        "phone":          phone,
        "record_type":    SK_FOLLOWUP,
        "followup_num":   followup_number,
        "followup_at":    target.isoformat(),
        "followup_ts":    int(target.timestamp()),   # para query numérica no EventBridge
        "status":         "pending",
        "lead_data":      conv.get("lead_data", {}),
        "ttl":            int(time.time()) + (CONVERSATION_TTL_DAYS * 86400)  # LGPD
    })
    logger.info(f"Follow-up {followup_number} agendado para {phone} em {target.isoformat()}")


def save_pending_transfer(phone: str, lead: dict, reason: str) -> None:
    """Salva lead quente fora do horário comercial para notificar Thiago às 8h."""
    conv = get_conversation(phone) or {}
    conv["lead_data"] = {**conv.get("lead_data", {}), **lead}
    conv["pending_transfer"] = {
        "reason":     reason,
        "created_at": _now()
    }
    conv["status"] = "hot_lead_pending"
    _table.put_item(Item={**conv,
        "phone":       phone,
        "record_type": SK_CONV,
        "ttl":         int(time.time()) + (CONVERSATION_TTL_DAYS * 86400)
    })
    logger.info(f"Transfer pendente salvo para {phone} — será notificado às 8h")


def get_pending_transfers() -> list:
    """Retorna todos os leads com transfer pendente. Chamado pelo EventBridge às 8h."""
    resp = _table.scan(
        FilterExpression="attribute_exists(pending_transfer) AND #s = :status",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":status": "hot_lead_pending"}
    )
    return resp.get("Items", [])


def clear_pending_transfer(phone: str) -> None:
    """Remove flag de transfer pendente após notificar Thiago."""
    _table.update_item(
        Key={"phone": phone, "record_type": SK_CONV},
        UpdateExpression="REMOVE pending_transfer SET #s = :status",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":status": "active"}
    )


def mark_followup_sent(phone: str) -> None:
    """Marca follow-up como enviado para não reprocessar."""
    _table.update_item(
        Key={"phone": phone, "record_type": SK_FOLLOWUP},
        UpdateExpression="SET #s = :sent",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":sent": "sent"}
    )


def delete_conversation(phone: str) -> None:
    """Apaga todos os registros de um número do DynamoDB (CONV, ARCH, FOLLOWUP, MSGID)."""
    for sk in (SK_CONV, SK_ARCH, SK_FOLLOWUP):
        try:
            _table.delete_item(Key={"phone": phone, "record_type": sk})
        except Exception:
            pass
    logger.info(f"Conversa apagada: {phone}")


def delete_conversations(phones: list[str]) -> None:
    """Apaga conversas de uma lista de números."""
    for phone in phones:
        delete_conversation(phone)


# ── Helper ───────────────────────────────────────────────────────────────────

def _now() -> str:
    return datetime.now(TZ).isoformat()
