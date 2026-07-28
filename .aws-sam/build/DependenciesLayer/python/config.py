"""
config.py — Configurações e regras comerciais do Yorkshire Canil Brazil
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── AWS ──────────────────────────────────────────────────────────────────────
AWS_REGION       = os.getenv("AWS_REGION", "us-east-1")
DYNAMODB_TABLE   = os.getenv("DYNAMODB_TABLE", "yorkshire-bot-conversations")
SNS_TOPIC_ARN    = os.getenv("SNS_TOPIC_ARN", "")
SQS_QUEUE_URL    = os.getenv("SQS_QUEUE_URL", "")   # fila FIFO — webhook → processor
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-sonnet-4-5")

# ── WhatsApp ──────────────────────────────────────────────────────────────────
WHATSAPP_TOKEN       = os.getenv("WHATSAPP_TOKEN", "")
WHATSAPP_PHONE_ID    = os.getenv("WHATSAPP_PHONE_ID", "")
WHATSAPP_APP_SECRET  = os.getenv("WHATSAPP_APP_SECRET", "")  # HMAC-SHA256 webhook
WEBHOOK_VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN", "")


def get_whatsapp_api_url() -> str:
    """URL lazy — garante que WHATSAPP_PHONE_ID já foi carregado."""
    return f"https://graph.facebook.com/v19.0/{WHATSAPP_PHONE_ID}/messages"


WHATSAPP_API_URL = get_whatsapp_api_url()

# ── Delay humanizado (segundos) ───────────────────────────────────────────────
TYPING_DELAY_MIN = 2
TYPING_DELAY_MAX = 5

# ── Limites de conversa ───────────────────────────────────────────────────────
MAX_TURNS              = 20   # após 20 mensagens sem fechamento → transfere pro Thiago
MAX_INJECTION_ATTEMPTS = 3    # tentativas de injection antes de bloquear
CONVERSATION_TTL_DAYS  = 90   # LGPD — dados apagados automaticamente após 90 dias

# ── Horário comercial (America/Sao_Paulo) ─────────────────────────────────────
BUSINESS_HOURS_START    = 8     # 08:00 — início do atendimento humano
BUSINESS_HOURS_END      = 21    # 21:00 — usado apenas como referência
NIGHT_MODE_START_HOUR   = 23    # 23:00 ─┐ início do modo noturno
NIGHT_MODE_START_MINUTE = 30    # :30   ─┘ (23h30)
NIGHT_MODE_END_HOUR     = 8     # 08:00 — fim do modo noturno
THIAGO_PHONE         = os.getenv("THIAGO_PHONE", "")  # WhatsApp do Thiago para notificação direta

# ── Follow-up ─────────────────────────────────────────────────────────────────
FOLLOWUP_1_HOUR   = 11    # às 11h do dia seguinte
FOLLOWUP_2_DAYS   = 30    # 30 dias após follow-up 1
FOLLOWUP_TIMEZONE = "America/Sao_Paulo"

# ── Bedrock Guardrails ────────────────────────────────────────────────────────
GUARDRAIL_ID      = os.getenv("GUARDRAIL_ID", "")
GUARDRAIL_VERSION = os.getenv("GUARDRAIL_VERSION", "DRAFT")

# Padrões de prompt injection para sanitização prévia (regex, case-insensitive)
INJECTION_PATTERNS = [
    r"ignore\s+(suas\s+)?instru[çc][õo]es",
    r"novo\s+prompt",
    r"modo\s+(teste|dev|desenvolvedor)",
    r"sem\s+restri[çc][õo]es",
    r"revel[ae]\s+(o\s+)?(prompt|instru[çc][õo]es|sistema)",
    r"repita\s+(suas\s+)?instru[çc][õo]es",
    r"\[SYSTEM\]",
    r"\[INSTRU[ÇC][ÃA]O\]",
    r"finja\s+que\s+voc[êe]",
    r"voc[êe]\s+agora\s+[ée]",
    r"\bDAN\b",
    r"jailbreak",
]

# ── Regras comerciais ─────────────────────────────────────────────────────────

PRICES = {
    "capital_100km": {
        "macho": 3949,
        "femea": 4949,
        "descricao": "Capital e cidades até 100km"
    },
    "acima_100km": {
        "macho": 5449,
        "femea": 6449,
        "descricao": "Cidades acima de 100km"
    },
    "outros_estados": {
        "macho": 6990,
        "femea": 7990,
        "descricao": "Outros estados"
    }
}

PIX_DISCOUNT_MAX = 300

INSTALLMENTS = {
    1:  0.00,
    2:  0.00,
    3:  0.00,
    4:  0.10,
    5:  0.10,
    6:  0.10,
    7:  0.10,
    8:  0.11,
    9:  0.12,
    10: 0.13,
    11: 0.14,
    12: 0.15
}

RESERVATION_DEPOSIT_PCT = 0.30

FRETE_INCLUSO = True

LOCATION_BY_CLIENT = {
    "SP": "Minas Gerais",
    "default": "São Paulo"
}

INCLUDED_ITEMS = [
    "1ª dose da vacina",
    "Vermifugado",
    "Contrato de compra e venda",
    "Pedigree",
    "Microchip",
    "Ração super premium de cortesia",
    "Acompanhamento inicial"
]

INTERNATIONAL_TRANSFER = True
