"""
processor.py — Lambda Processor (acionado pelo SQS)
Timeout: 60s | Sem pressão de tempo — cliente já recebeu 200 do webhook.
Processa: DynamoDB → Bedrock → WhatsApp → ações pós-resposta.
"""

import json
import logging
import urllib.request
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
    FOLLOWUP_TIMEZONE, THIAGO_PHONE, MEDIA_JSON_URL
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

    # Ignora mensagens do próprio Thiago (dono)
    if phone == THIAGO_PHONE:
        logger.info(f"Mensagem do Thiago ignorada: {mask_phone(phone)}")
        return

    # Ignora mensagens automáticas do bot antigo (loop de encerramento)
    if "Por falta de resposta, estamos encerrando esse atendimento" in text:
        logger.info(f"Mensagem do bot antigo ignorada: {mask_phone(phone)}")
        return

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

    if action == "send_media":
        logger.info(f"Enviando galeria de fotos para {mask_phone(phone)} | preference: {lead.get('preference')}")
        sent_urls = _send_media_gallery(phone, lead.get("preference", "indefinido"), first_caption=message or "Olha que lindo(a)! 🐶")
    elif media:
        send_message(phone, message, media=media)
    else:
        send_message(phone, message)

    if action == "close":
        _handle_close(phone, lead, conversation)
    elif action == "transfer":
        reason = response.get("reason", "")
        save_conversation(phone, message_in=message_in, message_out=message, lead_data=lead)
        if _is_business_hours():
            _notify_thiago(phone, lead, reason, history=conversation.get("history", []))
        else:
            save_pending_transfer(phone, lead, reason)
            schedule_followup(phone, followup_number=1)
            logger.info(f"Lead quente fora do horário — agendado para 8h: {mask_phone(phone)}")
    elif action == "archive":
        save_conversation(phone, message_in=message_in, message_out=message, lead_data=lead)
        archive_lead(phone)
    elif action == "send_media":
        save_conversation(phone, message_in=message_in, message_out=message, lead_data=lead, media_urls=sent_urls)
    else:
        save_conversation(phone, message_in=message_in, message_out=message, lead_data=lead)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _is_business_hours() -> bool:
    """Retorna True se fora do modo noturno (23h30–8h00, America/Sao_Paulo)."""
    now  = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(TZ)
    h, m = now.hour, now.minute
    # Modo noturno: >= 23h30 OU < 8h00
    after_cutoff  = (h > NIGHT_MODE_START_HOUR) or (h == NIGHT_MODE_START_HOUR and m >= NIGHT_MODE_START_MINUTE)
    before_morning = h < BUSINESS_HOURS_START
    return not (after_cutoff or before_morning)


def _send_media_gallery(phone: str, preference: str, first_caption: str = "Olha que lindo(a)! 🐶") -> list:
    """Busca fotos do media.json no CloudFront e envia para o cliente. Retorna lista de URLs enviadas."""
    try:
        with urllib.request.urlopen(MEDIA_JSON_URL, timeout=5) as resp:
            media_data = json.loads(resp.read())
    except Exception as e:
        logger.error(f"Erro ao carregar media.json: {e}")
        send_message(phone, "Vou pedir para o Thiago te enviar as fotos agora! 😊")
        return []

    fotos = media_data.get(preference, []) or media_data.get("femea", [])
    if not fotos:
        send_message(phone, "Vou pedir para o Thiago te enviar as fotos agora! 😊")
        return []

    sent_urls = []
    for i, foto in enumerate(fotos):
        caption = first_caption if i == 0 else ""
        media = {"type": "image", "id": foto["id"]} if "id" in foto else {"type": "image", "url": foto["url"]}
        send_message(phone, caption, media=media)
        if "url" in foto:
            sent_urls.append(foto["url"])
        if i < len(fotos) - 1:
            time.sleep(0.8)
    return sent_urls


def _handle_close(phone: str, lead: dict, conversation: dict):
    """Fluxo completo de fechamento: pausa IA e notifica Thiago."""
    from config import PRICES, PRICE_TIER_BY_STATE, RESERVATION_DEPOSIT_PCT

    # 1. Pausa a IA nessa conversa
    save_conversation(phone, message_in="", message_out="[FECHAMENTO]", lead_data=lead,
                      status="fechado", human_takeover=True)
    logger.info(f"Conversa pausada após fechamento | phone={mask_phone(phone)}")

    # 2. Notifica Thiago com resumo completo
    state      = lead.get("state", "")
    preference = lead.get("preference", "indefinido")
    reason = f"FECHAMENTO | Preferência: {preference} | Estado: {state or '?'}"
    if _is_business_hours():
        _notify_thiago(phone, lead, reason, history=conversation.get("history", []))
    else:
        save_pending_transfer(phone, lead, reason)
        schedule_followup(phone, followup_number=1)
        logger.info(f"Fechamento fora do horário — agendado para 8h: {mask_phone(phone)}")


def _notify_thiago(phone: str, lead: dict, reason: str, history: list = None):
    """Notifica Thiago diretamente no WhatsApp — sem SNS."""
    if not THIAGO_PHONE:
        logger.warning("THIAGO_PHONE não configurado — notificação não enviada")
        return

    name    = lead.get("name", "Cliente")
    city    = lead.get("city", "?")
    pref    = lead.get("preference", "?")
    payment = lead.get("payment", "indefinido")
    now     = datetime.now(TZ).strftime("%d/%m/%Y %H:%M")

    # Resumo das últimas 6 mensagens da conversa
    resumo = ""
    if history:
        ultimas = history[-6:]
        linhas = []
        for m in ultimas:
            role  = "Cliente" if m.get("role") == "user" else "Bella"
            texto = (m.get("content") or "")[:200]
            linhas.append(f"_{role}:_ {texto}")
        resumo = "\n\n💬 *Últimas mensagens:*\n" + "\n".join(linhas)

    send_message(THIAGO_PHONE, (
        f"🔥 *Lead Yorkshire*\n"
        f"📅 {now}\n"
        f"📱 https://wa.me/{phone}\n"
        f"👤 {name} — {city}\n"
        f"🐶 Preferência: {pref}\n"
        f"💳 Pagamento: {payment}\n"
        f"📋 {reason}"
        f"{resumo}"
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
    save_conversation(phone, message_in="", message_out="[HUMAN_TAKEOVER]", human_takeover=True)
    logger.info(f"IA pausada — Thiago assumiu {mask_phone(phone)}")


def _new_conversation(phone: str) -> dict:
    return {"phone": phone, "history": [], "lead_data": {}, "human_takeover": False, "status": "new"}
