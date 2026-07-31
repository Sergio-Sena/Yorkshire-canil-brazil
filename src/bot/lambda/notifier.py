"""
notifier.py — Lambda de alertas técnicos
Acionada pelo SNS quando CloudWatch detecta mensagem na DLQ.
Envia alerta via WhatsApp para o Sergio (responsável técnico do bot).
"""

import json
import logging
import os
from whatsapp import send_message

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SERGIO_PHONE = os.getenv("SERGIO_PHONE", "")   # ex: 5511999999999


def notify_sergio(text: str) -> None:
    """Envia mensagem direta para Sergio no WhatsApp. Reutilizável por outras Lambdas."""
    if not SERGIO_PHONE:
        logger.error("SERGIO_PHONE não configurado — notificação não enviada")
        return
    sent = send_message(SERGIO_PHONE, text)
    if not sent:
        logger.error("Falha ao enviar notificação WhatsApp para Sergio")


def lambda_handler(event, context):
    for record in event.get("Records", []):
        try:
            _handle_sns(record)
        except Exception as e:
            logger.error(f"Erro no notifier: {e}")


def _handle_sns(record: dict):
    sns_msg  = record.get("Sns", {})
    subject  = sns_msg.get("Subject", "Alerta Yorkshire Bot")
    message  = sns_msg.get("Message", "")

    # Tenta parsear JSON do CloudWatch Alarm
    try:
        alarm = json.loads(message)
        alarm_name  = alarm.get("AlarmName", subject)
        alarm_state = alarm.get("NewStateValue", "ALARM")
        reason      = alarm.get("NewStateReason", "")

        text = (
            f"🚨 *Alerta Yorkshire Bot*\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"⚠️ {alarm_name}\n"
            f"📊 Estado: {alarm_state}\n"
            f"📋 {reason}\n\n"
            f"Acesse o console AWS para investigar:\n"
            f"SQS → yorkshire-bot-dlq"
        )
    except (json.JSONDecodeError, KeyError):
        # Mensagem SNS genérica (não é alarm do CloudWatch)
        text = f"🚨 *Alerta Yorkshire Bot*\n{subject}\n{message[:300]}"

    if not SERGIO_PHONE:
        logger.error("SERGIO_PHONE não configurado — alerta não enviado")
        return

    sent = send_message(SERGIO_PHONE, text)
    if sent:
        logger.info(f"Alerta enviado para Sergio: {alarm_name if 'alarm_name' in dir() else subject}")
    else:
        logger.error("Falha ao enviar alerta WhatsApp para Sergio")
