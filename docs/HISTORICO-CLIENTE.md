# 🐕 Yorkshire Canil Brazil — Histórico do Cliente

---

## 📋 Dados do Cliente

```
Cliente:          Yorkshire Canil Brazil
Contato:          Thiago
Site .com.br:     yorkshirecanilbrazil.com.br (GitHub Pages — Sergio)
Site .com:        yorkshirecanilbrazil.com (Wix — Thiago, 10 anos histórico)
Nicho:            Criação e venda de Yorkshire Terrier
Google Ads ID:    550-651-2270
Conta Google Ads: yorkshirecanilbrazil@gmail.com
MCC:              967-971-4188 (Ss technologies ltda)
GTM:              GTM-PTLTVTHG
GA4:              552661371
Agência parceira: GOB Marketing (Barbara Passos)
Dashboard:        https://yorkshire.sstechnologies-cloud.com/painel-thiago.html
```

---

## 💰 Contrato

- Gestão mensal: a definir
- Bot IA WhatsApp: R$ 4.000 setup + R$ 300/mês (em negociação)
- Investimento Google Ads: pago direto pelo cliente

---

## 🛠️ Infraestrutura

```
.com.br:     GitHub Pages → AWS (migração feita)
.com:        Wix (Thiago — não mexer)
CDN:         CloudFront
Painel:      AWS S3 (yorkshire.sstechnologies-cloud.com)
Bot:         AWS Lambda + DynamoDB (conta AWS separada)
```

---

## 📊 Métricas de Referência

### Junho/2026 (baseline)
| Métrica | Valor |
|---|---|
| Leads (25 dias) | 1.272 |
| CPC médio | R$ 0,51 |
| Custo/lead | R$ 4,06 |
| Conversão .com.br | 14,9% |
| Conversão .com | 13,9% |
| Investimento | R$ 5.167 |

### Julho/2026 (7 dias — melhor período)
| Métrica | Valor |
|---|---|
| Leads | 543 |
| CPC | R$ 0,42 |
| Custo/lead | R$ 3,54 |
| Investimento | R$ 1.925 |

### Agosto/2026 (pós-reestruturação)
| Métrica | Valor |
|---|---|
| Leads (7 dias) | 118 |
| CPC | R$ 1,93 |
| Custo/lead | R$ 10,56 |
| Investimento | R$ 1.249 |

---

## 📅 Linha do Tempo

