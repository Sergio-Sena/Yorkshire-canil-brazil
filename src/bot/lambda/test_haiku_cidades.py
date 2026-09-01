import boto3, json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

s3 = boto3.client('s3', region_name='us-east-1')
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

resp = s3.get_object(Bucket='yorkshire-bot-prompts-dev-969430605054', Key='active/prompt.txt')
system_prompt = resp['Body'].read().decode('utf-8')

cenarios = [
    ("Cidade inequivoca - Regiao 1 (Guarulhos)",  "Oi, quero uma femea. Meu nome e Ana, sou de Guarulhos."),
    ("Cidade inequivoca - Regiao 2 (Campinas)",   "Oi, quero uma femea. Meu nome e Carlos, sou de Campinas."),
    ("Cidade inequivoca - Regiao 3 (Curitiba)",   "Oi, quero um macho. Meu nome e Pedro, sou de Curitiba."),
]

for titulo, mensagem in cenarios:
    print(f"=== {titulo} ===")
    print(f"Cliente: {mensagem}")
    resp = bedrock.converse(
        modelId='us.anthropic.claude-haiku-4-5-20251001-v1:0',
        system=[{'text': system_prompt}],
        messages=[{'role': 'user', 'content': [{'text': mensagem}]}],
        inferenceConfig={'maxTokens': 512, 'temperature': 0.4}
    )
    raw = resp['output']['message']['content'][0]['text']
    usage = resp.get('usage', {})
    try:
        match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', raw, re.DOTALL)
        parsed = json.loads(match.group(1) if match else raw.strip())
        print(f"action:    {parsed.get('action')}")
        print(f"message:   {parsed.get('message')}")
        print(f"lead_data: {parsed.get('lead_data')}")
    except Exception:
        print(f"raw: {raw}")
    print(f"tokens — input:{usage.get('inputTokens')} output:{usage.get('outputTokens')}\n")
