import sys, traceback, json
sys.path.insert(0, '.')
try:
    from bedrock import generate_response
    result = generate_response(
        phone='5511984969596',
        message='Sergio, Sao Paulo, femea, quero ver as fotos',
        history=[],
        lead_data={}
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
except Exception as e:
    traceback.print_exc()
