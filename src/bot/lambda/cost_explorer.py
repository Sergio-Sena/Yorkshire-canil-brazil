"""
cost_explorer.py — Custo mensal acumulado do bot
Endpoint: GET /bot-cost
Retorna custo do mês atual filtrado pela tag Project=yorkshire-bot.
Usado pelo card no painel-gestor.
"""

import json
import logging
import boto3
from datetime import date

logger = logging.getLogger()
logger.setLevel(logging.INFO)

_ce = boto3.client("ce", region_name="us-east-1")  # Cost Explorer só existe em us-east-1

_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json"
}


def lambda_handler(event, context):
    try:
        cost = _get_monthly_cost()
        return {
            "statusCode": 200,
            "headers": _HEADERS,
            "body": json.dumps(cost)
        }
    except Exception as e:
        logger.error(f"Erro ao buscar custo: {e}")
        return {
            "statusCode": 500,
            "headers": _HEADERS,
            "body": json.dumps({"error": str(e)})
        }


def _get_monthly_cost() -> dict:
    today = date.today()
    start = today.replace(day=1).isoformat()   # primeiro dia do mês
    end   = today.isoformat()                  # hoje

    # Se hoje é dia 1, start == end — Cost Explorer exige intervalo mínimo de 1 dia
    if start == end:
        return {"amount": 0.0, "currency": "USD", "period": start, "services": []}

    resp = _ce.get_cost_and_usage(
        TimePeriod={"Start": start, "End": end},
        Granularity="MONTHLY",
        Filter={
            "Tags": {
                "Key": "Project",
                "Values": ["yorkshire-bot"]
            }
        },
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
        Metrics=["UnblendedCost"]
    )

    results = resp.get("ResultsByTime", [{}])[0]
    groups  = results.get("Groups", [])

    services = [
        {
            "service": g["Keys"][0],
            "amount":  round(float(g["Metrics"]["UnblendedCost"]["Amount"]), 4),
            "currency": g["Metrics"]["UnblendedCost"]["Unit"]
        }
        for g in groups
        if float(g["Metrics"]["UnblendedCost"]["Amount"]) > 0
    ]

    total = round(sum(s["amount"] for s in services), 4)

    logger.info(f"Custo mensal bot | periodo={start}/{end} total={total} USD | servicos={len(services)}")

    return {
        "amount":   total,
        "currency": "USD",
        "period":   f"{start} → {end}",
        "services": services
    }
