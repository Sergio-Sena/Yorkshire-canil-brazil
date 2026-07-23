#!/bin/bash
# =============================================================================
# deploy-cli.sh — Fallback CLI para quando o SAM template falhar
# Yorkshire Canil Brazil — Bot IA WhatsApp
#
# USO:
#   chmod +x deploy-cli.sh
#   ./deploy-cli.sh dev    # ambiente de desenvolvimento
#   ./deploy-cli.sh prod   # produção
#
# PRÉ-REQUISITOS:
#   - AWS CLI v2 configurado (aws configure)
#   - Python 3.12
#   - Permissões: Lambda, SQS, DynamoDB, SNS, CloudWatch, IAM, API Gateway, EventBridge
# =============================================================================

set -euo pipefail  # para em qualquer erro

ENV=${1:-dev}
REGION="us-east-1"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
PREFIX="yorkshire-bot"

echo "============================================="
echo " Yorkshire Bot — Deploy CLI"
echo " Ambiente : $ENV"
echo " Região   : $REGION"
echo " Conta    : $ACCOUNT_ID"
echo "============================================="

# ── Variáveis — preencha antes de executar ────────────────────────────────────
WHATSAPP_TOKEN=""
WHATSAPP_PHONE_ID=""
WHATSAPP_APP_SECRET=""
WEBHOOK_VERIFY_TOKEN=""
THIAGO_PHONE=""          # ex: 5511999999999
SERGIO_PHONE=""          # ex: 5511888888888
SERGIO_EMAIL=""
GUARDRAIL_ID=""

if [[ -z "$WHATSAPP_TOKEN" || -z "$THIAGO_PHONE" || -z "$SERGIO_EMAIL" ]]; then
  echo "ERRO: Preencha WHATSAPP_TOKEN, THIAGO_PHONE e SERGIO_EMAIL antes de executar."
  exit 1
fi

# ── Nomes dos recursos ────────────────────────────────────────────────────────
TABLE_NAME="${PREFIX}-conversations-${ENV}"
DLQ_NAME="${PREFIX}-dlq-${ENV}.fifo"
QUEUE_NAME="${PREFIX}-messages-${ENV}.fifo"
SNS_NAME="${PREFIX}-alerts-${ENV}"
WEBHOOK_FN="${PREFIX}-webhook-${ENV}"
PROCESSOR_FN="${PREFIX}-processor-${ENV}"
MORNING_FN="${PREFIX}-morning-dispatcher-${ENV}"
NOTIFIER_FN="${PREFIX}-notifier-${ENV}"
ROLE_NAME="${PREFIX}-lambda-role-${ENV}"
LAYER_NAME="${PREFIX}-deps-${ENV}"

echo ""
echo "[ 1/10 ] Criando role IAM para as Lambdas..."
ROLE_ARN=$(aws iam create-role \
  --role-name "$ROLE_NAME" \
  --assume-role-policy-document '{
    "Version":"2012-10-17",
    "Statement":[{
      "Effect":"Allow",
      "Principal":{"Service":"lambda.amazonaws.com"},
      "Action":"sts:AssumeRole"
    }]
  }' \
  --query Role.Arn --output text 2>/dev/null || \
  aws iam get-role --role-name "$ROLE_NAME" --query Role.Arn --output text)

# Políticas gerenciadas
aws iam attach-role-policy --role-name "$ROLE_NAME" \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam attach-role-policy --role-name "$ROLE_NAME" \
  --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess

aws iam attach-role-policy --role-name "$ROLE_NAME" \
  --policy-arn arn:aws:iam::aws:policy/AmazonSQSFullAccess

aws iam attach-role-policy --role-name "$ROLE_NAME" \
  --policy-arn arn:aws:iam::aws:policy/AmazonSNSFullAccess

aws iam attach-role-policy --role-name "$ROLE_NAME" \
  --policy-arn arn:aws:iam::aws:policy/AmazonEventBridgeFullAccess

# Política inline para Bedrock
aws iam put-role-policy --role-name "$ROLE_NAME" \
  --policy-name BedrockInvokePolicy \
  --policy-document '{
    "Version":"2012-10-17",
    "Statement":[{
      "Effect":"Allow",
      "Action":["bedrock:InvokeModel","bedrock:ApplyGuardrail"],
      "Resource":"*"
    }]
  }'

