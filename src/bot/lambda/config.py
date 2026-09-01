"""
config.py — Configurações e regras comerciais do Yorkshire Canil Brazil
"""

import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Em Lambda as vars vêm das env vars do runtime

# ── AWS ──────────────────────────────────────────────────────────────────────
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "yorkshire-bot-conversations")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN", "")
# fila FIFO — webhook → processor
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL", "")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "us.anthropic.claude-haiku-4-5-20251001-v1:0")

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
MAX_TURNS = 20   # após 20 mensagens sem fechamento → transfere pro Thiago
MAX_INJECTION_ATTEMPTS = 3    # tentativas de injection antes de bloquear
MAX_MESSAGE_LENGTH = 1000  # limite de caracteres por mensagem
CONVERSATION_TTL_DAYS = 90   # LGPD — dados apagados automaticamente após 90 dias

# ── Horário comercial (America/Sao_Paulo) ─────────────────────────────────────
BUSINESS_HOURS_START = 8     # 08:00 — início do atendimento humano
BUSINESS_HOURS_END = 21    # 21:00 — usado apenas como referência
NIGHT_MODE_START_HOUR = 23    # 23:00 ─┐ início do modo noturno
NIGHT_MODE_START_MINUTE = 30    # :30   ─┘ (23h30)
NIGHT_MODE_END_HOUR = 8     # 08:00 — fim do modo noturno
# WhatsApp do Thiago para notificação direta
THIAGO_PHONE = os.getenv("THIAGO_PHONE", "")

# ── Follow-up ─────────────────────────────────────────────────────────────────
FOLLOWUP_1_HOUR = 11    # às 11h do dia seguinte
FOLLOWUP_2_DAYS = 30    # 30 dias após follow-up 1
FOLLOWUP_TIMEZONE = "America/Sao_Paulo"

# ── Bedrock Guardrails ────────────────────────────────────────────────────────
GUARDRAIL_ID = os.getenv("GUARDRAIL_ID", "")
GUARDRAIL_VERSION = os.getenv("GUARDRAIL_VERSION", "DRAFT")

# Padrões de prompt injection para sanitização prévia (regex, case-insensitive)
INJECTION_PATTERNS = [
    # Português
    r"ignore\s+(suas\s+)?instru[çc][õo]es",
    r"novo\s+prompt",
    r"modo\s+(teste|dev|desenvolvedor)",
    r"sem\s+restri[çc][õo]es",
    r"revel[ae]\s+(o\s+)?(prompt|instru[çc][õo]es|sistema)",
    r"repita\s+(suas\s+)?instru[çc][õo]es",
    r"finja\s+que\s+voc[êe]",
    r"voc[êe]\s+agora\s+[ée]",
    r"esquece\s+(as\s+)?regras",
    r"sem\s+filtros?",
    r"desative\s+(o\s+)?(filtro|guardrail|restri[çc][õo]es)",
    # Inglês
    r"ignore\s+(your\s+)?instructions",
    r"ignore\s+previous",
    r"forget\s+(your\s+)?(rules|instructions|guidelines)",
    r"act\s+as\s+(a\s+)?(?:different|new|another)",
    r"pretend\s+(you\s+are|to\s+be)",
    r"you\s+are\s+now",
    r"new\s+persona",
    r"without\s+(any\s+)?restrictions?",
    r"no\s+(more\s+)?restrictions?",
    r"bypass\s+(the\s+)?(filter|guardrail|rules)",
    # Tags e encoding
    r"\[SYSTEM\]",
    r"\[INSTRU[ÇC][ÃA]O\]",
    r"<\s*/?\s*(?:system|prompt|inst|instruction)\s*>",
    r"base64",
    r"\\u00[0-9a-fA-F]{2}",
    # Jailbreaks conhecidos
    r"\bDAN\b",
    r"jailbreak",
    r"developer\s+mode",
    r"god\s+mode",
]

# ── Regras comerciais ─────────────────────────────────────────────────────────

PRICES = {
    "grande_sp": {
        "macho": 3949,
        "femea": 4949,
        "descricao": "SP capital e Grande SP (lista de cidades)"
    },
    "interior_sp": {
        "macho": 5449,
        "femea": 6449,
        "descricao": "Interior de SP (fora da lista Grande SP)"
    },
    "outros_estados": {
        "macho": 6990,
        "femea": 7990,
        "descricao": "Outros estados (RJ, MG, PR etc)"
    }
}

# Cidades da Grande SP com mesmo preço da capital
GRANDE_SP_CITIES = {
    "são paulo", "sao paulo",
    "são caetano do sul", "sao caetano do sul", "são caetano", "sao caetano",
    "taboão da serra", "taboao da serra", "taboão", "taboao",
    "guarulhos",
    "santo andré", "santo andre",
    "osasco",
    "são bernardo do campo", "sao bernardo do campo", "são bernardo", "sao bernardo",
    "diadema",
    "mauá", "maua",
    "carapicuíba", "carapicuiba",
    "embu das artes", "embu",
    "barueri",
    "ferraz de vasconcelos", "ferraz",
    "cotia",
    "ribeirão pires", "ribeirao pires",
    "caieiras",
    "itapecerica da serra", "itapecerica",
    "jandira",
    "itapevi",
    "santana de parnaíba", "santana de parnaiba",
    "arujá", "aruja",
    "mairiporã", "mairipora",
    "itaquaquecetuba", "itaquá", "itaqua",
    "cajamar",
    "vargem grande paulista", "vargem grande",
    "francisco morato",
    "poá", "poa",
    "suzano",
    "rio grande da serra",
    "embu-guaçu", "embu guacu", "embu-guacu",
    "são lourenço da serra", "sao lourenco da serra",
    "araçariguama", "aracariguama",
    "várzea paulista", "varzea paulista",
    "santa isabel",
    "campo limpo paulista", "campo limpo",
    "jundiaí", "jundiai",
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

FORCE_NIGHT_MODE = os.getenv(
    "FORCE_NIGHT_MODE", "").lower() in ("1", "true", "yes")
MEDIA_JSON_URL = os.getenv(
    "MEDIA_JSON_URL", "https://d10mjoe1zes9j1.cloudfront.net/yorkshire/media.json")

# Localização declarada ao cliente para dissuadir retirada (não afeta preço)
LOCATION_BY_CLIENT = {
    "SP": "Minas Gerais",
    "default": "São Paulo"
}

# Faixa de preço por estado — SP tem lógica especial (cidade determina tier)
# Para SP: grande_sp ou interior_sp dependendo da cidade (ver GRANDE_SP_CITIES)
# Para demais estados: sempre outros_estados
PRICE_TIER_BY_STATE = {
    "SP": "interior_sp",   # fallback SP — cidade não identificada na lista Grande SP
    "default": "outros_estados"
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
