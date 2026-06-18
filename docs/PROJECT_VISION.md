# PROJECT_VISION.md

# IA DE ATENDIMENTO WHATSAPP - YORKSHIRE CANIL BRAZIL

Versão: 1.0

Autor: Sergio Sena

Status: Planejamento MVP

---

# Visão Geral

O objetivo deste projeto é criar uma assistente virtual inteligente para atendimento dos clientes do Yorkshire Canil Brazil através do WhatsApp.

A solução deverá utilizar Inteligência Artificial para responder dúvidas de forma natural, gerar confiança, qualificar potenciais compradores e transferir o atendimento para um humano quando houver intenção real de compra.

A proposta é substituir fluxos tradicionais de chatbot por uma experiência conversacional semelhante ao atendimento humano.

---

# Objetivos do Projeto

## Objetivos Principais

- Atender clientes 24 horas por dia.
- Responder dúvidas sobre a raça Yorkshire Terrier.
- Explicar os diferenciais do canil.
- Coletar informações dos interessados.
- Qualificar leads.
- Encaminhar clientes para atendimento humano.
- Reduzir tempo gasto com perguntas repetitivas.

## O que a IA NÃO deve fazer

- Fechar vendas.
- Informar preços.
- Negociar pagamentos.
- Confirmar reservas.
- Confirmar disponibilidade de filhotes.
- Inventar informações.

---

# Contexto do Negócio

## Empresa

Yorkshire Canil Brazil

Site:

https://yorkshirecanilbrazil.com.br/

## Diferenciais Identificados

- Especialização exclusiva em Yorkshire Terrier.
- Mais de 10 anos de experiência.
- Linhagens selecionadas.
- Campeão Nacional.
- Campeão Sul-Americano.
- Canil dos artistas.
- Entrega para diversas regiões do Brasil.
- Acompanhamento pós-venda.
- Atendimento personalizado.
- Criação ética e responsável.
- Acompanhamento veterinário.

---

# Decisão Arquitetural

## NÃO utilizar RAG no MVP

Motivos:

- Conteúdo relativamente pequeno.
- Apenas uma raça.
- Poucas regras de negócio.
- Menor custo.
- Menor complexidade.

Estratégia inicial:

Claude Sonnet

-

Prompt de Sistema

-

Base de Conhecimento

-

Histórico da Conversa

---

# Arquitetura da Solução

Cliente

↓

Site / Instagram / Facebook / Google / WhatsApp

↓

Mesmo Número de WhatsApp

↓

WhatsApp Cloud API

↓

API Gateway

↓

AWS Lambda

↓

Amazon Bedrock (Claude Sonnet)

↓

DynamoDB

↓

Resposta ao Cliente

---

# Fluxo de Atendimento

## Etapa 1

Recepção

A IA inicia uma conversa natural.

Objetivo:

Gerar confiança.

---

## Etapa 2

Descoberta

A IA tenta identificar:

- Nome.
- Cidade.
- Estado.
- Interesse em macho ou fêmea.
- Prazo de compra.

---

## Etapa 3

Educação

Responder dúvidas sobre:

- Temperamento.
- Higiene.
- Alimentação.
- Adaptação a apartamentos.
- Crianças.
- Convivência com outros animais.
- Cuidados gerais.

---

## Etapa 4

Qualificação

Identificar intenção de compra.

Exemplos:

- Solicitação de preço.
- Solicitação de fotos.
- Solicitação de vídeos.
- Solicitação de reserva.
- Solicitação de disponibilidade.

---

## Etapa 5

Transferência

Quando detectar lead qualificado:

lead_status = WAITING_HUMAN

Mensagem:

"Perfeito. Já reuni suas informações e vou encaminhar seu atendimento para nossa equipe especializada, que continuará seu atendimento."

---

# Estrutura Recomendada do Projeto

backend/

├── lambda/

│ ├── handler.py

│ ├── bedrock.py

│ ├── dynamodb.py

│ ├── whatsapp.py

│ └── lead_manager.py

│

├── prompts/

│ ├── system_prompt.txt

│ └── transfer_prompt.txt

│

├── knowledge/

│ ├── company.json

│ ├── faq.md

│ ├── breed_info.md

│ ├── sales_rules.md

│ └── handoff_rules.md

│

├── infrastructure/

│ ├── terraform/

│ └── cloudformation/

│

└── docs/

├── PROJECT_VISION.md

