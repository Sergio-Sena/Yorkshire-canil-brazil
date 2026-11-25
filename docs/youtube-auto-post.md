# Upload Automático de Vídeos — YouTube Yorkshire Canil Brazil

**Status:** Planejamento
**Criado:** 24/11/2026
**Responsável:** Sergio Sena

---

## Objetivo

Fazer upload automático de vídeos no canal do YouTube do Yorkshire Canil Brazil usando uma Lambda agendada via EventBridge. O cliente envia os vídeos, o sistema publica automaticamente no ritmo definido (1 vídeo/dia ou conforme agenda).

---

## Diferenças em relação ao Instagram Stories

| Item | Instagram Stories | YouTube |
|---|---|---|
| API | Meta Graph API | YouTube Data API v3 |
| Auth | Page Access Token (60 dias) | OAuth2 (refresh token sem expiração) |
| Formato | Story (some em 24h) | Shorts ou vídeo normal (permanente) |
| Limite diário | 25 posts/24h | 6 uploads/dia (quota padrão) |
| Vídeos | Existentes no projeto | Cliente envia novos |
| Duração | Máx 60s | Shorts ≤60s / vídeos normais sem limite |

---

## Pré-requisitos

### 1. Canal YouTube conectado ao Google Cloud Project
- Criar projeto no Google Cloud Console (ou usar o existente do Google Ads)
- Ativar **YouTube Data API v3**
- Criar credenciais OAuth2 (tipo "Aplicativo da Web" ou "Aplicativo para computador")
- Autorizar o canal do Yorkshire uma vez via browser → gera `refresh_token` permanente
- Salvar `client_id`, `client_secret` e `refresh_token` no Secrets Manager AWS
  - Chave sugerida: `yorkshire/youtube-token`

### 2. Canal YouTube do Yorkshire
- Confirmar que o Thiago tem acesso de proprietário ao canal
- O canal precisa estar verificado para uploads sem limite de duração
- Confirmar se quer publicar como **Shorts** (≤60s, vertical) ou **vídeos normais**

### 3. Vídeos do cliente
- Thiago envia os vídeos via WhatsApp ou link
- Sergio faz upload para S3 na pasta `youtube/pending/`
- Sistema processa na ordem de chegada

---

## Fluxo de Postagem

```
EventBridge (cron diário — ex: 09h BRT)
        ↓
Lambda youtube-dispatcher (Python)
        ↓
Busca próximo vídeo com status=pending no DynamoDB
        ↓
Baixa vídeo do S3
        ↓
Autentica via OAuth2 (refresh_token → access_token)
        ↓
POST /upload/youtube/v3/videos
  part=snippet,status
  title, description, tags, categoryId
  privacyStatus=public
        ↓
Marca vídeo como postado no DynamoDB
        ↓
Log no CloudWatch
```

---

## Estrutura de Arquivos

### Vídeos no S3
```
s3://sstech-cdn-unified/yorkshire/youtube/
├── pending/    ← vídeos aguardando upload
└── posted/     ← vídeos já publicados (movidos após upload)
```

### Controle de fila (DynamoDB)
Tabela: `yorkshire-youtube-queue`

| Campo | Tipo | Descrição |
|---|---|---|
| `video_key` | String (PK) | Chave S3 do vídeo |
| `title` | String | Título do vídeo no YouTube |
| `description` | String | Descrição com hashtags |
| `tags` | List | Tags para SEO |
| `posted_at` | String | ISO timestamp da postagem |
| `status` | String | `pending` / `posted` / `error` |
| `youtube_video_id` | String | ID retornado pela API após upload |

### Lambda
```
src/bot/lambda/
└── youtube_dispatcher.py   ← novo arquivo
```

---

## Implementação — youtube_dispatcher.py (esboço)

```python
"""
youtube_dispatcher.py — Lambda acionada pelo EventBridge diariamente
Faz upload do próximo vídeo da fila para o YouTube.
"""
import boto3, logging, tempfile, os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_credentials():
    sm = boto3.client('secretsmanager')
    secret = sm.get_secret_value(SecretId='yorkshire/youtube-token')['SecretString']
    import json; s = json.loads(secret)
    creds = Credentials(
        token=None,
        refresh_token=s['refresh_token'],
        client_id=s['client_id'],
        client_secret=s['client_secret'],
        token_uri='https://oauth2.googleapis.com/token'
    )
    creds.refresh(Request())
    return creds

def lambda_handler(event, context):
    video = get_next_video()  # busca no DynamoDB status=pending
    if not video:
        logger.info("Fila vazia — nenhum vídeo postado")
        return

    # Baixa vídeo do S3 para /tmp
    s3 = boto3.client('s3')
    tmp_path = f"/tmp/{os.path.basename(video['video_key'])}"
    s3.download_file('sstech-cdn-unified', video['video_key'], tmp_path)

    # Autentica e faz upload
    creds = get_credentials()
    youtube = build('youtube', 'v3', credentials=creds)

    body = {
        'snippet': {
            'title': video['title'],
            'description': video['description'],
            'tags': video.get('tags', ['yorkshire', 'yorkshireterrier', 'filhote']),
            'categoryId': '15'  # Pets & Animals
        },
        'status': {'privacyStatus': 'public'}
    }

    media = MediaFileUpload(tmp_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
    response = request.execute()

    mark_as_posted(video['video_key'], response['id'])
    logger.info(f"Vídeo publicado: {response['id']}")
```

