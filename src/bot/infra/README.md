# Infraestrutura — Yorkshire Bot IA WhatsApp

## Visão Geral da Arquitetura

```
Meta WhatsApp
     │  HTTPS + X-Hub-Signature-256
     ▼
API Gateway (HTTP API)
     │  GET  /webhook → verificação Meta
     │  POST /webhook → mensagens
     ▼
Lambda WEBHOOK (handler.py)          timeout: 10s
     │  1. Valida HMAC-SHA256
     │  2. Checa idempotência (DynamoDB)
     │  3. Enfileira no SQS FIFO
     │  4. Retorna 200 em < 500ms
     ▼
SQS FIFO (yorkshire-bot-messages.fifo)
     │  MessageGroupId = phone       → ordem por cliente
     │  MessageDeduplicationId = id  → sem duplicata
     │  VisibilityTimeout: 90s
     │  maxReceiveCount: 3 → DLQ
     ▼
Lambda PROCESSOR (processor.py)      timeout: 60s
     │  1. DynamoDB — busca histórico
     │  2. Bedrock Claude Sonnet 4.5
     │  3. WhatsApp — envia resposta
     │  4. DynamoDB — salva histórico
     │  5. Se transfer/close fora do horário → save_pending_transfer
     ▼
DLQ (yorkshire-bot-dlq.fifo)
     │  Retenção: 24h
     ▼
CloudWatch Alarm
     ▼
SNS TechAlertTopic
     ├── E-mail Sergio (backup passivo)
     └── Lambda NOTIFIER (notifier.py)
              └── WhatsApp Sergio (ativo, imediato)

EventBridge cron(0 11 * * ? *)  →  8h BRT
     ▼
Lambda MORNING DISPATCHER (morning_dispatcher.py)
     └── WhatsApp Thiago — resumo dos leads noturnos pendentes
```

---

## Recursos AWS

| Recurso | Nome (dev) | Nome (prod) |
|---------|-----------|-------------|
| Lambda Webhook | yorkshire-bot-webhook-dev | yorkshire-bot-webhook-prod |
| Lambda Processor | yorkshire-bot-processor-dev | yorkshire-bot-processor-prod |
| Lambda Morning Dispatcher | yorkshire-bot-morning-dispatcher-dev | yorkshire-bot-morning-dispatcher-prod |
| Lambda Notifier | yorkshire-bot-notifier-dev | yorkshire-bot-notifier-prod |
| SQS FIFO | yorkshire-bot-messages-dev.fifo | yorkshire-bot-messages-prod.fifo |
| DLQ FIFO | yorkshire-bot-dlq-dev.fifo | yorkshire-bot-dlq-prod.fifo |
| DynamoDB | yorkshire-bot-conversations-dev | yorkshire-bot-conversations-prod |
| SNS TechAlert (Sergio) | yorkshire-bot-tech-alerts-dev | yorkshire-bot-tech-alerts-prod |
| EventBridge Rule | yorkshire-bot-morning-dispatch-dev | yorkshire-bot-morning-dispatch-prod |
| Lambda Layer | yorkshire-bot-deps-dev | yorkshire-bot-deps-prod |

---

## Alertas — Separação de Responsabilidades

| Alerta | Destino | Canal | Quando |
|--------|---------|-------|--------|
| Lead quente / fechamento (horário comercial) | Thiago | WhatsApp direto | Processor detecta action=transfer/close entre 8h–23h30 |
| Lead quente / fechamento (modo noturno 23h30–8h) | Thiago | WhatsApp via Morning Dispatcher às 8h | EventBridge dispara morning_dispatcher.py |
| DLQ com mensagem | Sergio | WhatsApp + E-mail (SNS TechAlert → Notifier) | CloudWatch Alarm |

---

## Deploy — Opção 1: SAM (recomendado)

### Pré-requisitos
```bash
pip install aws-sam-cli
aws configure   # região: us-east-1
```