echo "   Role ARN: $ROLE_ARN"
echo "   Aguardando propagação da role (10s)..."
sleep 10

# ── DynamoDB ──────────────────────────────────────────────────────────────────
echo ""
echo "[ 2/10 ] Criando tabela DynamoDB..."
aws dynamodb create-table \
  --table-name "$TABLE_NAME" \
  --attribute-definitions \
    AttributeName=phone,AttributeType=S \
    AttributeName=record_type,AttributeType=S \
  --key-schema \
    AttributeName=phone,KeyType=HASH \
    AttributeName=record_type,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST \
  --region "$REGION" 2>/dev/null || echo "   Tabela já existe — pulando."

# TTL
aws dynamodb update-time-to-live \
  --table-name "$TABLE_NAME" \
  --time-to-live-specification "Enabled=true,AttributeName=ttl" \
  --region "$REGION" 2>/dev/null || true

# Point-in-time recovery
aws dynamodb update-continuous-backups \
  --table-name "$TABLE_NAME" \
  --point-in-time-recovery-specification PointInTimeRecoveryEnabled=true \
  --region "$REGION" 2>/dev/null || true

echo "   Tabela: $TABLE_NAME"

# ── SQS DLQ ───────────────────────────────────────────────────────────────────
echo ""
echo "[ 3/10 ] Criando Dead Letter Queue (FIFO)..."
DLQ_URL=$(aws sqs create-queue \
  --queue-name "$DLQ_NAME" \
  --attributes FifoQueue=true,MessageRetentionPeriod=86400 \
  --region "$REGION" \
  --query QueueUrl --output text 2>/dev/null || \
  aws sqs get-queue-url --queue-name "$DLQ_NAME" --region "$REGION" --query QueueUrl --output text)

DLQ_ARN=$(aws sqs get-queue-attributes \
  --queue-url "$DLQ_URL" \
  --attribute-names QueueArn \
  --query Attributes.QueueArn --output text)

echo "   DLQ URL: $DLQ_URL"

# ── SQS Fila principal ────────────────────────────────────────────────────────
echo ""
echo "[ 4/10 ] Criando fila SQS FIFO principal..."
QUEUE_URL=$(aws sqs create-queue \
  --queue-name "$QUEUE_NAME" \
  --attributes \
    FifoQueue=true \
    ContentBasedDeduplication=false \
    VisibilityTimeout=90 \
    MessageRetentionPeriod=3600 \
    RedrivePolicy="{\"deadLetterTargetArn\":\"$DLQ_ARN\",\"maxReceiveCount\":\"3\"}" \
  --region "$REGION" \
  --query QueueUrl --output text 2>/dev/null || \
  aws sqs get-queue-url --queue-name "$QUEUE_NAME" --region "$REGION" --query QueueUrl --output text)

QUEUE_ARN=$(aws sqs get-queue-attributes \
  --queue-url "$QUEUE_URL" \
  --attribute-names QueueArn \
  --query Attributes.QueueArn --output text)

echo "   Queue URL: $QUEUE_URL"

# ── SNS ───────────────────────────────────────────────────────────────────────
echo ""
echo "[ 5/10 ] Criando tópico SNS TechAlert (Sergio) e inscrevendo e-mail..."
SNS_ARN=$(aws sns create-topic \
  --name "$SNS_NAME" \
  --region "$REGION" \
  --query TopicArn --output text)

aws sns subscribe \
  --topic-arn "$SNS_ARN" \
  --protocol email \
  --notification-endpoint "$SERGIO_EMAIL" \
  --region "$REGION" > /dev/null

echo "   SNS ARN: $SNS_ARN"
echo "   ⚠️  Confirme a inscrição no e-mail: $SERGIO_EMAIL"

# ── Lambda Layer ──────────────────────────────────────────────────────────────
echo ""
echo "[ 6/10 ] Empacotando e publicando Lambda Layer..."
cd ../lambda
pip install -r requirements.txt -t /tmp/layer/python --quiet
cd /tmp/layer && zip -r /tmp/layer.zip python --quiet
cd - > /dev/null

LAYER_ARN=$(aws lambda publish-layer-version \
  --layer-name "$LAYER_NAME" \
  --zip-file fileb:///tmp/layer.zip \
  --compatible-runtimes python3.12 \
  --region "$REGION" \
  --query LayerVersionArn --output text)