---

## Infraestrutura AWS

| Recurso | Detalhe |
|---|---|
| Lambda | `yorkshire-youtube-dispatcher` — Python 3.12, timeout 15 min (upload pode demorar) |
| EventBridge | Cron `0 12 * * ? *` (09h BRT = 12h UTC) |
| S3 | Bucket `sstech-cdn-unified` — pasta `yorkshire/youtube/pending/` |
| DynamoDB | Tabela `yorkshire-youtube-queue` |
| Secrets Manager | `yorkshire/youtube-token` (refresh_token + client_id + client_secret) |
| CloudWatch | Logs automáticos da Lambda |
| Lambda Layer | `google-api-python-client` + `google-auth` (não estão no runtime padrão) |

**Custo estimado:** < R$ 5/mês (Lambda timeout maior + S3 storage dos vídeos)

---

## Gotchas e Decisões

### Quota da YouTube Data API
- Quota padrão: **10.000 unidades/dia**
- Upload de vídeo custa **1.600 unidades** — comporta ~6 uploads/dia
- 1 upload/dia está bem dentro do limite
- Se precisar de mais: solicitar aumento de quota no Google Cloud Console

### Lambda Layer obrigatória
- `google-api-python-client` e `google-auth` não estão no runtime Python da Lambda
- Criar layer com: `pip install google-api-python-client google-auth -t python/`
- Zipar e publicar como Lambda Layer

### Timeout da Lambda
- Upload de vídeo pode levar 2-10 min dependendo do tamanho
- Configurar timeout para **15 minutos** (máximo da Lambda)
- Para vídeos muito grandes (>500MB): usar upload resumable (já no esboço)

### Formato dos vídeos
- YouTube aceita: MP4, MOV, AVI, MKV
- Para Shorts: vertical (9:16), ≤60s, adicionar `#Shorts` no título ou descrição
- Para vídeos normais: qualquer proporção, qualquer duração

### Título e descrição
- Definir template padrão com o Thiago
- Sugestão: título = "Yorkshire Canil Brazil — {categoria}" + data
- Descrição = bio do canil + link do site + WhatsApp + hashtags

### Autenticação OAuth2
- Diferente do Instagram, o refresh_token do YouTube **não expira** (enquanto não revogar)
- Não precisa de Lambda de renovação automática
- Único cuidado: não revogar o acesso no Google Account

---

## Passos para Executar

- [ ] **1.** Confirmar com Thiago: Shorts (≤60s vertical) ou vídeos normais?
- [ ] **2.** Confirmar canal YouTube do Yorkshire (URL/handle)
- [ ] **3.** Criar projeto Google Cloud + ativar YouTube Data API v3
- [ ] **4.** Gerar credenciais OAuth2 + autorizar canal → salvar refresh_token no Secrets Manager
- [ ] **5.** Criar tabela DynamoDB `yorkshire-youtube-queue`
- [ ] **6.** Criar Lambda Layer com `google-api-python-client` + `google-auth`
- [ ] **7.** Implementar `youtube_dispatcher.py`
- [ ] **8.** Criar Lambda `yorkshire-youtube-dispatcher` + EventBridge
- [ ] **9.** Thiago envia primeiros vídeos → Sergio faz upload para S3 + popula DynamoDB
- [ ] **10.** Testar manualmente invocando a Lambda
- [ ] **11.** Ativar agendamento

---

## Referências

- [YouTube Data API v3 — Videos.insert](https://developers.google.com/youtube/v3/docs/videos/insert)
- [Google OAuth2 para Lambda](https://google-auth.readthedocs.io/en/master/)
- Padrão Instagram Stories: `docs/instagram-stories-auto-post.md`
- Bot WhatsApp existente: `src/bot/lambda/` — mesmo padrão de Lambda + Secrets Manager
