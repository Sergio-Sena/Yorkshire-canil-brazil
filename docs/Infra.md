backend/
├── lambda/
│ ├── handler.py
│ ├── bedrock.py
│ ├── whatsapp.py
│ └── dynamodb.py
│
├── prompts/
│ ├── system_prompt.txt
│ └── transfer_prompt.txt
│
├── knowledge/
│ ├── company.json
│ ├── faq.md
│ ├── breed_info.md
│ └── sales_rules.md
│
└── infrastructure/
├── terraform
└── cloudformation

    Quanto cobrar do cliente?

Eu dividiria em:

Implantação

Você vai:

Criar infraestrutura AWS.
Configurar Bedrock.
Configurar Meta Developers.
Configurar Webhook.
Criar prompt.
Criar base de conhecimento.
Testar.

Como profissional AWS/Cloud, eu não cobraria menos que:

Faixa inicial

R$ 1.500 a R$ 3.000

Mensalidade

Você terá:

Hospedagem AWS.
Custos Bedrock.
Monitoramento.
Ajustes de prompt.
Correções.
Plano simples

R$ 150 a R$ 300/mês

Plano gerenciado

R$ 300 a R$ 600/mês

Incluindo:

Atualizações.
Ajustes da IA.
Novas perguntas.
Relatórios básicos.
O que eu faria se fosse meu projeto

Para um cliente como o Yorkshire Canil Brazil:

Implantação

R$ 2.500

Mensalidade

R$ 250

O cliente paga:

R$ 250 manutenção

- custos AWS
- custos Meta

ou

R$ 350/mês tudo incluso

Eu prefiro o modelo "tudo incluso", porque o cliente não quer entender Bedrock, Lambda e Meta.

Manutenção real

Depois que estiver funcionando:

95% do tempo não vai exigir nada.
O maior trabalho será ajustar respostas da IA.
Adicionar novas informações.
Atualizar FAQ.

Provavelmente:

1 a 2 horas por mês.

Um detalhe importante

Como você já trabalha com AWS e Serverless, eu faria uma melhoria que aumenta muito o valor percebido:

Gravar no DynamoDB:

{
"nome": "João",
"cidade": "Curitiba",
"interesse": "Fêmea",
"status": "HOT_LEAD",
"ultima_interacao": "2026-06-09"
}

E criar um painel simples para o canil visualizar leads.

Isso muda a percepção de:

"chatbot"

para

"sistema de captação e qualificação de clientes"

E aí fica muito mais fácil justificar uma mensalidade recorrente.

Site
Instagram
Facebook
Google
Indicação
QR Code

        ↓

Mesmo número WhatsApp

        ↓

Cloud API

        ↓

Claude Sonnet

        ↓

DynamoDB

        ↓

Atendente humano

Assim qualquer pessoa que mandar mensagem para aquele número, independentemente da origem, conversa primeiro com a IA e depois é transferida para o proprietário quando estiver pronta para fechar a compra.

Essa é a arquitetura que eu implementaria para o projeto. Ela elimina a diferença entre "veio do site" e "veio direto pelo WhatsApp". Para a IA, tudo é apenas uma conversa chegando no mesmo número.s
