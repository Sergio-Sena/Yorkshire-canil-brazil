# Postagem Automática de Stories — Instagram Yorkshire Canil Brazil

**Status:** Planejamento
**Criado:** 2026
**Responsável:** Sergio Sena

---

## Objetivo

Postar automaticamente um vídeo por dia no Story do Instagram do Yorkshire Canil Brazil usando uma Lambda agendada via EventBridge. Stories somem após 24h — ciclo perfeito para manter presença diária sem esforço manual.

---

## Pré-requisitos

### 1. Conta Instagram conectada ao Business Manager (BM)
- Adicionar o perfil do Instagram do Yorkshire ao BM `Sergio Sena` (`882212698821548`)
- Caminho: Meta Business Suite → Configurações → Contas → Contas do Instagram → Adicionar
- A conta precisa ser **Instagram Business** ou **Creator** (não conta pessoal)

### 2. App Meta com permissões corretas
- Usar o app Meta já existente (mesmo que gera o token do WhatsApp/Meta Ads)
- Permissões necessárias:
  - `instagram_basic`
  - `instagram_content_publish`
  - `pages_read_engagement`
- Verificar se o app já tem essas permissões em: Meta for Developers → App → Permissões

### 3. Token de acesso
- Gerar um **Page Access Token** de longa duração (60 dias) via Graph API Explorer
- Armazenar no **Secrets Manager** AWS (mesmo padrão do bot WhatsApp)
- Chave sugerida: `yorkshire/instagram-token`
- Renovação: criar Lambda de refresh automático antes do vencimento (ver seção Gotchas)

### 4. Instagram User ID
- Buscar via: `GET https://graph.facebook.com/v21.0/me/accounts?access_token={token}`
- Pegar o `instagram_business_account.id` da página vinculada
- Salvar no Secrets Manager junto com o token

---

## Fluxo de Postagem (Story)

```
EventBridge (cron diário — ex: 09h BRT)
        ↓
Lambda story-dispatcher (Python)
        ↓
Busca próximo vídeo da fila (DynamoDB ou S3 manifest)
        ↓
Step 1 — Upload do container de mídia:
POST /v21.0/{ig-user-id}/media
  media_type=REELS ou VIDEO
  video_url={url pública S3}
  is_stories=true
        ↓
Aguarda processamento (polling ou sleep 30s)
GET /v21.0/{creation-id}?fields=status_code
        ↓
Step 2 — Publicar:
POST /v21.0/{ig-user-id}/media_publish
  creation_id={creation-id}
        ↓
Marca vídeo como postado no controle de fila
        ↓
Log no CloudWatch
```

---

## Estrutura de Arquivos

### Vídeos disponíveis (já existem no projeto)
```
src/videos/
├── emocoes-reais/    — 20 vídeos (campanha-01 a campanha-20)
├── famosos/          — 11 vídeos (celebridades com Yorkshire)
├── na tv/            — 9 vídeos (aparições em TV)
└── promocionais/     — 2 vídeos
```

Total: ~42 vídeos — suficiente para 6 semanas sem repetir.

### Controle de fila (DynamoDB)
Tabela: `yorkshire-stories-queue`

| Campo | Tipo | Descrição |
|---|---|---|
| `video_key` | String (PK) | Chave S3 do vídeo |
| `category` | String | emocoes / famosos / natv / promocional |
| `posted_at` | String | ISO timestamp da postagem |
| `status` | String | `pending` / `posted` / `error` |
| `ig_media_id` | String | ID retornado pela API após publicação |

### Lambda
```
src/bot/lambda/
└── story_dispatcher.py   ← novo arquivo
```

---

## Implementação — story_dispatcher.py (esboço)

