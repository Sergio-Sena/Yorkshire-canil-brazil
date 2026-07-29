import boto3, time

client = boto3.client("logs", region_name="us-east-1")
start = int(time.time() * 1000) - 10 * 60 * 1000

for pattern in ["Claude action", "Enviando galeria", "media.json", "WhatsApp API", "ERROR"]:
    resp = client.filter_log_events(
        logGroupName="/aws/lambda/yorkshire-bot-processor-dev",
        startTime=start,
        filterPattern=pattern
    )
    for e in resp.get("events", []):
        print(e["message"].encode("ascii", "replace").decode())
