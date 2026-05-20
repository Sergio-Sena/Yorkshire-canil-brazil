# Estratégia SEO & Google Ads — Yorkshire Canil Brasil

## 1. Palavras-chave Primárias (Alto Volume / Alta Intenção)

| Palavra-chave | Intenção | Uso |
|---|---|---|
| filhotes de yorkshire | Compra | Title, H1, meta description |
| yorkshire terrier filhotes à venda | Compra | H2, conteúdo |
| canil de yorkshire | Pesquisa | H2, conteúdo |
| comprar yorkshire terrier | Compra | CTA, conteúdo |
| yorkshire filhote preço | Compra | FAQ, conteúdo |

## 2. Palavras-chave Secundárias (Cauda Longa)

| Palavra-chave | Uso |
|---|---|
| filhotes de yorkshire com pedigree | Seção diferenciais |
| canil de yorkshire registrado | Seção sobre |
| yorkshire terrier micro | Conteúdo / FAQ |
| yorkshire campeão nacional | Seção títulos |
| melhor canil de yorkshire do brasil | Meta description, conteúdo |
| filhotes yorkshire SP / São Paulo | Geo-targeting |
| yorkshire terrier macho / fêmea disponível | Seção filhotes |
| como escolher um filhote de yorkshire | Blog / FAQ |

## 3. Palavras-chave para Google Ads

### Campanhas de Pesquisa (Search)

**Grupo 1 — Compra direta:**
- comprar filhote yorkshire
- yorkshire terrier venda
- filhote yorkshire disponível
- yorkshire à venda SP

**Grupo 2 — Canil / Criador:**
- canil yorkshire confiável
- criador de yorkshire terrier
- canil registrado yorkshire

**Grupo 3 — Preço:**
- yorkshire filhote preço
- quanto custa um yorkshire terrier
- valor filhote yorkshire

### Palavras-chave Negativas (excluir):
- adoção
- grátis
- doação
- resgate
- SRD
- vira-lata

## 4. Estrutura de Conteúdo da Landing Page (SEO On-Page)

```
H1: Filhotes de Yorkshire Terrier — Yorkshire Canil Brasil
  H2: Nossos Filhotes Disponíveis
  H2: Por que Escolher o Yorkshire Canil Brasil
    H3: Campeões Nacionais e Sul-Americanos
    H3: Pedigree e Registro Oficial
    H3: Saúde e Acompanhamento Veterinário
  H2: Depoimentos de Clientes
  H2: Perguntas Frequentes
    H3: Qual o preço de um filhote?
    H3: Como funciona a entrega?
    H3: Os filhotes vêm vacinados?
  H2: Entre em Contato
```

## 5. Meta Tags Otimizadas

```html
<title>Filhotes de Yorkshire Terrier | Yorkshire Canil Brasil — Campeões Nacionais</title>
<meta name="description" content="Filhotes de Yorkshire Terrier com pedigree e linhagem campeã. Canil registrado com mais de X anos de experiência. Filhotes disponíveis com entrega para todo o Brasil.">
```

## 6. Schema Markup (Dados Estruturados)

Implementar JSON-LD para:
- **LocalBusiness** — nome, endereço, telefone, horário
- **Product** — filhotes disponíveis
- **FAQ** — perguntas frequentes
- **Review** — depoimentos de clientes

## 7. Estratégia de Landing Page para Google Ads

A página de destino dos anúncios deve ter:
- **Headline** alinhada com o texto do anúncio (Quality Score)
- **CTA acima da dobra** (WhatsApp direto)
- **Prova social visível** (títulos, depoimentos)
- **Velocidade < 2.5s LCP** (Core Web Vitals)
- **Sem navegação externa** que tire o usuário da conversão

## 8. Estratégia Meta Business (Facebook & Instagram Ads)

### Open Graph Tags

Implementadas no `<head>` para garantir:
- Preview otimizado ao compartilhar o link no Facebook/Instagram/WhatsApp
- Imagem de capa 1200x630px (`og-cover.jpg`) — usar foto premium de filhote
- Título e descrição persuasivos que incentivem o clique

### Meta Pixel — Eventos Configurados

| Evento | Gatilho | Objetivo |
|---|---|---|
| `PageView` | Carregamento da página | Audiência de retargeting |
| `Lead` | Clique no CTA "Quero Meu Filhote" | Conversão principal |
| `Contact` | Clique no CTA "Falar no WhatsApp" | Conversão secundária |
| `ViewContent` | Scroll até seção filhotes | Público de interesse |

