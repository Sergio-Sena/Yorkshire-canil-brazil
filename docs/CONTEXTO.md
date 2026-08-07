# 📋 Contexto do Projeto — Yorkshire Canil Brazil

> Leia este arquivo primeiro para ter contexto completo antes de qualquer tarefa.

---

## 👤 Cliente

- **Nome**: Yorkshire Canil Brazil
- **Dono**: Thiago (yorkshirecanil@...)
- **Produto**: Filhotes de Yorkshire Terrier — ticket R$3.000–5.000
- **Sites**: yorkshirecanilbrazil.com (Wix) e yorkshirecanilbrazil.com.br (GitHub Pages — este projeto)
- **WhatsApp**: 5511977118201

---

## 👨‍💻 Gestor

- **Nome**: Sergio Sena (senanetworker@gmail.com)
- **Empresa**: SS Technologies / SS Gestão de Tráfego
- **Agência Google Ads**: GOB Marketing (Matheus + Barbara Passos)
- **MCC**: Ss technologies ltda — 967-971-4188

---

## 🎯 Projetos Ativos

### 1. Google Ads (em produção)
- 3 campanhas: .COM Search, .COM.BR Search, Performance Max
- Budget: ~R$7.200/mês total
- Lambda: `ss-google-ads-yorkshire` (us-east-1)
- API: `https://q29d294f74.execute-api.us-east-1.amazonaws.com/google-ads/yorkshire`
- Painel: `https://sstrafegopago.sstechnologies-cloud.com/painel-gestor.html`
- Token renovação: `npm run renew:token` no projeto SS-Gestao-de-Trafego

### 2. Bot de Atendimento WhatsApp ✅ Sprint 2 concluído
- **Status**: End-to-end validado com número real (`9176`)
- **Objetivo**: Substituir bot engessado (R$200/mês, opções 1/2/3) por bot com IA
- **Infraestrutura**: AWS (roda em nuvem — não trava celular)
- **Número bot**: `9176` — Phone Number ID `1209550188914168` (em uso)
- **Número suporte Sergio**: `5511982699176`
- **Número testes**: `9596` (Sergio pessoal)
- **Guardrail**: `l2sg39cfds01` versão 7 — tópicos: política, religião, concorrentes
- **Preços**: por estado do cliente (`PRICE_TIER_BY_STATE`) — SP: R$3.949/R$4.949
- **Localização declarada**: SP → "Minas Gerais", outros → "São Paulo" (dissuadir retirada)
- **Notificações**: Bot avisa Thiago via `https://wa.me/{phone}` (link clicável) quando precisar de intervenção
- **Sinal de 30%**: removido do fluxo da Bella e da notificação ao Thiago
- **Conhecimento técnico**: micro/mini/toy (não reconhecido), Goldust (sem FCI), microchip, tamanho adulto
- **Bot antigo**: mensagem de encerramento ignorada (fix loop)
- **Docs**: `docs/IA DE ATENDIMENTO - WATTSUP.md`, `docs/chatbot-ia-arquitetura.md`, `docs/proposta-chatbot-ia-cliente.md`

#### 🔧 Números WhatsApp
| Número | Descrição |
|--------|----------|
| `5511982699176` | Número bot dev (Sergio) — `Phone Number ID: 1219655164565164` |
| `5511984969596` | Número testes (Sergio pessoal) |
| `5511960197657` | Chip do Thiago — candidato a número de produção do bot |
| Variável | Valor |
|----------|-------|
| `WHATSAPP_PHONE_ID` | `1219655164565164` |
| `GUARDRAIL_ID` | `l2sg39cfds01` |
| `GUARDRAIL_VERSION` | `5` |
| `DYNAMODB_TABLE` | `yorkshire-bot-conversations-dev` |
| `THIAGO_PHONE` | `5511977119176` |
| `BEDROCK_MODEL_ID` | `us.anthropic.claude-sonnet-4-5-20250929-v1:0` |

---

## 🔑 Acessos e Infraestrutura

### Google Ads
- Customer ID: `5506512270`
- MCC ID: `9679714188`
- Client ID OAuth: `225354072287-8k6ag7l28jfcito8h5jcddd8rarp04cg.apps.googleusercontent.com`
- Acesso Sergio: **Somente leitura** via MCC (Barbara rebaixou em 15/07/2026 sem autorização do Thiago — pendente correção na segunda-feira)

### AWS
- Lambda: `ss-google-ads-yorkshire` — região us-east-1
- GTM: GTM-PTLTVTHG (instalado no .com.br)
- GitHub Pages: deploy automático via push na main

### WhatsApp Business API
- Thiago já usou API antes (bot engessado R$200/mês — cancelado)
- Número do Thiago pode já estar habilitado para API
- Esposa do Thiago tem acesso vinculado (normal + business) — será desconectada na migração
- **Perfil do número** (foto, nome, descrição, site): [Acessar no Meta Business Manager](https://business.facebook.com/latest/settings/whatsapp_account?business_id=882212698821548&nav_ref=bizweb_settings_asset_linkout&selected_asset_id=2508011329664874&selected_asset_type=whatsapp-business-account&detail_view_tab=PHONE_NUMBERS)

---

## 📊 Performance Atual (últimos 7 dias)

| Métrica | Valor | Variação |
|---------|-------|----------|
| Leads | 428 | +25.9% |
| Custo/Lead | R$ 4,59 | -7.9% |
| CTR | 4.29% | +8.6% |
| Investimento | R$ 1.963 | +15.9% |

**Por campanha:**
- .COM Search: 185 leads, R$5,45/lead, R$1.007 investido
- .COM.BR Search: 78 leads, R$7,17/lead, R$559 investido
- PMax: 165 leads, R$2,40/lead, R$396 investido

**Impression Share crítico**: .COM e PMax apenas 10% — perdendo 83-89% por rank  
**Quality Score**: médio baixo — LP score 2 na maioria (melhoria deferida)  
**Melhor horário**: 14h (36 conv, 16.1% taxa)  
**Geo**: São Paulo domina (305 conv em 7 dias)

---

## 🚧 Pendências

- [ ] Restaurar acesso Admin do Sergio na conta Google Ads (alinhar segunda-feira com Thiago)
- [ ] Fechar contrato bot WhatsApp (sábado)
- [ ] Definir número temporário para desenvolvimento do bot
- [ ] Implementar tracking UTM no .com (Wix)
- [ ] Melhorias landing page .com.br (deferido — aguarda .com.br virar página principal)
- [ ] Investigar qualidade leads PMax

---

## 🗣️ Comunicação

- **Tom**: Humanizado, direto, sem parecer ChatGPT
- **Thiago**: Relatórios de performance, decisões estratégicas
- **GOB (Matheus/Barbara)**: Alinhamentos técnicos de campanha
- **Sergio**: Gestor independente — não é funcionário da GOB

---

## 📁 Docs Importantes

| Arquivo | Conteúdo |
|---------|----------|
| `chatbot-ia-arquitetura.md` | Arquitetura técnica do bot |
| `proposta-chatbot-ia-cliente.md` | Proposta comercial para Thiago |
| `IA DE ATENDIMENTO - WATTSUP.md` | Planejamento do bot WhatsApp |
| `guia-google-ads.md` | Guia das campanhas |
| `historico-campanhas.md` | Histórico de decisões |
| `Infra.md` | Infraestrutura AWS |
| `saas-chatbot-visao.md` | Visão de produto SaaS multi-cliente |
