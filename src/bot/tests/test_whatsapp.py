"""
test_whatsapp.py — Testes unitários para whatsapp.py
"""

import hashlib
import hmac
import json
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lambda"))

# Mock das variáveis de ambiente antes de importar o módulo
os.environ.setdefault("WHATSAPP_TOKEN",      "test-token")
os.environ.setdefault("WHATSAPP_PHONE_ID",   "123456789")
os.environ.setdefault("WHATSAPP_APP_SECRET", "test-secret")
os.environ.setdefault("WEBHOOK_VERIFY_TOKEN","test-verify")
os.environ.setdefault("DYNAMODB_TABLE",      "test-table")
os.environ.setdefault("AWS_REGION",          "us-east-1")
os.environ.setdefault("AWS_DEFAULT_REGION",  "us-east-1")

from whatsapp import verify_webhook, validate_signature, extract_message, mask_phone


# ── verify_webhook ────────────────────────────────────────────────────────────

def test_verify_webhook_valid():
    params = {"hub.mode": "subscribe", "hub.verify_token": "test-verify", "hub.challenge": "abc123"}
    result = verify_webhook(params, "test-verify")
    assert result["statusCode"] == 200
    assert result["body"] == "abc123"


def test_verify_webhook_wrong_token():
    params = {"hub.mode": "subscribe", "hub.verify_token": "wrong", "hub.challenge": "abc123"}
    result = verify_webhook(params, "test-verify")
    assert result["statusCode"] == 403


def test_verify_webhook_wrong_mode():
    params = {"hub.mode": "unsubscribe", "hub.verify_token": "test-verify", "hub.challenge": "abc123"}
    result = verify_webhook(params, "test-verify")
    assert result["statusCode"] == 403


# ── validate_signature ────────────────────────────────────────────────────────

def _make_signature(body: str, secret: str = "test-secret") -> str:
    sig = hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()
    return f"sha256={sig}"


def test_validate_signature_valid():
    body = '{"entry": []}'
    sig  = _make_signature(body)
    assert validate_signature(body, sig) is True


def test_validate_signature_invalid():
    body = '{"entry": []}'
    assert validate_signature(body, "sha256=invalido") is False


def test_validate_signature_missing_header():
    assert validate_signature('{"entry": []}', "") is False


def test_validate_signature_no_prefix():
    assert validate_signature('{"entry": []}', "semprefix") is False


# ── extract_message ───────────────────────────────────────────────────────────

def _make_payload(msg_type="text", text="Olá", phone="5511999999999", msg_id="msg-001"):
    payload = {
        "entry": [{
            "changes": [{
                "value": {
                    "contacts": [{"wa_id": phone}],
                    "messages": [{
                        "id":   msg_id,
                        "from": phone,
                        "type": msg_type,
                    }]
                }
            }]
        }]
    }
    if msg_type == "text":
        payload["entry"][0]["changes"][0]["value"]["messages"][0]["text"] = {"body": text}
    elif msg_type == "audio":
        payload["entry"][0]["changes"][0]["value"]["messages"][0]["audio"] = {"id": "audio-123"}
    elif msg_type == "interactive":
        payload["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"] = {
            "type": "button_reply",
            "button_reply": {"id": "btn1", "title": "Macho"}
        }
    return payload


def test_extract_message_text():
    msg = extract_message(_make_payload("text", "Quero um filhote"))
    assert msg is not None
    assert msg["phone"] == "5511999999999"
    assert msg["text"]  == "Quero um filhote"
    assert msg["type"]  == "text"
    assert msg["message_id"] == "msg-001"


def test_extract_message_audio():
    msg = extract_message(_make_payload("audio"))
    assert msg is not None
    assert msg["type"] == "audio"
    assert msg["text"] == ""


def test_extract_message_interactive_button():
    msg = extract_message(_make_payload("interactive"))
    assert msg is not None
    assert msg["text"] == "Macho"
    assert msg["type"] == "interactive"


def test_extract_message_no_messages():
    payload = {"entry": [{"changes": [{"value": {"statuses": [{"id": "s1"}]}}]}]}
    assert extract_message(payload) is None


def test_extract_message_empty_body():
    assert extract_message({}) is None


def test_extract_message_malformed():
    assert extract_message({"entry": "invalido"}) is None


# ── mask_phone ────────────────────────────────────────────────────────────────

def test_mask_phone_standard():
    assert mask_phone("5511977118201") == "55119****8201"


def test_mask_phone_short():
    assert mask_phone("123") == "****"
