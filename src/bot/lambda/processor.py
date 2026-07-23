"""
processor.py — Lambda Processor (acionado pelo SQS)
Timeout: 60s | Sem pressão de tempo — cliente já recebeu 200 do webhook.
Processa: DynamoDB → Bedrock → WhatsApp → ações pós-resposta.
"""

import json
import logging
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from whatsapp import extract_message, send_message, send_typing, mask_phone
from dynamodb import (
    get_conversation, save_conversation, archive_lead, recover_lead,
    save_pending_transfer, schedule_followup
)
from bedrock import generate_response
from config import (
    BUSINESS_HOURS_START, NIGHT_MODE_START_HOUR, NIGHT_MODE_START_MINUTE,
    FOLLOWUP_TIMEZONE, THIAGO_PHONE
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TZ = ZoneInfo(FOLLOWUP_TIMEZONE)


def lambda_handler(event, context):
    """Entry point SQS — processa cada record individualmente."""
    for record in event.get("Records", []):
        try:
            body = json.loads(record["body"])
            _process(body)
        except Exception as e:
            logger.error(f"Erro ao processar record SQS: {e}")
            raise  # re-raise → SQS recoloca na fila (até maxReceiveCount → DLQ)


# ── Processamento principal ───────────────────────────────────────────────────

def _process(raw_body: dict):
    message = extract_message(raw_body)
    if not message:
        return

    phone    = message["phone"]
    text     = message["text"]
    msg_type = message["type"]

    logger.info(f"Processando mensagem de {mask_phone(phone)}")

    # Thiago respondendo manualmente → pausa IA
    if _is_owner_message(raw_body):
        _mark_human_takeover(phone)
        return

    # Sprint 2 — áudio: Transcribe + Comprehend Sentiment
    if msg_type == "audio":
        # TODO Sprint 2: text = transcribe_audio(message["audio_url"])
        # TODO Sprint 2: if is_negative_sentiment(text): _handle_negative_sentiment(phone); return
        send_message(phone, "Olá! No momento só consigo processar mensagens de texto. Como posso te ajudar? 😊")
        return

    if msg_type != "text":
        send_message(phone, "Olá! No momento só consigo processar mensagens de texto. Como posso te ajudar? 😊")
        return

    # Busca ou recupera conversa
    conversation = get_conversation(phone) or recover_lead(phone) or _new_conversation(phone)

    if conversation.get("human_takeover"):
        return

    send_typing(phone)

    response = generate_response(
        phone=phone,
        message=text,
        history=conversation.get("history", []),
        lead_data=conversation.get("lead_data", {})
    )

    _process_action(phone, response, conversation, text)


# ── Ações pós-resposta ────────────────────────────────────────────────────────

def _process_action(phone: str, response: dict, conversation: dict, message_in: str):
    action  = response.get("action", "reply")
    message = response.get("message", "")
    media   = response.get("media")
    lead    = response.get("lead_data", {})

    if media:
        send_message(phone, message, media=media)
    else:
        send_message(phone, message)

    save_conversation(phone, message_in=message_in, message_out=message, lead_data=lead)

    if action in ("transfer", "close"):
        reason = response.get("reason", "") if action == "transfer" else "Fechamento — aguardando sinal 30%"

        if _is_business_hours():
            # Horário comercial — notifica Thiago imediatamente via WhatsApp
            _notify_thiago(phone, lead, reason)
        else:
            # Fora do horário — salva para notificar às 8h via EventBridge
            save_pending_transfer(phone, lead, reason)
            schedule_followup(phone, followup_number=1)
            logger.info(f"Lead quente fora do horário — agendado para 8h: {mask_phone(phone)}")

    elif action == "archive":
        archive_lead(phone)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _is_business_hours() -> bool:
    """Retorna True se fora do modo noturno (23h30–8h00, America/Sao_Paulo)."""
    now  = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(TZ)
    h, m = now.hour, now.minute
    # Modo noturno: >= 23h30 OU < 8h00
    after_cutoff  = (h > NIGHT_MODE_START_HOUR) or (h == NIGHT_MODE_START_HOUR and m >= NIGHT_MODE_START_MINUTE)
    before_morning = h < BUSINESS_HOURS_START
    return not (after_cutoff or before_morning)


def _notify_thiago(phone: str, lead: dict, reason: str):
    """Notifica Thiago diretamente no WhatsApp — sem SNS."""
    if not THIAGO_PHONE:
        logger.warning("THIAGO_PHONE não configurado — notificação não enviada")
        return

    name = lead.get("name", "Cliente")
    city = lead.get("city", "?")
    pref = lead.get("preference", "?")

    send_message(THIAGO_PHONE, (
        f"🔥 *Lead Yorkshire*\n"
        f"📱 {mask_phone(phone)}\n"
        f"👤 {name} — {city}\n"
        f"🐶 Preferência: {pref}\n"
        f"📋 {reason}"
    ))
    logger.info(f"Thiago notificado via WhatsApp: {mask_phone(phone)}")


def _is_owner_message(body: dict) -> bool:
    """Detecta status de entrega (Thiago respondendo) vs mensagem de cliente."""
    try:
        value = body["entry"][0]["changes"][0]["value"]
        return bool(value.get("statuses")) and not bool(value.get("contacts"))
    except (KeyError, IndexError):
        return False


def _mark_human_takeover(phone: str):
    conversation = get_conversation(phone) or {}
    save_conversation(phone, message_in="", message_out="[HUMAN_TAKEOVER]",
                      lead_data={**conversation.get("lead_data", {}), "human_takeover": True})
    logger.info(f"IA pausada — Thiago assumiu {mask_phone(phone)}")


def _new_conversation(phone: str) -> dict:
    return {"phone": phone, "history": [], "lead_data": {}, "human_takeover": False, "status": "new"}
