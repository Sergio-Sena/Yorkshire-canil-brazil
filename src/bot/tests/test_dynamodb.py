"""
test_dynamodb.py — Testes unitários para dynamodb.py (DynamoDB mockado com moto)
"""

import sys
import os
import time
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lambda"))

os.environ["WHATSAPP_TOKEN"]       = "test-token"
os.environ["WHATSAPP_PHONE_ID"]    = "123456789"
os.environ["WHATSAPP_APP_SECRET"]  = "test-secret"
os.environ["WEBHOOK_VERIFY_TOKEN"] = "test-verify"
os.environ["DYNAMODB_TABLE"]       = "yorkshire-bot-conversations-test"
os.environ["AWS_REGION"]           = "us-east-1"
os.environ["AWS_DEFAULT_REGION"]   = "us-east-1"
os.environ["AWS_ACCESS_KEY_ID"]    = "test"
os.environ["AWS_SECRET_ACCESS_KEY"]= "test"

import boto3
from moto import mock_aws


def _create_table(dynamodb):
    dynamodb.create_table(
        TableName="yorkshire-bot-conversations-test",
        AttributeDefinitions=[
            {"AttributeName": "phone",       "AttributeType": "S"},
            {"AttributeName": "record_type", "AttributeType": "S"},
            {"AttributeName": "followup_ts", "AttributeType": "N"},
        ],
        KeySchema=[
            {"AttributeName": "phone",       "KeyType": "HASH"},
            {"AttributeName": "record_type", "KeyType": "RANGE"},
        ],
        GlobalSecondaryIndexes=[{
            "IndexName": "followup-index",
            "KeySchema": [
                {"AttributeName": "record_type", "KeyType": "HASH"},
                {"AttributeName": "followup_ts",  "KeyType": "RANGE"},
            ],
            "Projection": {"ProjectionType": "ALL"},
        }],
        BillingMode="PAY_PER_REQUEST",
    )


# ── Idempotência ──────────────────────────────────────────────────────────────

@mock_aws
def test_is_duplicate_message_first_time():
    _create_table(boto3.resource("dynamodb", region_name="us-east-1"))
    import importlib, dynamodb as db
    importlib.reload(db)
    assert db.is_duplicate_message("msg-001") is False


@mock_aws
def test_is_duplicate_message_second_time():
    _create_table(boto3.resource("dynamodb", region_name="us-east-1"))
    import importlib, dynamodb as db
    importlib.reload(db)
    db.is_duplicate_message("msg-002")
    assert db.is_duplicate_message("msg-002") is True


# ── save_conversation / get_conversation ──────────────────────────────────────

@mock_aws
def test_save_and_get_conversation():
    _create_table(boto3.resource("dynamodb", region_name="us-east-1"))
    import importlib, dynamodb as db
    importlib.reload(db)

    db.save_conversation("5511999", "Quero um filhote", "Olá! Temos machos e fêmeas 😊",
                         lead_data={"name": "João", "city": "SP"})
    conv = db.get_conversation("5511999")

    assert conv is not None
    assert conv["phone"] == "5511999"
    assert len(conv["history"]) == 2
    assert conv["lead_data"]["name"] == "João"
    assert "ttl" in conv  # LGPD


@mock_aws
def test_save_conversation_merges_lead_data():
    _create_table(boto3.resource("dynamodb", region_name="us-east-1"))
    import importlib, dynamodb as db
    importlib.reload(db)

    db.save_conversation("5511999", "msg1", "resp1", lead_data={"name": "João"})
    db.save_conversation("5511999", "msg2", "resp2", lead_data={"city": "SP"})
    conv = db.get_conversation("5511999")

    assert conv["lead_data"]["name"] == "João"
    assert conv["lead_data"]["city"] == "SP"


@mock_aws
def test_history_capped_at_40():
    _create_table(boto3.resource("dynamodb", region_name="us-east-1"))
    import importlib, dynamodb as db
    importlib.reload(db)

    for i in range(25):
        db.save_conversation("5511999", f"msg{i}", f"resp{i}")

    conv = db.get_conversation("5511999")
    assert len(conv["history"]) <= 40


# ── archive_lead / recover_lead ───────────────────────────────────────────────

@mock_aws
def test_archive_and_recover_lead():
    _create_table(boto3.resource("dynamodb", region_name="us-east-1"))
    import importlib, dynamodb as db
    importlib.reload(db)

    db.save_conversation("5511999", "oi", "olá", lead_data={"name": "Maria"})
    db.archive_lead("5511999")

    assert db.get_conversation("5511999") is None

    recovered = db.recover_lead("5511999")
    assert recovered is not None
    assert recovered["lead_data"]["name"] == "Maria"
    assert recovered["status"] == "recovered"
    assert recovered["human_takeover"] is False


# ── schedule_followup — SK dedicado sobrevive ao archive ─────────────────────

@mock_aws
def test_followup_survives_archive():
    _create_table(boto3.resource("dynamodb", region_name="us-east-1"))
    import importlib, dynamodb as db
    importlib.reload(db)

    db.save_conversation("5511999", "oi", "olá", lead_data={"name": "Carlos"})
    db.schedule_followup("5511999", followup_number=1)
    db.archive_lead("5511999")

    # CONV foi apagado mas FOLLOWUP deve existir
    assert db.get_conversation("5511999") is None

    table = boto3.resource("dynamodb", region_name="us-east-1").Table("yorkshire-bot-conversations-test")
    resp  = table.get_item(Key={"phone": "5511999", "record_type": "FOLLOWUP"})
    assert resp.get("Item") is not None
    assert resp["Item"]["status"] == "pending"
    assert "followup_ts" in resp["Item"]


# ── save_conversation com status e human_takeover no nível raiz ──────────────

@mock_aws
def test_save_conversation_status_at_root():
    _create_table(boto3.resource("dynamodb", region_name="us-east-1"))
    import importlib, dynamodb as db
    importlib.reload(db)

    db.save_conversation("5511999", "", "[FECHAMENTO]", lead_data={"name": "João"},
                         status="fechado", human_takeover=True)
    conv = db.get_conversation("5511999")

    assert conv["status"] == "fechado"
    assert conv["human_takeover"] is True
    assert "status" not in conv.get("lead_data", {})
    assert "human_takeover" not in conv.get("lead_data", {})


# ── pending_transfer ──────────────────────────────────────────────────────────

@mock_aws
def test_save_and_get_pending_transfer():
    _create_table(boto3.resource("dynamodb", region_name="us-east-1"))
    import importlib, dynamodb as db
    importlib.reload(db)

    db.save_conversation("5511999", "quero fechar", "ótimo!", lead_data={"name": "Ana"})
    db.save_pending_transfer("5511999", {"name": "Ana", "city": "RJ"}, "Quer fechar — madrugada")

    pending = db.get_pending_transfers()
    assert len(pending) == 1
    assert pending[0]["phone"] == "5511999"
    assert pending[0]["status"] == "hot_lead_pending"


@mock_aws
def test_clear_pending_transfer():
    _create_table(boto3.resource("dynamodb", region_name="us-east-1"))
    import importlib, dynamodb as db
    importlib.reload(db)

    db.save_conversation("5511999", "msg", "resp", lead_data={})
    db.save_pending_transfer("5511999", {}, "teste")
    db.clear_pending_transfer("5511999")

    pending = db.get_pending_transfers()
    assert len(pending) == 0