### Build e deploy
```bash
cd src/bot/infra

# Primeiro deploy (interativo — cria samconfig.toml)
sam build
sam deploy --guided \
  --parameter-overrides \
    Environment=dev \
    WhatsappToken=<token> \
    WhatsappPhoneId=<phone_id> \
    WhatsappAppSecret=<app_secret> \
    WebhookVerifyToken=<verify_token> \
    ThiagoPhone=<5511999999999> \
    SergioEmail=<email_sergio> \
    SergioPhone=<5511888888888> \
    GuardrailId=<guardrail_id>

# Deploys subsequentes (usa samconfig.toml)
sam build && sam deploy
```

### Deploy produção
```bash
sam build
sam deploy \
  --config-env prod \
  --parameter-overrides Environment=prod ...
```

### Rollback
```bash
# SAM usa CloudFormation — rollback automático em caso de falha
# Para rollback manual:
aws cloudformation rollback-stack --stack-name yorkshire-bot-dev
```

---

## Deploy — Opção 2: CLI (fallback se SAM falhar)

```bash
cd src/bot/infra

# Preencha as variáveis no topo do script
nano deploy-cli.sh

# Execute
chmod +x deploy-cli.sh
./deploy-cli.sh dev    # desenvolvimento
./deploy-cli.sh prod   # produção
```

### Erros comuns no CLI e soluções

**`EntityAlreadyExists` na role IAM**
```bash
# O script já trata isso — usa a role existente automaticamente
```

**`QueueAlreadyExists` no SQS**
```bash
# O script já trata isso — recupera a URL da fila existente
```

**`ResourceConflictException` no Lambda**
```bash
# O script já trata isso — faz update-function-code automaticamente
```

**Permissão negada no Bedrock**
```bash
# Habilitar modelo no console:
# AWS Console → Bedrock → Model access → anthropic.claude-sonnet-4-5 → Enable
```

---

## Variáveis de Ambiente

| Variável | Descrição | Onde obter |
|----------|-----------|-----------|
| `WHATSAPP_TOKEN` | Token de acesso permanente | Meta for Developers → WhatsApp → API Setup |
| `WHATSAPP_PHONE_ID` | ID do número de telefone | Meta for Developers → WhatsApp → API Setup |
| `WHATSAPP_APP_SECRET` | App Secret para validar webhook | Meta for Developers → App Settings → Basic |
| `WEBHOOK_VERIFY_TOKEN` | Token customizado para verificação | Você define (string aleatória segura) |
| `GUARDRAIL_ID` | ID do Bedrock Guardrail | AWS Console → Bedrock → Guardrails |
| `GUARDRAIL_VERSION` | Versão do guardrail | `DRAFT` em dev, número em prod |
| `TECH_SNS_TOPIC_ARN` | ARN do tópico SNS TechAlert (Sergio) | Gerado pelo template |
| `THIAGO_PHONE` | WhatsApp do Thiago para leads | Número com DDI: 5511999999999 |
| `SERGIO_PHONE` | WhatsApp do Sergio para alertas técnicos | Número com DDI: 5511888888888 |
| `SQS_QUEUE_URL` | URL da fila SQS FIFO | Gerado pelo template |

---

## DynamoDB — Estrutura da Tabela

**Tabela**: `yorkshire-bot-conversations-{env}`
**PK**: `phone` (string) — número do cliente
**SK**: `record_type` (string)

| record_type | Descrição | TTL |
|-------------|-----------|-----|
| `CONV` | Conversa ativa | 90 dias (LGPD) |
| `ARCHIVED` | Lead frio arquivado | 90 dias (LGPD) |
| `FOLLOWUP` | Follow-up agendado — SK dedicado, sobrevive ao archive_lead() | 90 dias (LGPD) |
| `MSGID#{id}` | Controle de idempotência | 24h |

**GSI `followup-index`**: PK=`record_type`, SK=`followup_ts` (Unix timestamp numérico)
- Permite query eficiente: "todos os follow-ups pendentes com followup_ts <= agora"
- Usado pelo Lambda de follow-up (Sprint 2) via EventBridge a cada hora
- `SK=FOLLOWUP` é independente de `CONV` e `ARCHIVED` — não é apagado pelo `archive_lead()`

---

## Segurança

### Camadas implementadas