├── ARCHITECTURE.md

└── DEPLOYMENT.md

---

# Estrutura de Conhecimento

## company.json

Contém informações institucionais do canil.

Exemplos:

- Nome.
- Tempo de atuação.
- Diferenciais.
- Entrega.
- Suporte pós-venda.

---

## faq.md

Perguntas frequentes.

Exemplos:

- Yorkshire late muito?
- Yorkshire se adapta a apartamento?
- Yorkshire convive com crianças?
- Yorkshire convive com gatos?
- Yorkshire pode ficar sozinho?
- Qual a expectativa de vida?

---

## breed_info.md

Informações técnicas da raça.

- História.
- Temperamento.
- Alimentação.
- Exercícios.
- Higiene.
- Saúde preventiva.

---

## sales_rules.md

Regras comerciais.

Define o que a IA pode ou não responder.

---

## handoff_rules.md

Define quando o atendimento deve ser transferido para humano.

---

# DynamoDB

Tabela:

Conversations

Campos:

- phone_number
- customer_name
- city
- state
- interest_gender
- purchase_timeframe
- lead_status
- conversation_history
- last_interaction

---

# Critérios de Lead Quente

Um lead deve ser considerado HOT quando:

- Solicita preço.
- Solicita fotos.
- Solicita vídeos.
- Solicita reserva.
- Solicita disponibilidade.
- Demonstra intenção clara de compra.

Exemplo:

{
"lead_status": "HOT",
"handoff": true
}

---

# Prompt de Sistema

Você é a assistente virtual oficial do Yorkshire Canil Brazil.

Sua função é atender clientes de forma natural, acolhedora, educada e profissional.

Nunca diga que é um chatbot.

Nunca diga que é uma inteligência artificial, exceto se for questionada diretamente.

Você representa oficialmente o Yorkshire Canil Brazil.

Seu papel é agir como uma consultora especializada na raça Yorkshire Terrier.

## Informações do Canil

- Especialização exclusiva em Yorkshire Terrier.
- Mais de 10 anos de experiência.
- Campeão Nacional.
- Campeão Sul-Americano.
- Linhagens selecionadas.
- Criação ética e responsável.
- Acompanhamento veterinário.
- Atendimento personalizado.
- Entrega para diversas regiões do Brasil.
- Suporte pós-venda.

## Estilo

- Simpática.
- Educada.
- Profissional.
- Natural.
- Objetiva.

## Objetivos

Coletar:

- Nome.
- Cidade.
- Estado.
- Interesse em macho ou fêmea.
- Prazo de compra.

## Restrições

Nunca:

- Informar preços.
- Confirmar disponibilidade.
- Confirmar reservas.
- Confirmar pagamentos.
- Inventar informações.

## Transferência

Transferir para humano quando houver:

- Pedido de preço.
- Pedido de reserva.
- Pedido de pagamento.
- Pedido de disponibilidade.
- Pedido de fotos.
- Pedido de vídeos.
- Interesse real de compra.

Mensagem:

"Perfeito. Já reuni suas informações e vou encaminhar seu atendimento para nossa equipe especializada, que continuará seu atendimento."

---

# Custos Estimados

## AWS

API Gateway

R$ 0 ~ R$ 5

Lambda

R$ 0 ~ R$ 5

DynamoDB

R$ 0 ~ R$ 5

CloudWatch

R$ 0 ~ R$ 5

Bedrock Claude

R$ 20 ~ R$ 80

Total estimado:

R$ 30 ~ R$ 100/mês

---

# Modelo Comercial Sugerido

Implantação:

R$ 1.500 ~ R$ 3.000

Mensalidade:

R$ 250 ~ R$ 400

Incluindo:

- Hospedagem AWS.
- Monitoramento.
- Ajustes de Prompt.
- Pequenas evoluções.

---

# Roadmap

Fase 1

- WhatsApp Cloud API
- Claude Sonnet
- DynamoDB
- Prompt
- FAQ

Fase 2

- Dashboard de Leads
- CRM
- Relatórios

Fase 3

- Bedrock Knowledge Base
- RAG
- OpenSearch Serverless

---

# Decisão Final

Para o Yorkshire Canil Brazil:

✅ Serverless AWS

✅ Claude Sonnet no Bedrock

✅ DynamoDB

✅ WhatsApp Cloud API

✅ Handoff para humano

✅ Sem RAG inicialmente

✅ Estrutura preparada para evolução futura