```python
"""
story_dispatcher.py — Lambda acionada pelo EventBridge diariamente
Posta o próximo vídeo da fila como Story no Instagram.
"""
import boto3, requests, time, logging
from config import IG_USER_ID, IG_TOKEN, S3_BUCKET

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    video = get_next_video()
    if not video:
        logger.info("Fila vazia — nenhum story postado")
        return

    video_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{video['video_key']}"

    # Step 1: criar container
    r = requests.post(
        f"https://graph.facebook.com/v21.0/{IG_USER_ID}/media",
        params={
            "media_type": "REELS",
            "video_url": video_url,
            "is_stories": "true",
            "access_token": IG_TOKEN,
        }
    )
    creation_id = r.json()["id"]

    # Aguarda processamento (máx 2 min)
    for _ in range(8):
        time.sleep(15)
        status = requests.get(
            f"https://graph.facebook.com/v21.0/{creation_id}",
            params={"fields": "status_code", "access_token": IG_TOKEN}
        ).json().get("status_code")
        if status == "FINISHED":
            break

    # Step 2: publicar
    pub = requests.post(
        f"https://graph.facebook.com/v21.0/{IG_USER_ID}/media_publish",
        params={"creation_id": creation_id, "access_token": IG_TOKEN}
    )

    mark_as_posted(video["video_key"], pub.json().get("id"))
    logger.info(f"Story postado: {video['video_key']}")
```

---

## Infraestrutura AWS

| Recurso | Detalhe |
|---|---|
| Lambda | `yorkshire-story-dispatcher` — Python 3.12, timeout 3 min |
| EventBridge | Cron `0 12 * * ? *` (09h BRT = 12h UTC) |
| S3 | Bucket existente — vídeos em pasta `stories/` com ACL público-leitura |
| DynamoDB | Tabela `yorkshire-stories-queue` |
| Secrets Manager | `yorkshire/instagram-token` (token + ig_user_id) |
| CloudWatch | Logs automáticos da Lambda |

**Custo estimado:** < R$ 2/mês (Lambda + DynamoDB no free tier, S3 centavos)

---

## Gotchas e Decisões

### Token expira em 60 dias
- Criar Lambda `story-token-refresh` acionada 7 dias antes do vencimento
- Usa `GET /oauth/access_token?grant_type=fb_exchange_token` para renovar
- Atualiza o Secrets Manager automaticamente

### Vídeo precisa ser acessível publicamente
- Upload para S3 com URL pública temporária (pre-signed URL) ou pasta pública
- Alternativa: usar URL do CloudFront do site Yorkshire

### Formato aceito pela API
- MP4, MOV — codec H.264, áudio AAC
- Duração: 1s a 60s para Stories
- Os vídeos existentes em `src/videos/` precisam ser verificados (alguns podem ser longos demais)
- Usar ffmpeg para cortar/converter se necessário: `ffmpeg -i input.mp4 -t 60 -c copy output.mp4`

### Ordem de postagem
- Sugestão: rotacionar por categoria (1 emoção → 1 famoso → 1 TV → repeat)
- Evita monotonia no feed de stories

### Rate limit Meta
- Limite: 25 posts de mídia por 24h por conta — sem risco com 1 story/dia

---

## Passos para Executar

- [ ] **1.** Adicionar conta Instagram Yorkshire ao BM `882212698821548`
- [ ] **2.** Verificar/adicionar permissões `instagram_content_publish` no app Meta
- [ ] **3.** Gerar Page Access Token de longa duração e salvar no Secrets Manager
- [ ] **4.** Buscar e salvar o `ig_user_id` da conta
- [ ] **5.** Fazer upload dos vídeos para S3 (pasta `stories/`)
- [ ] **6.** Criar tabela DynamoDB `yorkshire-stories-queue` e popular com os vídeos
- [ ] **7.** Implementar `story_dispatcher.py`
- [ ] **8.** Criar Lambda + EventBridge no AWS Console (ou SAM — já temos `template.yaml`)
- [ ] **9.** Testar manualmente invocando a Lambda
- [ ] **10.** Ativar o agendamento

---

## Referências

- [Meta Graph API — Stories](https://developers.facebook.com/docs/instagram-api/guides/content-publishing#stories)
- [Instagram Content Publishing](https://developers.facebook.com/docs/instagram-api/guides/content-publishing)
- Bot WhatsApp existente: `src/bot/lambda/` — mesmo padrão de Lambda + Secrets Manager
