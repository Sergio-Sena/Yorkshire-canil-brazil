import boto3

client = boto3.client("dynamodb", region_name="us-east-1")
table = "yorkshire-bot-conversations-dev"

resp = client.scan(TableName=table, ProjectionExpression="phone, record_type")
items = resp.get("Items", [])

for item in items:
    client.delete_item(
        TableName=table,
        Key={"phone": item["phone"], "record_type": item["record_type"]}
    )
    print(f"Deletado: {item['phone']['S']} | {item['record_type']['S']}")

print(f"\nTotal deletado: {len(items)} itens")
