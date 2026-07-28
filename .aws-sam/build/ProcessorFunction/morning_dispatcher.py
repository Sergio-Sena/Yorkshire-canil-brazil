"""
morning_dispatcher.py — Lambda acionada pelo EventBridge às 8h (BRT)
Busca todos os leads com pending_transfer e notifica Thiago via WhatsApp.
"""

import logging
from whatsapp import send_message, mask_phone
from dynamodb import get_pending_transfers, clear_pending_transfer
from config import THIAGO_PHONE

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    if not THIAGO_PHONE:
        logger.error("THIAGO_PHONE não configurado — dispatcher abortado")
        return

    leads = get_pending_transfers()

    if not leads:
        logger.info("Nenhum lead noturno pendente")
        return

    logger.info(f"{len(leads)} lead(s) noturno(s) para notificar")

    # Resumo consolidado se houver muitos leads
    if len(leads) > 3:
        _send_summary(leads)
    else:
        for lead in leads:
            _notify_single(lead)

    # Marca todos como notificados
    for lead in leads:
        clear_pending_transfer(lead["phone"])


def _notify_single(lead: dict):
    phone     = lead["phone"]
    lead_data = lead.get("lead_data", {})
    transfer  = lead.get("pending_transfer", {})

    name   = lead_data.get("name", "Cliente")
    city   = lead_data.get("city", "?")
    pref   = lead_data.get("preference", "?")
    reason = transfer.get("reason", "")
    time   = transfer.get("created_at", "")[:16].replace("T", " às ")

    send_message(THIAGO_PHONE, (
        f"🌙 *Lead da madrugada*\n"
        f"📱 {mask_phone(phone)}\n"
        f"👤 {name} — {city}\n"
        f"🐶 Preferência: {pref}\n"
        f"🕐 Contato: {time}\n"
        f"📋 {reason}"
    ))
    logger.info(f"Thiago notificado sobre lead noturno: {mask_phone(phone)}")


def _send_summary(leads: list):
    lines = [f"🌙 *{len(leads)} leads da madrugada — resumo:*\n"]
    for i, lead in enumerate(leads, 1):
        ld   = lead.get("lead_data", {})
        name = ld.get("name", "Cliente")
        city = ld.get("city", "?")
        pref = ld.get("preference", "?")
        lines.append(f"{i}. {name} ({city}) — {pref} — {mask_phone(lead['phone'])}")

    lines.append("\nResponda cada um pelo WhatsApp normalmente. 💪")
    send_message(THIAGO_PHONE, "\n".join(lines))
    logger.info(f"Resumo de {len(leads)} leads noturnos enviado para Thiago")
