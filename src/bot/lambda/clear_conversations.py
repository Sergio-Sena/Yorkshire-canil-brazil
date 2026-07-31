"""
clear_conversations.py — Apaga conversas do DynamoDB por número
Uso:
  python clear_conversations.py 5511982699596
  python clear_conversations.py 5511982699596 5511960197657
  python clear_conversations.py --all   (apaga TUDO — cuidado em prod)
"""

import sys
import boto3
from boto3.dynamodb.conditions import Attr

TABLE  = "yorkshire-bot-conversations-dev"
REGION = "us-east-1"

_dynamodb = boto3.resource("dynamodb", region_name=REGION)
_table    = _dynamodb.Table(TABLE)

SKS = ("CONV", "ARCHIVED", "FOLLOWUP")


def delete_phone(phone: str):
    for sk in SKS:
        _table.delete_item(Key={"phone": phone, "record_type": sk})
    print(f"✅ Apagado: {phone}")


def delete_all():
    confirm = input("⚠️  Apagar TODAS as conversas? Digite 'sim' para confirmar: ")
    if confirm.strip().lower() != "sim":
        print("Cancelado.")
        return

    resp = _table.scan(ProjectionExpression="phone, record_type")
    items = resp.get("Items", [])
    for item in items:
        _table.delete_item(Key={"phone": item["phone"], "record_type": item["record_type"]})
    print(f"✅ {len(items)} registros apagados.")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Uso: python clear_conversations.py <numero> [<numero2> ...] | --all")
        sys.exit(1)

    if args[0] == "--all":
        delete_all()
    else:
        for phone in args:
            delete_phone(phone)
