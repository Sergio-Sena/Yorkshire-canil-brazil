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
- **Preços:** Macho R$3.949 / Fêmea R$4.949 — ÚNICOS para todo o Brasil
- **Frete:** incluso para qualquer cidade, incluindo toda a Grande SP
- **Desconto PIX:** até R$300 adicional (progressivo)
- **Parcelamento:** 1x-3x sem juros | 4x-7x +10% | 8x +11% | 9x +12% | 10x +13% | 11x +14% | 12x +15%
- **Limite SSM:** 8.192 chars — manter prompt abaixo de 7.500 chars para ter margem

### Regras críticas do prompt:
- NUNCA ajustar preço por região — preço é único nacional
- NUNCA mencionar custo extra de frete para nenhuma cidade
- NÃO avançar para preço sem ter o nome do cliente
- Após enviar foto (send_media), SEMPRE incluir pergunta de avanço no "message"

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

- [ ] Migrar prompt para S3 (eliminar limite de 8.192 chars do SSM)
- [ ] Implementar estrutura de preços por região (Thiago/GOB)
- [ ] Sentry no frontend dos painéis
- [ ] Testes unitários nos Lambdas críticos (processor, bedrock)
