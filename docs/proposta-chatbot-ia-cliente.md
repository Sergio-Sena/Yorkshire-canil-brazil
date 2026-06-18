# Proposta Comercial — Assistente Virtual IA via WhatsApp
## Yorkshire Canil Brazil

**Preparado por:** Sergio Sena  
**Data:** Junho 2025  
**Versão:** 1.0

---

## 1. Visão Geral

Implantação de uma assistente virtual inteligente no WhatsApp do canil que atende clientes 24 horas por dia, responde dúvidas sobre a raça Yorkshire Terrier, qualifica potenciais compradores e transfere automaticamente para atendimento humano quando há intenção real de compra.

**Resultado para o canil:**
- Zero leads perdidos fora do horário comercial
- Redução de 80% das perguntas repetitivas
- Qualificação automática de clientes (quente / morno / frio)
- Painel de leads com nome, cidade e interesse

---

## 2. Como Funciona (Fluxo Simplificado)

```
┌─────────────────────────────────────────────────┐
│  Cliente entra em contato via WhatsApp           │
│  (vindo do Site, Instagram, Google, Indicação)   │
└──────────────────────┬──────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────┐
│  IA responde de forma natural e acolhedora       │
│  • Tira dúvidas sobre a raça                     │
│  • Explica diferenciais do canil                 │
│  • Coleta nome, cidade, interesse                │
└──────────────────────┬───────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────┐
│  Detecta intenção de compra?                     │
│  (pediu preço, fotos, disponibilidade, reserva)  │
└─────────┬────────────────────────┬───────────────┘
          │ SIM                    │ NÃO
          ▼                        ▼
┌─────────────────────┐  ┌────────────────────────┐
│ Transfere para o    │  │ Continua educando e    │
│ proprietário com    │  │ nutrindo o interesse   │
│ resumo do lead      │  │ do potencial cliente   │
└─────────────────────┘  └────────────────────────┘
```

**Importante:** A IA NUNCA informa preço, confirma disponibilidade ou fecha venda. Isso é sempre feito pelo humano.

---

## 3. Infraestrutura Técnica

| Componente | Serviço AWS | Função |
|---|---|---|
| Canal de entrada | WhatsApp Cloud API (Meta) | Recebe e envia mensagens |
| Porta de entrada | API Gateway | Recebe webhook do WhatsApp |
| Cérebro | AWS Lambda (Python) | Orquestra o fluxo |
| Inteligência | Amazon Bedrock (Claude) | Gera respostas naturais |
| Memória | DynamoDB | Salva leads e histórico |
| Alertas | SNS | Notifica novo lead quente |
| Monitoramento | CloudWatch | Logs e métricas |

**Características:**
- 100% serverless (paga só quando usa)
- Escala automaticamente
- Alta disponibilidade (99.9%)
- Sem servidor para manter

---

## 4. O que a IA Faz e Não Faz

### ✅ A IA FAZ:
- Atende 24h, inclusive madrugadas e feriados
- Responde dúvidas sobre Yorkshire (temperamento, cuidados, alimentação)
- Explica diferenciais do canil (títulos, experiência, pedigree)
- Informa sobre entrega, vacinas, documentação
- Coleta dados do interessado (nome, cidade, preferência macho/fêmea)
- Classifica o lead (quente, morno, frio)
- Avisa o proprietário quando tem lead quente
- Transfere naturalmente para atendimento humano

### ❌ A IA NÃO FAZ:
- Informar preços ou valores
- Confirmar disponibilidade de filhotes
- Fechar vendas ou reservas
- Negociar pagamento
- Inventar informações

---

## 5. Sprints de Entrega

### Sprint 1 — Configuração e Infraestrutura (5 dias)

| Entrega | Descrição |
|---|---|
| Conta Meta Developers | Configurar WhatsApp Cloud API |
| Infraestrutura AWS | API Gateway + Lambda + DynamoDB |
| Webhook | Conexão Meta ↔ AWS funcionando |
| Teste de recebimento | Mensagem chega no sistema |

**Marco:** Mensagem do WhatsApp chega na AWS e retorna resposta fixa de teste.

---

### Sprint 2 — Inteligência e Prompt (4 dias)

| Entrega | Descrição |
|---|---|
| Amazon Bedrock | Configurar Claude como modelo |
| Prompt de sistema | Tom de voz, regras, restrições |
| Base de conhecimento | FAQ, informações do canil, raça |
| Histórico de conversa | IA lembra o contexto da conversa |

**Marco:** IA conversa naturalmente sobre o canil e a raça, mantendo tom profissional e acolhedor.

