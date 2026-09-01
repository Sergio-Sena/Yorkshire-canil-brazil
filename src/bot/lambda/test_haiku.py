import boto3, json, sys
sys.stdout.reconfigure(encoding='utf-8')

client = boto3.client('bedrock-runtime', region_name='us-east-1')

system_prompt = (
    'Voce e Bella, assistente do Yorkshire Canil Brazil. '
    'CRITICO: Responda EXCLUSIVAMENTE em JSON valido. Nunca inclua texto fora do JSON. '
    'FORMATO: {"message": "texto", "action": "reply|send_media", "lead_data": {"name": "", "city": "", "preference": "macho|femea|indefinido"}}. '
    'REGRA: Se tiver nome+cidade+preferencia, use send_media com preco de R$5.949 por R$4.949 + urgencia + escassez.'
)

resp = client.converse(
    modelId='us.anthropic.claude-haiku-4-5-20251001-v1:0',
    system=[{'text': system_prompt}],
    messages=[{'role': 'user', 'content': [{'text': 'Oi, quero comprar uma femea. Meu nome e Ana, sou de Sao Paulo.'}]}],
    inferenceConfig={'maxTokens': 512, 'temperature': 0.4}
)

raw = resp['output']['message']['content'][0]['text']
usage = resp.get('usage', {})

print("=== RESPOSTA RAW ===")
print(raw)
print("\n=== TOKENS ===")
print(f"input: {usage.get('inputTokens')} | output: {usage.get('outputTokens')} | cacheRead: {usage.get('cacheReadInputTokens')} | cacheWrite: {usage.get('cacheWriteInputTokens')}")
