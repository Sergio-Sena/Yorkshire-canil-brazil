"""
whatsapp.py — Integração com Meta WhatsApp Business API
"""

import hashlib
import hmac
import json
import logging
import random
import time
import urllib.request
import urllib.error
from config import (
    WHATSAPP_TOKEN, WHATSAPP_PHONE_ID,
    WHATSAPP_APP_SECRET, TYPING_DELAY_MIN, TYPING_DELAY_MAX
)

logger = logging.getLogger()


# ── Webhook ──────────────────────────────────────────────────────────────────

def verify_webhook(params: dict, verify_token: str) -> dict:
    """Valida o handshake do webhook da Meta."""
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == verify_token:
        return {"statusCode": 200, "body": params.get("hub.challenge", "")}
    return {"statusCode": 403, "body": "Forbidden"}


def validate_signature(body_raw: str, signature_header: str) -> bool:
    """
    Valida X-Hub-Signature-256 da Meta (HMAC-SHA256 com App Secret).
    Deve ser chamado antes de qualquer processamento do payload POST.
    """
    if not signature_header or not signature_header.startswith("sha256="):
        logger.warning("Webhook sem assinatura — rejeitado")
        return False

    expected = hmac.new(
        WHATSAPP_APP_SECRET.encode(),
        body_raw.encode(),
        hashlib.sha256
    ).hexdigest()

    received = signature_header.removeprefix("sha256=")
    valid = hmac.compare_digest(expected, received)

    if not valid:
        logger.warning("Assinatura do webhook inválida — possível request forjado")
    return valid


# ── Extração de mensagem ─────────────────────────────────────────────────────

def extract_message(body: dict) -> dict | None:
    """
    Extrai dados relevantes do payload do webhook.
    Retorna dict com phone, text, type, message_id ou None se não for mensagem.
    """
    try:
        value = body["entry"][0]["changes"][0]["value"]
        messages = value.get("messages")
        if not messages:
            return None

        msg = messages[0]
        msg_type = msg.get("type", "unknown")
        phone = msg["from"]
        message_id = msg.get("id", "")

        if msg_type == "text":
            text = msg["text"]["body"]
        elif msg_type == "interactive":
            # Botões ou listas de resposta rápida
            interactive = msg["interactive"]
            if interactive["type"] == "button_reply":
                text = interactive["button_reply"]["title"]
            elif interactive["type"] == "list_reply":
                text = interactive["list_reply"]["title"]
            else:
                text = ""
        else:
            text = ""

        return {"phone": phone, "text": text, "type": msg_type, "message_id": message_id}

    except (KeyError, IndexError, TypeError):
        return None


def mask_phone(phone: str) -> str:
    """Mascara número para logs — ex: 5511977118201 → 55119****8201"""
    if len(phone) < 8:
        return "****"
    return phone[:5] + "****" + phone[-4:]


# ── Envio de mensagem ────────────────────────────────────────────────────────

def send_message(phone: str, text: str, media: dict | None = None) -> bool:
    """
    Envia mensagem de texto ou mídia (image/video/document).
    media = {"type": "image", "url": "https://..."}
    """
    if media:
        payload = _build_media_payload(phone, text, media)
    else:
        payload = {
            "messaging_product": "whatsapp",
            "to": phone,
            "type": "text",
            "text": {"body": text, "preview_url": False}
        }

    return _post(payload)


def send_typing(phone: str) -> None:
    """Simula digitação com delay humanizado."""
    delay = random.uniform(TYPING_DELAY_MIN, TYPING_DELAY_MAX)
    time.sleep(delay)


# ── Helpers internos ─────────────────────────────────────────────────────────

def _build_media_payload(phone: str, caption: str, media: dict) -> dict:
    media_type = media.get("type", "image")
    media_content = {"caption": caption}
    if "id" in media:
        media_content["id"] = media["id"]
    else:
        media_content["link"] = media["url"]
    return {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": media_type,
        media_type: media_content
    }


def _post(payload: dict) -> bool:
    data = json.dumps(payload).encode("utf-8")
    api_url = f"https://graph.facebook.com/v19.0/{WHATSAPP_PHONE_ID}/messages"
    logger.info(f"WhatsApp payload: {json.dumps(payload)[:300]}")
    logger.info(f"WhatsApp API URL: {api_url}")
    req = urllib.request.Request(
        api_url,
        data=data,
        headers={
            "Authorization": f"Bearer {WHATSAPP_TOKEN}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode()
            logger.info(f"WhatsApp API response {resp.status}: {body[:200]}")
            return resp.status == 200
    except urllib.error.HTTPError as e:
        logger.error(f"WhatsApp API error {e.code}: {e.read().decode()}")
    except Exception as e:
        logger.error(f"WhatsApp send failed: {e}")
        return False