echo "   Layer ARN: $LAYER_ARN"

# ── Empacotar código Lambda ───────────────────────────────────────────────────
echo ""
echo "[ 7/10 ] Empacotando código Lambda..."
cd ../lambda
zip -r /tmp/lambda.zip \
  handler.py processor.py whatsapp.py dynamodb.py bedrock.py config.py \
  morning_dispatcher.py notifier.py \
  --quiet
cd - > /dev/null

ENV_VARS="Variables={\
AWS_REGION_NAME=$REGION,\
DYNAMODB_TABLE=$TABLE_NAME,\
TECH_SNS_TOPIC_ARN=$SNS_ARN,\
SQS_QUEUE_URL=$QUEUE_URL,\
BEDROCK_MODEL_ID=anthropic.claude-sonnet-4-5,\
GUARDRAIL_ID=$GUARDRAIL_ID,\
GUARDRAIL_VERSION=DRAFT,\
WHATSAPP_TOKEN=$WHATSAPP_TOKEN,\
WHATSAPP_PHONE_ID=$WHATSAPP_PHONE_ID,\
WHATSAPP_APP_SECRET=$WHATSAPP_APP_SECRET,\
WEBHOOK_VERIFY_TOKEN=$WEBHOOK_VERIFY_TOKEN,\
THIAGO_PHONE=$THIAGO_PHONE,\
SERGIO_PHONE=$SERGIO_PHONE}"

# ── Lambda Webhook ────────────────────────────────────────────────────────────
echo ""
echo "[ 8/10 ] Criando Lambdas..."

# Webhook
aws lambda create-function \
  --function-name "$WEBHOOK_FN" \
  --runtime python3.12 \
  --architectures arm64 \
  --role "$ROLE_ARN" \
  --handler handler.lambda_handler \
  --zip-file fileb:///tmp/lambda.zip \
  --timeout 10 \
  --memory-size 256 \
  --layers "$LAYER_ARN" \
  --environment "$ENV_VARS" \
  --region "$REGION" 2>/dev/null || \
aws lambda update-function-code \
  --function-name "$WEBHOOK_FN" \
  --zip-file fileb:///tmp/lambda.zip \
  --region "$REGION" > /dev/null

# Processor
aws lambda create-function \
  --function-name "$PROCESSOR_FN" \
  --runtime python3.12 \
  --architectures arm64 \
  --role "$ROLE_ARN" \
  --handler processor.lambda_handler \
  --zip-file fileb:///tmp/lambda.zip \
  --timeout 60 \
  --memory-size 256 \
  --layers "$LAYER_ARN" \
  --environment "$ENV_VARS" \
  --region "$REGION" 2>/dev/null || \
aws lambda update-function-code \
  --function-name "$PROCESSOR_FN" \
  --zip-file fileb:///tmp/lambda.zip \
  --region "$REGION" > /dev/null

# Trigger SQS → Processor
aws lambda create-event-source-mapping \
  --function-name "$PROCESSOR_FN" \
  --event-source-arn "$QUEUE_ARN" \
  --batch-size 1 \
  --function-response-types ReportBatchItemFailures \
  --region "$REGION" 2>/dev/null || echo "   Trigger SQS já existe — pulando."

# Morning Dispatcher
aws lambda create-function \
  --function-name "$MORNING_FN" \
  --runtime python3.12 \
  --architectures arm64 \
  --role "$ROLE_ARN" \
  --handler morning_dispatcher.lambda_handler \
  --zip-file fileb:///tmp/lambda.zip \
  --timeout 60 \
  --memory-size 256 \
  --layers "$LAYER_ARN" \
  --environment "$ENV_VARS" \
  --region "$REGION" 2>/dev/null || \
aws lambda update-function-code \
  --function-name "$MORNING_FN" \
  --zip-file fileb:///tmp/lambda.zip \
  --region "$REGION" > /dev/null

# Notifier
aws lambda create-function \
  --function-name "$NOTIFIER_FN" \
  --runtime python3.12 \
  --architectures arm64 \
  --role "$ROLE_ARN" \
  --handler notifier.lambda_handler \
  --zip-file fileb:///tmp/lambda.zip \
  --timeout 30 \
  --memory-size 128 \
  --layers "$LAYER_ARN" \
  --environment "$ENV_VARS" \
  --region "$REGION" 2>/dev/null || \