| Data | Evento |
|---|---|
| Abr/2026 | Início das campanhas Google Ads |
| 22/04/2026 | Campanhas .COM e Performance Max criadas |
| Jun/2026 | Melhor período — 1.272 leads em 25 dias |
| 06/2026 | Campanha .COM.BR [06.26] criada |
| Jul/2026 | Pagamento bloqueado — campanhas pararam |
| 20/08/2026 | Thiago regularizou pagamento |
| 05/08/2026 | Reestruturação completa — campanha [08.26] criada |
| 03/09/2026 | Ajustes com profissional do Google (keywords, segmentação, grupos, exclusões de conteúdo) |
| Set/2026 | ✅ Acesso Admin do Sergio restaurado na conta Google Ads |
| Set/2026 | ✅ Keywords negativas adicionadas: "adoção", "adotar", "castração" |
| Set/2026 | ✅ Campanha Wix pausada — budget redirecionado para .com.br |
| Set/2026 | ✅ Painel do Thiago: horário de Brasília implementado |
| 22/09/2026 | Análise completa via API: 272 conversões, R$5.536 investidos, R$20,35/conv, CTR 17,88% (últimos 30 dias) |
| 22/09/2026 | **Ações pendentes** (aguardando acesso editor no Google Ads — atualmente só visualizador) |
| Set/2026 | Lambda refatorada para multi-cliente (Yorkshire + Procap) — roteamento por path |
| Set/2026 | Painel expandido: AbsTop IS e Top IS adicionados à tabela de Impression Share |
| 30/09/2026 | **Relatório 7 dias enviado ao Thiago** — 59 conv, R$1.238,52, R$20,99/conv, CTR 21,21%, IS 52,5% |
| 30/09/2026 | Top horários: 10h (7 conv, R$14,06) e 9h (6 conv, R$14,42) |
| 30/09/2026 | Top keywords: "yorkshire micro" (8 conv, R$11,17) e "valor de yorkshire terrier" (8 conv, R$19,79) |
| 30/09/2026 | Oportunidade identificada: 47,5% impressões perdidas (19,3% budget, 28,2% ranking) — sugerido aumento de budget |
| 17/11/2026 | **Stories automáticos no ar** — Lambda `ss-yorkshire-stories` publicando 2x/dia (7h e 18h Brasília) |
| 17/11/2026 | 4 mídias no S3 `sstech-cdn-unified/yorkshire-stories/` (story-01 a story-04) em rotação |
| 17/11/2026 | Token renovação automática — Lambda `ss-yorkshire-token-renewer` a cada 45 dias via EventBridge |
| 17/11/2026 | CloudWatch Alarm + SNS configurados — e-mail em caso de falha na publicação |
| 17/11/2026 | App Meta: `yorkshire-stories` (id `2349383575601565`) — permissões: instagram_basic, instagram_content_publish |
| 17/11/2026 | Instagram ID: `17841401887935389` (@yorkshire.canilbrazil) — BM `yorkshire.canilbrazil` (id `3084045798548292`) |
| 17/11/2026 | **Arquitetura migrada para Step Functions** — publica todos os stories em sequência (1x/dia, 90s intervalo) |
| 17/11/2026 | 33 vídeos no S3 `sstech-cdn-unified/yorkshire-stories/` (story-01 a story-33) — story-07 com música |
| 17/11/2026 | EventBridge `ss-yorkshire-stories-manha` → 5h Brasília (8h UTC) — pronto às 7h |
| 17/11/2026 | EventBridge `ss-yorkshire-stories-noite` desativado — publicação 1x/dia |
| 17/11/2026 | Step Function `ss-yorkshire-stories-flow` — lista S3 → loop MaxConcurrency:1 → publica → wait 90s |
| 17/11/2026 | Mídias locais em `C:\Projetos Git\Yorkshire-canil-brazil\Stories midias\` |

---

## 🔑 Quality Score

| Site | QS Landing Page |
|---|---|
| Wix (.com) | 2 (abaixo da média) |
| Estático (.com.br) | 4.8 ✅ |

---

## ⚙️ Campanhas Ativas

| Campanha | Status | Observação |
|---|---|---|
| [.COM.BR] [08.26] Rede de Pesquisa | Ativa | Nova — ainda em aprendizado |
| [.COM.BR] [06.26] Rede de Pesquisa | Ativa | Melhor custo/lead (R$ 3,37) |
| [22.04.26] Performance Max | Ativa | CPC R$ 0,22 |
| [.COM] [22.04.26] Rede de Pesquisa | Pausada | — |

---

## 🤖 Bot IA — Status

```
Infraestrutura: AWS Lambda + DynamoDB + SQS
Número bot:     Triagem no número principal
Leads quentes:  Transferidos para número separado do Thiago
GCLID:          NÃO implementado (Fase 1 do LIH)
DynamoDB Streams: NÃO habilitado (necessário para LIH)
```

## ⏳ Pendências

- [ ] **Solicitar acesso editor ao Thiago no Google Ads (550-651-2270)** — atualmente só visualizador
- [ ] Pausar `"filhotes de yorkshire a venda"` — QS 2, baixa qualidade, CTR 5,52%
- [ ] Pausar `"yorkshire micro a venda"` — R$60,77/conv (3x acima da média)
- [ ] Pausar `"yorkshire canil brazil"` (frase) — R$73,84/conv, manter só correspondência exata
- [ ] Pausar `"quanto custa um filhote de yorkshire"` — QS 3, 0 conversões
- [ ] Adicionar `[melhor canil de yorkshire sp]` (exata) → grupo 02 - Canil e criador
- [ ] Adicionar `[yorkshire venda]` (exata) → grupo 01 - Compra
- [ ] Reduzir lance entre 3h-5h (3 conversões, R$48 gastos no período)
- [ ] Tique ✔️ no painel do Thiago para clientes com `human_takeover: true` — verificar
- [ ] Bug loop infinito: bot respondendo em loop às mensagens de encerramento (número 6040)
- [ ] Análise tráfego orgânico — usar Cheveux como referência para aplicar no Yorkshire

---

*SS Gestão de Tráfego — Sergio Sena | senanetworker@gmail.com | (11) 98496-9596*