---

### Sprint 3 — Qualificação e Handoff (3 dias)

| Entrega | Descrição |
|---|---|
| Qualificação de leads | Classifica quente/morno/frio |
| Coleta de dados | Nome, cidade, interesse |
| Handoff automático | Transfere para humano quando necessário |
| Notificação SNS | Alerta o proprietário de lead quente |
| DynamoDB | Salva todos os leads e conversas |

**Marco:** Lead qualificado é registrado e proprietário recebe notificação em tempo real.

---

### Sprint 4 — Testes e Go-Live (3 dias)

| Entrega | Descrição |
|---|---|
| Testes end-to-end | Simular cenários reais |
| Ajustes de prompt | Refinar respostas com base nos testes |
| Ativação em produção | Número real do canil conectado |
| Documentação | Manual de operação para o cliente |
| Treinamento | Orientação sobre o painel de leads |

**Marco:** Sistema em produção no número real do canil.

---

### Resumo do Cronograma

| Sprint | Duração | Acumulado |
|---|---|---|
| Sprint 1 — Infra | 5 dias | 5 dias |
| Sprint 2 — IA | 4 dias | 9 dias |
| Sprint 3 — Leads | 3 dias | 12 dias |
| Sprint 4 — Go-Live | 3 dias | **15 dias úteis** |

**Prazo total: 3 semanas**

---

## 6. Precificação

### Implantação (pagamento único)

| Item | Valor |
|---|---|
| Configuração WhatsApp Cloud API + Meta Developers | Incluso |
| Infraestrutura AWS (API Gateway, Lambda, DynamoDB) | Incluso |
| Integração Amazon Bedrock (Claude) | Incluso |
| Criação do prompt e base de conhecimento | Incluso |
| Sistema de qualificação de leads | Incluso |
| Notificação de leads quentes | Incluso |
| Testes e go-live | Incluso |
| **Total implantação** | **R$ 2.500** |

---

### Mensalidade (tudo incluso)

| Item | Valor |
|---|---|
| Hospedagem AWS (Lambda, DynamoDB, API Gateway) | Incluso |
| Custos Amazon Bedrock (IA) | Incluso |
| Custos Meta/WhatsApp | Incluso |
| Monitoramento e disponibilidade 24h | Incluso |
| Ajustes de prompt e respostas da IA | Incluso |
| Atualizações da base de conhecimento | Incluso |
| Suporte técnico | Incluso |
| **Total mensal** | **R$ 350/mês** |

---

### Resumo Financeiro

| | Valor |
|---|---|
| Investimento inicial | R$ 2.500 (único) |
| Mensalidade | R$ 350/mês |
| **Custo no 1º mês** | **R$ 2.850** |
| **Custo mensal recorrente** | **R$ 350** |

---

## 7. O que o Cliente Recebe

- ✅ Assistente virtual ativa 24/7 no WhatsApp
- ✅ Atendimento natural (não parece robô)
- ✅ Qualificação automática de leads
- ✅ Notificação imediata quando lead está pronto para comprar
- ✅ Registro de todos os interessados (nome, cidade, interesse)
- ✅ Zero preocupação com infraestrutura
- ✅ Manutenção e ajustes inclusos na mensalidade

---

## 8. Pré-requisitos do Cliente

Para iniciar o projeto, o cliente precisa fornecer:

1. **Número de WhatsApp** que será usado (novo ou existente)
2. **Conta Meta Business** verificada (ou criaremos juntos)
3. **Documento da empresa** para verificação Meta
4. **Informações atualizadas** sobre filhotes, serviços e diferenciais
5. **Aprovação** do tom de voz e respostas da IA

---

## 9. Evolução Futura (opcional)

| Fase | O que inclui | Investimento adicional |
|---|---|---|
| Dashboard de Leads | Painel web para visualizar leads | R$ 1.500 |
| Relatório mensal automático | Insights (cidades, horários, perguntas top) | R$ 1.000 |
| Integração CRM | Exportar leads para ferramenta do canil | R$ 1.000 |

---

## 10. Garantias

- **7 dias de teste** após go-live para ajustes sem custo extra
- **SLA 99.9%** de disponibilidade (infraestrutura AWS)
- **Cancelamento** da mensalidade a qualquer momento com 30 dias de aviso

---

## Próximo Passo

Aprovar esta proposta para início do desenvolvimento em **Sprint 1**.

---

*Yorkshire Canil Brazil — Sistema de Atendimento Inteligente*  
*Tecnologia: Amazon Web Services (AWS)*