aws lambda update-function-code \
  --function-name "$NOTIFIER_FN" \
  --zip-file fileb:///tmp/lambda.zip \
  --region "$REGION" > /dev/null

# Inscreve Notifier no SNS TechAlert
NOTIFIER_ARN=$(aws lambda get-function --function-name "$NOTIFIER_FN" --region "$REGION" --query Configuration.FunctionArn --output text)
aws sns subscribe \
  --topic-arn "$SNS_ARN" \
  --protocol lambda \
  --notification-endpoint "$NOTIFIER_ARN" \
  --region "$REGION" > /dev/null 2>/dev/null || true
aws lambda add-permission \
  --function-name "$NOTIFIER_FN" \
  --statement-id sns-invoke \
  --action lambda:InvokeFunction \
  --principal sns.amazonaws.com \
  --source-arn "$SNS_ARN" \
  --region "$REGION" 2>/dev/null || true

echo "[ 9/10 ] Criando regra EventBridge para Morning Dispatcher (8h BRT)..."
MORNING_ARN=$(aws lambda get-function --function-name "$MORNING_FN" --region "$REGION" --query Configuration.FunctionArn --output text)
RULE_ARN=$(aws events put-rule \
  --name "${PREFIX}-morning-dispatch-${ENV}" \
  --schedule-expression "cron(0 11 * * ? *)" \
  --state ENABLED \
  --region "$REGION" \
  --query RuleArn --output text)
aws events put-targets \
  --rule "${PREFIX}-morning-dispatch-${ENV}" \
  --targets "Id=MorningDispatcher,Arn=$MORNING_ARN" \
  --region "$REGION" > /dev/null
aws lambda add-permission \
  --function-name "$MORNING_FN" \
  --statement-id eventbridge-invoke \
  --action lambda:InvokeFunction \
  --principal events.amazonaws.com \
  --source-arn "$RULE_ARN" \
  --region "$REGION" 2>/dev/null || true

echo "   Webhook           : $WEBHOOK_FN"
echo "   Processor         : $PROCESSOR_FN"
echo "   Morning Dispatcher: $MORNING_FN"
echo "   Notifier          : $NOTIFIER_FN"

# ── CloudWatch Alarm ──────────────────────────────────────────────────────────
echo ""
echo "[ 10/10 ] Criando alarme CloudWatch para DLQ..."
aws cloudwatch put-metric-alarm \
  --alarm-name "${PREFIX}-dlq-alarm-${ENV}" \
  --alarm-description "Mensagem na DLQ — processamento falhou 3 vezes" \
  --namespace AWS/SQS \
  --metric-name ApproximateNumberOfMessagesVisible \
  --dimensions Name=QueueName,Value="$DLQ_NAME" \
  --statistic Sum \
  --period 60 \
  --evaluation-periods 1 \
  --threshold 1 \
  --comparison-operator GreaterThanOrEqualToThreshold \
  --alarm-actions "$SNS_ARN" \
  --treat-missing-data notBreaching \
  --region "$REGION"

# ── Resumo final ──────────────────────────────────────────────────────────────
echo ""
echo "============================================="
echo " Deploy concluído!"
echo "============================================="
echo ""
echo " Próximos passos:"
echo " 1. Confirme o e-mail de inscrição SNS ($SERGIO_EMAIL)"
echo " 2. Configure a URL do webhook no Meta for Developers:"

WEBHOOK_FN_URL=$(aws lambda get-function-url-config \
  --function-name "$WEBHOOK_FN" \
  --region "$REGION" \
  --query FunctionUrl --output text 2>/dev/null || echo "  (configure API Gateway manualmente)")

echo "    $WEBHOOK_FN_URL/webhook"
echo ""
echo " Recursos criados:"
echo "  DynamoDB : $TABLE_NAME"
echo "  SQS      : $QUEUE_URL"
echo "  DLQ      : $DLQ_URL"
echo "  SNS TechAlert : $SNS_ARN"
echo "  Lambda Webhook: $WEBHOOK_FN"
echo "  Lambda Proc   : $PROCESSOR_FN"
echo "  Lambda Morning: $MORNING_FN"
echo "  Lambda Notifier: $NOTIFIER_FN"
echo "  Layer         : $LAYER_ARN"
