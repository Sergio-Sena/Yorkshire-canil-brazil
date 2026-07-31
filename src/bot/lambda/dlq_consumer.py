"""
dlq_consumer.py — Consome a Dead Letter Queue
Quando o processor falha 3x, o cliente ficaria no vazio.
Esta Lambda extrai o número do payload, manda mensagem de fallback
e notifica Sergio via SNS.
"""

import json
import logging
from whatsapp import send_message, mask_phone
from dynamodb import get_conversation, save_conversation
from notifier import notify_sergio
from config import THIAGO_PHONE

logger = logging.getLogger()
logger.setLevel(logging.INFO)

_FALLBACK_MSG = (
    "Oi! Tivemos uma instabilidade técnica agora e não consegui processar "
    "sua mensagem. Nossa equipe já foi avisada e entrará em contato em breve! 🐾"
)


def lambda_handler(event, context):
    for record in event.get("Records", []):
        try:
            _process(record)
        except Exception as e:
            logger.error(f"Erro no DLQ consumer: {e}")
            # Não re-raise — mensagem já está na DLQ, não queremos loop infinito


def _process(record: dict):
    body = json.loads(record["body"])

    phone = _extract_phone(body)
    if not phone:
        logger.error(f"DLQ: não foi possível extrair phone do payload: {str(body)[:200]}")
        return

    logger.warning(f"DLQ consumer acionado | phone={mask_phone(phone)}")

    # Só envia fallback se não houver human_takeover ativo
    conversation = get_conversation(phone) or {}
    if conversation.get("lead_data", {}).get("human_takeover"):
        logger.info(f"Human takeover ativo — fallback suprimido | phone={mask_phone(phone)}")
        return

    send_message(phone, _FALLBACK_MSG)
    save_conversation(phone, message_in="[DLQ]", message_out=_FALLBACK_MSG,
                      lead_data=conversation.get("lead_data", {}))

    notify_sergio(
        f"⚠️ *DLQ acionada*\n"
        f"📱 {mask_phone(phone)}\n"
        f"Mensagem não processada após 3 tentativas.\n"
        f"Cliente avisado do fallback."
    )


def _extract_phone(body: dict) -> str | None:
    """Extrai o número do cliente do payload original do webhook."""
    try:
        return body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    except (KeyError, IndexError, TypeError):
        return None
