# Contexto — Yorkshire Canil Brazil

Leia este arquivo antes de implementar qualquer mudança neste projeto.

---

## Sobre o Projeto

- **Cliente:** Yorkshire Canil Brazil — campeão nacional e sul-americano de Yorkshire Terrier
- **Gestor de tráfego:** Sergio Sena (senanetworker@gmail.com) — SS Technologies
- **Repositório:** `C:\Projetos Git\Yorkshire-canil-brazil`

### Dois focos principais:
1. **Landing page** — yorkshirecanilbrazil.com.br (GitHub Pages) em `src/`
2. **Bot de atendimento WhatsApp com IA** — em `src/bot/` (AWS Lambda + Bedrock + DynamoDB)

---

## Arquitetura do Bot

- **API Gateway** → Lambdas Python separados por responsabilidade:
  - `handler.py` — recebe mensagens do WhatsApp (webhook)
  - `processor.py` — processa mensagens e chama Bedrock
  - `bedrock.py` — integração com Claude (Anthropic) via AWS Bedrock
  - `prompt_manager.py` — CRUD do system prompt via SSM Parameter Store
  - `conversations_manager.py` — gerencia histórico de conversas
  - `morning_dispatcher.py` — dispara follow-ups matinais
  - `notifier.py` — notificações para o painel do Thiago
- **SSM Parameter Store (Advanced tier)** — armazena o system prompt (limite: 8.192 chars)
- **DynamoDB** — histórico de conversas e dados de leads
- **API Key:** `7e63f385192f40acb7b096d6cab74a13`
- **Endpoint bot:** `https://8x17umz5s7.execute-api.us-east-1.amazonaws.com/dev/`

### Endpoints disponíveis:
- `GET /prompt` — retorna prompt ativo + backup + metadados
- `PUT /prompt` — salva novo prompt (move atual para backup)
- `POST /prompt/rollback` — restaura backup
- `GET /conversations` — lista conversas
- `GET /conversations/{phone}` — histórico de uma conversa
- `GET /bot-cost` — custo do bot

---

## Prompt da Bella (bot)

- **Nome do bot:** Bella
- **Modelo:** Haiku 4.5 (`us.anthropic.claude-haiku-4-5-20251001-v1:0`)
- **Prompt:** armazenado no S3 com versionamento (6 versões) — rollback via `POST /prompt/rollback`
- **Frete:** incluso em todas as regiões, entrega pessoal
- **Desconto PIX:** até R$300 adicional (progressivo)
- **Parcelamento:** 1x-3x sem juros | 4x-7x +10% | 8x +11% | 9x +12% | 10x +13% | 11x +14% | 12x +15%

### Preços por região (ancoragem de/por)
| Região | Macho | Fêmea |
|---|---|---|
| SP capital + Grande SP | de R$4.949 por R$3.949 | de R$5.949 por R$4.949 |
| Interior SP | de R$6.449 por R$5.449 | de R$7.449 por R$6.449 |
| Outros estados | de R$7.990 por R$6.990 | de R$8.990 por R$7.990 |

### Regras críticas do prompt:
- Preço determinado pela cidade — perguntar sempre antes de apresentar valor
- Ancoragem de/por é intencional (técnica de vendas)
- NUNCA mencionar endereço exato do canil (localização declarada: Minas Gerais)
- NÃO avançar para preço sem ter nome + cidade + preferência
- Após enviar foto (send_media), SEMPRE incluir pergunta de avanço no "message"
- Fechamento (action `close`) SOMENTE com confirmação explícita do cliente

---

## Painel de Gestão

- **Painel Thiago** (`painel-thiago.html`) — atendimento e conversas do bot
- **Painel Google** (`painel-gestor.html`) — métricas Google Ads
- Hospedado via CloudFront + S3

---

## Gestão de Tarefas e Entregas

- Toda tarefa importante tem uma **Issue no GitHub** antes do código:
  - `correção` — bug fix
  - `melhoria` — aprimoramento existente
  - `nova função` — funcionalidade nova
- Todo **Pull Request** deve:
  - Mencionar a Issue (`Closes #N`)
  - Explicar o que mudou e por quê
  - Descrever como foi validado
  - Registrar riscos, limitações e próximos passos
- Branch `main` só recebe código após lint, testes e revisão aprovada

---

## Interface e UX

Toda interface deve ter:
- Skeleton screens durante carregamento
- Lazy loading onde fizer sentido
- Animações suaves de entrada/saída
- Feedback visual para ações do usuário
- Estados de progresso em elementos interativos
- Transições consistentes entre telas, cards e modais

Referência: https://github.com/kylezantos/design-principles

---

## Qualidade e Segurança

- Nunca commitar `.env` ou secrets — usar `.env.example`
- Rate limit em todas as APIs públicas
- Sem `console.log` desnecessário em produção
- Testes antes de qualquer deploy em produção
- Observabilidade: CloudWatch já configurado — Sentry recomendado para frontend

---

## Checklist antes de chamar de pronto

- [ ] Issue criada e referenciada no PR
- [ ] Lint passou
- [ ] Testes passando
- [ ] Sem secrets no código
- [ ] Interface revisada (skeleton, feedback, animações)
- [ ] Este arquivo atualizado se algo estrutural mudou

---

## Roadmap / Pendências

### Bot
- [ ] Testar pagamento, parcelamento, entrega e objeções
- [ ] Verificar token WhatsApp (erro 400 nos logs — pode estar expirado)
- [ ] Testes unitários nos Lambdas críticos (processor, bedrock)
- [ ] Sentry no frontend dos painéis

### Landing page
- [ ] Validar `renderVideoSection` no celular real
- [ ] Remover `lazyLoadVideos` (função morta no `main.js`)
- [ ] Logo definitiva, fotos reais, depoimentos reais
- [ ] Deploy final (Cloudflare Pages + domínio) + ativar SEO
- [ ] Configurar GA4 + Meta Pixel
