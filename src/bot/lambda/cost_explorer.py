"""
cost_explorer.py — Custo AWS do bot Yorkshire
Bedrock: filtrado por serviço (não aceita tags de recurso)
Demais serviços: filtrados por tag Project=yorkshire-bot
"""
import json
import boto3
from datetime import date, timedelta

ce = boto3.client("ce", region_name="us-east-1")

BOT_SERVICES = [
    "Amazon Bedrock",
    "Amazon API Gateway",
    "AWS Lambda",
    "Amazon DynamoDB",
    "Amazon Simple Queue Service",
    "Amazon Simple Notification Service",
    "Amazon Simple Storage Service",
]


def lambda_handler(event, context):
    today = date.today()
    start = today.replace(day=1).isoformat()
    end   = today.isoformat()

    period_str = f"{today.strftime('%Y-%m-01')} → {today.isoformat()}"

    # Query 1 — serviços tagueados com Project=yorkshire-bot (exceto Bedrock)
    tagged = ce.get_cost_and_usage(
        TimePeriod={"Start": start, "End": end},
        Granularity="MONTHLY",
        Metrics=["BlendedCost"],
        Filter={"Tags": {"Key": "Project", "Values": ["yorkshire-bot"]}},
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
    )

    # Query 2 — Bedrock por dimensão (não tagueável)
    bedrock = ce.get_cost_and_usage(
        TimePeriod={"Start": start, "End": end},
        Granularity="MONTHLY",
        Metrics=["BlendedCost"],
        Filter={"Dimensions": {"Key": "SERVICE", "Values": ["Amazon Bedrock"]}},
    )

    services = {}

    # Processa serviços tagueados
    for group in (tagged["ResultsByTime"][0].get("Groups") or []):
        svc    = group["Keys"][0]
        amount = float(group["Metrics"]["BlendedCost"]["Amount"])
        if amount > 0:
            services[svc] = services.get(svc, 0) + amount

    # Adiciona Bedrock
    bedrock_amount = float(
        bedrock["ResultsByTime"][0]["Total"]["BlendedCost"]["Amount"]
    )
    if bedrock_amount > 0:
        services["Amazon Bedrock"] = services.get("Amazon Bedrock", 0) + bedrock_amount

    total = sum(services.values())

    services_list = sorted(
        [{"service": k, "amount": round(v, 4), "currency": "USD"} for k, v in services.items()],
        key=lambda x: x["amount"],
        reverse=True,
    )

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": json.dumps({
            "amount":   round(total, 4),
            "currency": "USD",
            "period":   period_str,
            "services": services_list,
        }),
    }
