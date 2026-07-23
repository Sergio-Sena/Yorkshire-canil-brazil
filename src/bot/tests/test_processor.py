"""
test_processor.py — Testes unitários para processor.py
Foco: lógica de horário comercial (23h30–8h) e pending_transfer
"""

import sys
import os
import json
import pytest
from unittest.mock import patch, MagicMock
from freezegun import freeze_time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lambda"))

os.environ["WHATSAPP_TOKEN"]        = "test-token"
os.environ["WHATSAPP_PHONE_ID"]     = "123456789"
os.environ["WHATSAPP_APP_SECRET"]   = "test-secret"
os.environ["WEBHOOK_VERIFY_TOKEN"]  = "test-verify"
os.environ["DYNAMODB_TABLE"]        = "yorkshire-bot-conversations-test"
os.environ["AWS_REGION"]            = "us-east-1"
os.environ["AWS_DEFAULT_REGION"]    = "us-east-1"
os.environ["AWS_ACCESS_KEY_ID"]     = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
os.environ["THIAGO_PHONE"]          = "5511977118201"
os.environ["SERGIO_PHONE"]          = "5511999999999"
os.environ["GUARDRAIL_ID"]          = ""


# ── _is_business_hours — limites exatos ──────────────────────────────────────

@freeze_time("2024-01-15 11:00:00", tz_offset=-3)  # 08h00 BRT — início comercial
def test_is_business_hours_at_8h():
    from processor import _is_business_hours
    assert _is_business_hours() is True


@freeze_time("2024-01-15 10:59:00", tz_offset=-3)  # 07h59 BRT — ainda noturno
def test_is_business_hours_at_759():
    from processor import _is_business_hours
    assert _is_business_hours() is False


@freeze_time("2024-01-15 02:29:00", tz_offset=-3)  # 23h29 BRT — ainda comercial
def test_is_business_hours_at_2329():
    from processor import _is_business_hours
    assert _is_business_hours() is True


@freeze_time("2024-01-15 02:30:00", tz_offset=-3)  # 23h30 BRT — início noturno
def test_is_business_hours_at_2330():
    from processor import _is_business_hours
    assert _is_business_hours() is False


@freeze_time("2024-01-15 02:31:00", tz_offset=-3)  # 23h31 BRT — modo noturno
def test_is_business_hours_at_2331():
    from processor import _is_business_hours
    assert _is_business_hours() is False


@freeze_time("2024-01-15 03:00:00", tz_offset=-3)  # 00h00 BRT — madrugada
def test_is_business_hours_at_midnight():
    from processor import _is_business_hours
    assert _is_business_hours() is False


@freeze_time("2024-01-15 17:00:00", tz_offset=-3)  # 14h00 BRT — meio do dia
def test_is_business_hours_midday():
    from processor import _is_business_hours
    assert _is_business_hours() is True


# ── _process_action — horário comercial notifica Thiago imediatamente ────────

@freeze_time("2024-01-15 17:00:00", tz_offset=-3)  # 14h BRT
@patch("processor.schedule_followup")
@patch("processor.save_pending_transfer")
@patch("processor._notify_thiago")
@patch("processor.save_conversation")
@patch("processor.send_message")
def test_process_action_transfer_business_hours(
    mock_send, mock_save_conv, mock_notify, mock_pending, mock_followup
):
    from processor import _process_action
    response     = {"action": "transfer", "message": "Vou te conectar!", "reason": "Cliente quer fechar", "lead_data": {"name": "João"}}
    conversation = {"history": [], "lead_data": {}}

    _process_action("5511999", response, conversation, "quero fechar")

    mock_notify.assert_called_once()           # notifica Thiago imediatamente
    mock_pending.assert_not_called()           # NÃO salva como pendente
    mock_followup.assert_not_called()


# ── _process_action — fora do horário salva pending_transfer ─────────────────

@freeze_time("2024-01-15 03:00:00", tz_offset=-3)  # 00h BRT — madrugada
@patch("processor.schedule_followup")
@patch("processor.save_pending_transfer")
@patch("processor._notify_thiago")
@patch("processor.save_conversation")
@patch("processor.send_message")
def test_process_action_transfer_night_mode(
    mock_send, mock_save_conv, mock_notify, mock_pending, mock_followup
):
    from processor import _process_action
    response     = {"action": "transfer", "message": "Vou te conectar!", "reason": "Quer fechar", "lead_data": {"name": "Ana"}}
    conversation = {"history": [], "lead_data": {}}

    _process_action("5511999", response, conversation, "quero fechar")

    mock_notify.assert_not_called()            # NÃO notifica agora
    mock_pending.assert_called_once()          # salva para 8h
    mock_followup.assert_called_once_with("5511999", followup_number=1)


# ── _is_owner_message ─────────────────────────────────────────────────────────

def test_is_owner_message_with_status_only():
    from processor import _is_owner_message
    body = {"entry": [{"changes": [{"value": {"statuses": [{"id": "s1"}], "contacts": []}}]}]}
    assert _is_owner_message(body) is True


def test_is_owner_message_with_contacts():
    from processor import _is_owner_message
    body = {"entry": [{"changes": [{"value": {"contacts": [{"wa_id": "5511999"}], "messages": [{}]}}]}]}
    assert _is_owner_message(body) is False


def test_is_owner_message_malformed():
    from processor import _is_owner_message
    assert _is_owner_message({}) is False