### Públicos para Campanhas

**Público Personalizado (Custom Audience):**
- Visitantes da landing page (últimos 30 dias)
- Quem clicou no WhatsApp mas não converteu
- Engajamento com página/perfil do Instagram

**Público Semelhante (Lookalike):**
- Baseado em compradores anteriores (lista de clientes)
- Baseado em quem clicou no CTA (Lead)

### Estrutura de Campanhas Sugerida

**Campanha 1 — Topo de Funil (Alcance/Tráfego):**
- Objetivo: Tráfego para a landing page
- Criativo: Vídeo/carrossel de filhotes
- Segmentação: Interesse em Yorkshire, pets, cães de raça
- Geo: Estado de SP + capitais do Brasil

**Campanha 2 — Meio de Funil (Engajamento):**
- Objetivo: Engajamento com conteúdo
- Criativo: Depoimentos em vídeo, bastidores do canil
- Segmentação: Público personalizado de visitantes

**Campanha 3 — Fundo de Funil (Conversão):**
- Objetivo: Conversão (evento Lead)
- Criativo: Oferta direta com CTA claro
- Segmentação: Retargeting de visitantes + Lookalike de compradores

### Conversions API (CAPI)

Para máxima precisão de rastreamento (contornando bloqueadores de cookies):
- Configurar Meta Conversions API via servidor
- Pode ser feito via GTM Server-Side ou integração direta
- Necessário: Access Token do Meta Business + Pixel ID

## 9. Tracking & Conversões (Consolidado)

Configurar no HTML:
- Google Tag Manager (GTM)
- Google Analytics 4 (GA4)
- Evento de conversão Google Ads: clique no WhatsApp
- Google Ads Conversion Tag (via GTM)
- Meta Pixel com eventos: PageView, Lead, Contact, ViewContent
- Meta Conversions API (server-side, fase intermediária)

## 10. Estratégia de Content Marketing (Blog)

### Objetivo
Gerar tráfego orgânico de cauda longa, construir autoridade de domínio e nutrir leads que ainda não estão prontos para comprar.

### Artigos Publicados

| Artigo | Keyword Principal | Keywords Secundárias |
|---|---|---|
| Como Cuidar de um Filhote de Yorkshire | como cuidar filhote yorkshire | alimentação yorkshire, vacina yorkshire filhote |
| Temperamento do Yorkshire Terrier | yorkshire terrier temperamento | personalidade yorkshire, yorkshire com crianças |
| Como Escolher um Canil Confiável | canil yorkshire confiável | como comprar yorkshire, canil registrado |

### Próximos Artigos Sugeridos

| Keyword | Volume Estimado | Dificuldade |
|---|---|---|
| yorkshire micro vs padrão | Médio | Baixa |
| quanto custa um yorkshire terrier 2025 | Alto | Média |
| yorkshire pelo longo vs curto | Médio | Baixa |
| yorkshire late muito | Médio | Baixa |
| diferença yorkshire macho e fêmea | Médio | Baixa |
| yorkshire pode ficar sozinho | Médio | Baixa |

### Benefícios para SEO

- **Internal linking:** Cada artigo linka para a landing page (CTA WhatsApp)
- **Topical authority:** Google entende que o domínio é especialista em Yorkshire
- **Long-tail traffic:** Captura buscas informacionais que viram leads
- **Fresh content:** Conteúdo novo sinaliza ao Google que o site está ativo
- **Rich snippets:** Schema Article em cada post melhora CTR nos resultados

### Frequência de Publicação

- Mínimo: 2 artigos por mês
- Ideal: 1 artigo por semana
- Cada artigo deve ter 800-1500 palavras

## 11. Seção de Depoimentos (Prova Social)

### Impacto no SEO e Conversão

- **Schema Review/AggregateRating:** Gera estrelas nos resultados do Google (rich snippets)
- **Prova social:** Aumenta confiança e taxa de conversão
- **Conteúdo único:** Depoimentos são conteúdo original que o Google valoriza

### Boas Práticas

- Usar nomes reais (com autorização) ou cidade/estado
- Incluir fotos dos filhotes com os donos (quando possível)
- Atualizar depoimentos periodicamente
- Coletar via Google Business Profile para reforçar SEO local

### Imagem obrigatória para Open Graph

Criar `src/images/og-cover.jpg`:
- Dimensão: 1200x630px
- Conteúdo: Foto de filhote Yorkshire + logo do canil
- Peso: < 300KB (otimizada para carregamento rápido)
