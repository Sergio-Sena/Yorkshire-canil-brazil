# Chatbot IA para Qualificação de Leads — Arquitetura Futura

## Visão Geral

Bot conversacional no site que atende visitantes 24/7, responde dúvidas frequentes sobre o canil e direciona leads qualificados para atendimento humano via WhatsApp.

---

## Quando Implementar

| Sinal | Ação |
|---|---|
| Cliente perde leads fora do horário | Implementar fase 1 |
| 50+ mensagens/dia repetitivas | Implementar fase 2 |
| Quer insights sobre o público | Implementar fase 3 |

---

## Arquitetura

```
┌─────────────────────────────────────────────────────┐
│                    SITE (Frontend)                    │
│                                                      │
│  Widget de Chat → API Gateway → Lambda (orquestrador)│
└─────────────────────┬───────────────────────────────┘
                      │
         ┌────────────┼────────────────┐
         │            │                │
         ▼            ▼                ▼
   ┌──────────┐ ┌──────────┐   ┌─────────────┐
   │ Amazon   │ │ Amazon   │   │  Amazon     │
   │ Lex v2   │ │ Bedrock  │   │  Comprehend │
   │          │ │ (Claude) │   │             │
   │ Entende  │ │ Responde │   │ Análise de  │
   │ intenção │ │ contexto │   │ sentimento  │
   └────┬─────┘ └────┬─────┘   └──────┬──────┘
        │             │                │
        └──────┬──────┘                │
               ▼                       ▼
        ┌─────────────┐        ┌─────────────┐
        │  DynamoDB   │        │     S3      │
        │             │        │             │
        │ Leads       │        │ Logs de     │
        │ Conversas   │        │ conversas   │
        │ Qualificação│        │ para análise│
        └──────┬──────┘        └─────────────┘
               │
        ┌──────┴──────┐
        │             │
        ▼             ▼
  ┌──────────┐  ┌──────────┐
  │ SNS/SES  │  │ WhatsApp │
  │          │  │ Business │
  │ Notifica │  │ API      │
  │ cliente  │  │          │
  │ novo lead│  │ Handoff  │
  └──────────┘  │ humano   │
                └──────────┘
```

---

## Fases de Implementação

### Fase 1 — Bot Básico (FAQ automático)
**Custo:** ~$10/mês
**Tempo:** 1-2 dias

- Amazon Lex v2 com intents:
  - Preço do filhote
  - Disponibilidade
  - Formas de pagamento
  - Entrega
  - Vacinas/pedigree
- Respostas pré-definidas
- Se não entender → direciona para WhatsApp
- Widget simples no site (iframe ou JS)

### Fase 2 — Bot Inteligente (Bedrock)
**Custo:** ~$20-30/mês
**Tempo:** 3-5 dias

- Amazon Bedrock (Claude 3 Haiku — mais barato)
- Contexto do canil injetado no prompt (RAG simples)
- Conversa natural sobre:
  - Raça Yorkshire
  - Cuidados com filhote
  - Diferencial do canil
  - Linhagem e títulos
- Qualificação do lead:
  - Pergunta nome, cidade, interesse
  - Classifica: quente / morno / frio
- Lead quente → notifica cliente via SNS + direciona WhatsApp
- DynamoDB salva todas as conversas

### Fase 3 — Analytics com Comprehend
**Custo:** ~$5-10/mês adicional
**Tempo:** 2-3 dias

- Amazon Comprehend analisa mensagens:
  - Sentimento (positivo/negativo/neutro)
  - Entidades (cidade, nome, raça mencionada)
  - Tópicos mais perguntados
  - Idioma
- Dashboard de insights:
  - Perguntas mais frequentes
  - Horários de pico
  - Cidades com mais interesse
  - Taxa de conversão do bot
- S3 armazena logs para análise histórica
- Relatório mensal automático para o cliente

---

## Stack Técnica

| Serviço | Função | Custo estimado |
|---|---|---|
| Amazon Lex v2 | Entender intenção | ~$0.75/1000 requests |
| Amazon Bedrock (Haiku) | Respostas inteligentes | ~$0.25/1000 requests |
| Amazon Comprehend | Análise de sentimento | ~$0.01/100 unidades |
| Lambda | Orquestração | ~$0.20/1M requests |
| DynamoDB | Armazenar leads/conversas | ~$1-2/mês |
| API Gateway | Endpoint do chat | ~$1/mês |
| SNS | Notificações | ~$0.50/mês |
| S3 | Logs para análise | ~$0.02/mês |

**Total estimado:** $10-30/mês dependendo do volume

---

## Modelo de Qualificação de Lead

```json
{
  "lead_id": "uuid",
  "nome": "João Silva",
  "cidade": "São Paulo",
  "interesse": "filhote fêmea",
  "qualificacao": "quente",
  "sentimento": "positivo",
  "perguntas": ["preço", "disponibilidade", "entrega"],
  "timestamp": "2024-01-15T14:30:00Z",
  "encaminhado_whatsapp": true
}
```

### Critérios de Qualificação:
- **Quente:** Perguntou preço + disponibilidade + forma de pagamento
- **Morno:** Perguntou sobre a raça/cuidados
- **Frio:** Só curiosidade, não deixou contato

---

## Insights do Comprehend (exemplos)

### Relatório Mensal:
- 📊 **150 conversas** no mês
- 🔥 **45 leads quentes** (30% conversão)
- 📍 **Top cidades:** SP (40%), RJ (25%), MG (15%)
- ❓ **Pergunta #1:** "Qual o preço?" (78%)
- ❓ **Pergunta #2:** "Tem disponível?" (65%)
- ❓ **Pergunta #3:** "Entrega para minha cidade?" (45%)
- 😊 **Sentimento:** 85% positivo
- ⏰ **Horário pico:** 19h-22h (fora do comercial — bot essencial)

---

## Precificação para o Cliente

| Item | Valor |
|---|---|
| Implementação Fase 1 | R$ 1.500 |
| Implementação Fase 2 | R$ 2.500 |
| Implementação Fase 3 | R$ 1.500 |
| Pacote completo (1+2+3) | R$ 4.500 |
| Manutenção mensal | R$ 150-250/mês |
| Custo AWS (repasse) | R$ 50-150/mês |

---

## Prompt Base para Bedrock (Fase 2)

```
Você é o assistente virtual do Yorkshire Canil Brazil, um canil campeão nacional e sul-americano, referência em Yorkshire Terrier na América Latina desde 2014.

Seu papel:
- Responder dúvidas sobre filhotes, raça, cuidados
- Qualificar o interesse do visitante
- Coletar nome e cidade quando possível
- Direcionar para WhatsApp quando o lead estiver quente

Informações do canil:
- Filhotes com pedigree completo
- Vacinados e vermifugados
- Entrega para todo o Brasil
- Acompanhamento veterinário
- Suporte vitalício ao tutor
- Campeão Nacional e Sul-Americano FECAM

Tom: Profissional, acolhedor, premium. Nunca fale preço diretamente — direcione para WhatsApp.
```

---

## Próximos Passos

1. Aguardar volume de mensagens justificar
2. Implementar Fase 1 (Lex básico) como teste
3. Medir conversão bot vs direto
4. Se positivo, evoluir para Fase 2 e 3

---

**Criado:** 2025-05-20
**Status:** Documentado para implementação futura
**Prioridade:** Baixa (aguardando demanda)