1. **HMAC-SHA256** — valida `X-Hub-Signature-256` em todo POST do webhook
2. **Idempotência** — `message_id` salvo no DynamoDB, duplicatas ignoradas
3. **Sanitização regex** — 12 padrões de prompt injection/jailbreak
4. **Bedrock Guardrails** — content filter, topic denial, prompt attack detection
5. **System prompt hardened** — anti-drift, anti-roleplay, anti-exfiltration
6. **Rate limiting** — `MAX_INJECTION_ATTEMPTS = 3` → bloqueia + notifica
7. **TTL LGPD** — dados apagados automaticamente após 90 dias
8. **PII mascarado** — telefone mascarado em todos os logs CloudWatch
9. **SQS FIFO** — sem processamento duplicado mesmo com retry da Meta

### Criptografia
- **Em trânsito**: HTTPS/TLS 1.2+ em todos os endpoints
- **Em repouso**: SSE padrão DynamoDB (AES-256, chave AWS gerenciada) — sem custo adicional
- **Secrets**: variáveis sensíveis via `NoEcho` no SAM / nunca em código

---

## Monitoramento

### CloudWatch Logs
```bash
# Webhook
aws logs tail /aws/lambda/yorkshire-bot-webhook-dev --follow

# Processor
aws logs tail /aws/lambda/yorkshire-bot-processor-dev --follow

# Notifier
aws logs tail /aws/lambda/yorkshire-bot-notifier-dev --follow
```

### Verificar DLQ
```bash
aws sqs get-queue-attributes \
  --queue-url <DLQ_URL> \
  --attribute-names ApproximateNumberOfMessages
```

### Reprocessar mensagem da DLQ manualmente
```bash
# 1. Ler mensagem da DLQ
aws sqs receive-message --queue-url <DLQ_URL>

# 2. Reenviar para fila principal
aws sqs send-message \
  --queue-url <QUEUE_URL> \
  --message-body "<body_da_mensagem>" \
  --message-group-id "<phone>" \
  --message-deduplication-id "<novo_id_unico>"

# 3. Deletar da DLQ
aws sqs delete-message \
  --queue-url <DLQ_URL> \
  --receipt-handle "<receipt_handle>"
```

---

## Bedrock Guardrails — Configuração

Criar via console AWS → Bedrock → Guardrails → Create guardrail:

| Categoria | Configuração recomendada |
|-----------|------------------------|
| Content filters | HATE: HIGH, INSULTS: HIGH, SEXUAL: HIGH, VIOLENCE: MEDIUM |
| Denied topics | Concorrentes, política, religião, preços de outros canils |
| Word filters | Xingamentos em PT-BR |
| Grounding | Ativado — respostas baseadas no contexto |
| Prompt attacks | Ativado — detecta injection e jailbreak |

Após criar, copie o `Guardrail ID` e atualize `GUARDRAIL_ID` nas variáveis de ambiente.

---

## Sprint 2 — Pendências de Infraestrutura

- [ ] **Amazon Transcribe** — processar áudios do WhatsApp (OGG/Opus)
- [ ] **Amazon Comprehend** — análise de sentimento pré-Bedrock
- [ ] **S3 Bucket** — hospedar mídias (fotos dos filhotes) com URL pública
- [ ] **EventBridge Scheduler** — disparar follow-ups D+1 e D+30 via GSI followup-index
- [ ] **Lambda Follow-up** — enviar mensagens de reengajamento
- [ ] **CloudWatch Dashboard** — painel visual de métricas
- [ ] **Fine-tuning** — exportar conversas do DynamoDB para dataset

---

## Custos Estimados (dev — volume baixo)

| Serviço | Estimativa/mês |
|---------|---------------|
| Lambda (3 funções, ~1000 invocações/dia) | ~$0,00 (free tier) |
| SQS FIFO (~30k mensagens/mês) | ~$0,02 |
| DynamoDB On-Demand (~50k ops/mês) | ~$0,15 |
| Bedrock Claude Sonnet 4.5 (~500 conversas) | ~$8,00 |
| API Gateway HTTP API | ~$0,01 |
| CloudWatch Logs | ~$0,50 |
| **Total estimado dev** | **~$9/mês** |

> Produção com volume real de leads (~428/semana): estimar via [AWS Pricing Calculator](https://calculator.aws)
