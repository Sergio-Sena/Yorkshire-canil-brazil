"""
handler.py — Lambda Webhook (entry point do API Gateway)
Responsabilidade única: validar + enfileirar no SQS. Responde 200 em < 500ms.
Todo processamento pesado (Bedrock, DynamoDB, WhatsApp) fica no processor.py.
"""

import json
import logging
import boto3
from whatsapp import verify_webhook, validate_signature, extract_message, mask_phone
from dynamodb import is_duplicate_message
from config import WEBHOOK_VERIFY_TOKEN, SQS_QUEUE_URL, AWS_REGION

logger = logging.getLogger()
logger.setLevel(logging.INFO)

_sqs = boto3.client("sqs", region_name=AWS_REGION)


def lambda_handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")

    if method == "GET":
        params = event.get("queryStringParameters", {}) or {}
        return verify_webhook(params, WEBHOOK_VERIFY_TOKEN)

    if method == "POST":
        signature = event.get("headers", {}).get("x-hub-signature-256", "")
        if not validate_signature(event.get("body", ""), signature):
            return {"statusCode": 403, "body": "Forbidden"}

        return _enqueue(event)

    return {"statusCode": 405, "body": "Method Not Allowed"}


def _enqueue(event):
    try:
        body    = json.loads(event.get("body", "{}"))
        message = extract_message(body)

        if not message:
            return {"statusCode": 200, "body": "OK"}  # status de entrega, reação, etc.

        # Idempotência aqui — evita enfileirar duplicata antes mesmo do processor
        if is_duplicate_message(message["message_id"]):
            logger.info(f"Duplicata ignorada no webhook: {message['message_id']}")
            return {"statusCode": 200, "body": "OK"}

        logger.info(f"Enfileirando mensagem de {mask_phone(message['phone'])}")

        # MessageGroupId garante ordem FIFO por número de telefone
        _sqs.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=event.get("body", "{}"),
            MessageGroupId=message["phone"],
            MessageDeduplicationId=message["message_id"]
        )

        return {"statusCode": 200, "body": "OK"}

    except Exception as e:
        logger.error(f"Erro no webhook handler: {e}")
        return {"statusCode": 200, "body": "OK"}  # sempre 200 — Meta não reenviar
