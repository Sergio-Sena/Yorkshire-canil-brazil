# Yorkshire Canil Brazil — Checklist de Lançamento

## 1. Conteúdo Real (aguardando criativo)

### 1.1 Imagem Hero
- [ ] Receber imagem real da fachada/yorkshires (substituir imagem IA)
- [ ] Recortar a faixa superior do menu da imagem (evitar duplicidade com header)
- [ ] Salvar em `src/images/` com nome descritivo (ex: `hero-banner.webp`)
- [ ] Converter para WebP para performance
- [ ] Atualizar o `src` em `index.html` na seção `#inicio`

### 1.2 Fotos dos Filhotes
- [ ] Receber fotos reais dos filhotes disponíveis
- [ ] Salvar em `src/images/filhotes/`
- [ ] Substituir os `.filhote-img-placeholder` por `<img>` com `loading="lazy"`
- [ ] Atualizar nome, sexo e informações de cada card
- [ ] Exemplo de substituição:
```html
<!-- De: -->
<div class="filhote-img-placeholder">
  <span>🐾</span>
  <p>Foto em breve</p>
</div>

<!-- Para: -->
<img src="images/filhotes/filhote-01.webp" alt="Filhote Yorkshire macho" loading="lazy" />
```

### 1.3 Vídeos de Famosos
- [ ] Receber URLs dos vídeos (Instagram Reels / YouTube Shorts)
- [ ] Descomentar a seção `#famosos` no `index.html`
- [ ] Substituir `.video-placeholder` por embeds reais:
```html
<iframe src="URL_DO_VIDEO" loading="lazy" allowfullscreen></iframe>
```
- [ ] Adicionar "Famosos" de volta ao menu se necessário

### 1.4 Depoimentos em Vídeo (Emoções Reais)
- [ ] Receber vídeos de clientes reais
- [ ] Descomentar a seção `#emocoes` no `index.html`
- [ ] Substituir placeholders por embeds

### 1.5 Depoimentos Escritos
- [ ] Receber depoimentos reais com nome e cidade
- [ ] Descomentar a seção `#depoimentos` no `index.html`
- [ ] Atualizar textos e nomes reais
- [ ] Adicionar "Depoimentos" de volta ao menu nav
- [ ] Atualizar o schema JSON-LD de reviews com dados reais

### 1.6 Logo Definitiva
- [ ] Receber logo vetorial/PNG de alta qualidade
- [ ] Substituir `e9762d_8b6bed4dcbc94d0c927977c8fc01122d~mv2.avif` em todas as páginas
- [ ] Gerar favicon em múltiplos tamanhos (16x16, 32x32, 180x180, 512x512)
- [ ] Atualizar `manifest.json` com os novos ícones

### 1.7 Imagem OG (compartilhamento social)
- [ ] Criar imagem 1200x630px para compartilhamento
- [ ] Salvar como `src/images/og-cover.jpg`
- [ ] Já está referenciada nas meta tags

---

## 2. Deploy

### 2.1 Pré-deploy
- [ ] Rodar `npm run build` para minificar CSS/JS
- [ ] Verificar se todas as imagens estão otimizadas (WebP, comprimidas)
- [ ] Testar em múltiplos navegadores (Chrome, Safari, Firefox, Edge)
- [ ] Testar responsividade (mobile, tablet, desktop)
- [ ] Validar HTML: https://validator.w3.org/
- [ ] Testar performance: https://pagespeed.web.dev/
- [ ] Verificar links quebrados
- [ ] Confirmar que `robots.txt` e `sitemap.xml` estão corretos

### 2.2 Hospedagem (opções recomendadas)
**Opção 1 — AWS Amplify (recomendado)**
- [ ] Conectar repositório GitHub ao AWS Amplify
- [ ] Configurar build: diretório de saída `dist/`
- [ ] Configurar domínio customizado `yorkshirecanilbrazil.com.br`
- [ ] SSL automático via Amplify

**Opção 2 — Amazon S3 + CloudFront**
- [ ] Criar bucket S3 com hospedagem estática
- [ ] Configurar CloudFront como CDN
- [ ] Configurar certificado SSL via ACM
- [ ] Apontar domínio via Route 53

**Opção 3 — Netlify/Vercel (alternativa simples)**
- [ ] Conectar repositório
- [ ] Build automático a cada push
- [ ] Configurar domínio customizado

### 2.3 DNS
- [ ] Apontar `yorkshirecanilbrazil.com.br` para o hosting
- [ ] Apontar `yorkshirecanilbrazil.com` como redirect para `.com.br`
- [ ] Configurar `www` como redirect para domínio principal
- [ ] Verificar propagação DNS (24-48h)

### 2.4 Pós-deploy
- [ ] Verificar se o site carrega corretamente no domínio final
- [ ] Testar formulário de captura de leads
- [ ] Testar botões de WhatsApp
- [ ] Submeter sitemap no Google Search Console
- [ ] Submeter sitemap no Bing Webmaster Tools

---

## 3. Tracking e Analytics

### 3.1 Google Analytics 4 (GA4)
- [ ] Criar propriedade GA4 em https://analytics.google.com/
- [ ] Obter ID de medição (G-XXXXXXXXXX)
- [ ] Adicionar script no `<head>` de todas as páginas:
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### 3.2 Google Tag Manager (GTM)
- [ ] Criar container GTM em https://tagmanager.google.com/
- [ ] Obter ID (GTM-XXXXXXX)
- [ ] Descomentar o bloco GTM no `<head>` e `<body>` do `index.html`
- [ ] Substituir `GTM-XXXXXXX` pelo ID real
- [ ] Configurar triggers para:
  - Clique no WhatsApp
  - Envio do formulário de leads
  - Scroll depth (25%, 50%, 75%, 100%)

### 3.3 Meta Pixel (Facebook/Instagram)
- [ ] Criar pixel em https://business.facebook.com/
- [ ] Obter Pixel ID
- [ ] Descomentar o bloco Meta Pixel no `index.html`
- [ ] Substituir `SEU_PIXEL_ID` pelo ID real
- [ ] Eventos já configurados no código:
  - `PageView` — automático
  - `Lead` — clique no WhatsApp (hero e float)
  - `Contact` — clique no WhatsApp (seção contato)

### 3.4 Google Search Console
- [ ] Verificar propriedade do domínio
- [ ] Submeter `sitemap.xml`
- [ ] Monitorar indexação das páginas
- [ ] Verificar erros de rastreamento

### 3.5 Hotjar / Microsoft Clarity (opcional)
- [ ] Criar conta gratuita em https://clarity.microsoft.com/
- [ ] Adicionar script de tracking
- [ ] Monitorar heatmaps e gravações de sessão
- [ ] Identificar pontos de abandono

---

## 4. Manutenção Contínua

- [ ] Atualizar filhotes disponíveis conforme nascem/são vendidos
- [ ] Publicar novos posts no blog (mínimo 2x/mês para SEO)
- [ ] Coletar e adicionar depoimentos reais
- [ ] Monitorar performance no PageSpeed (manter acima de 90)
- [ ] Atualizar sitemap.xml ao adicionar novas páginas
- [ ] Revisar e responder comentários/mensagens

---

## 5. Estratégia de Migração (Wix → Novo Site)

### Situação Atual
- Domínio `yorkshirecanilbrazil.com.br` ativo no Wix
- Contrato Wix vigente
- Novo site pronto para deploy

### Fase 1 — Preview (agora)
- [ ] Novo site no GitHub Pages para aprovação: `sergio-sena.github.io/Yorkshire-canil-brazil`
- [ ] Cliente testa e aprova
- [ ] Wix continua ativo normalmente

### Fase 2 — Subdomínio (após aprovação)
- [ ] Criar conta Cloudflare Pages (grátis)
- [ ] Deploy do novo site no Cloudflare Pages
- [ ] No painel DNS do Wix, criar CNAME: `novo.yorkshirecanilbrazil.com.br` → Cloudflare Pages
- [ ] Cliente acessa `novo.yorkshirecanilbrazil.com.br` para validação final
- [ ] Site Wix continua ativo em `yorkshirecanilbrazil.com.br`

### Fase 3 — Virada (quando 100% aprovado)
- [ ] No painel DNS, apontar `yorkshirecanilbrazil.com.br` para Cloudflare Pages
- [ ] Ou transferir DNS para Cloudflare (grátis, mais controle)
- [ ] Testar domínio principal no novo site
- [ ] Remover `noindex` e ativar SEO
- [ ] Descomentar canonical
- [ ] Atualizar robots.txt
- [ ] Submeter sitemap no Google Search Console

### Fase 4 — Desativar Wix (quando contrato vencer)
- [ ] Cancelar plano Wix
- [ ] Confirmar que DNS não depende mais do Wix
- [ ] Economia mensal do plano Wix

### Hosting Recomendado por Fase

| Fase | Hosting | Custo | CDN |
|------|---------|-------|-----|
| Preview | GitHub Pages | Grátis | Fastly |
| Produção | Cloudflare Pages | Grátis | Cloudflare Global |
| Se crescer muito | S3 + CloudFront | ~$5-10/mês | AWS Global |

### Por que Cloudflare Pages?
- Grátis (sem limite de banda)
- CDN global (mais rápido que S3 para sites estáticos)
- SSL automático
- Deploy automático via GitHub
- Custom domain fácil
- Zero manutenção

### Quando migrar para S3 + CloudFront?
- Tráfego acima de 100k visitas/mês
- Necessidade de controle avançado (Lambda@Edge, headers custom)
- Vídeos muito pesados que precisem de streaming adaptativo (HLS)
- Integração com outros serviços AWS

---

## 6. Teste A/B — Wix vs Novo Site (mesmo domínio)

### Como Funciona

O domínio `yorkshirecanilbrazil.com.br` fica no Wix. Criamos um subdomínio apontando para o novo site:

| URL | Destino |
|---|---|
| `yorkshirecanilbrazil.com.br` | Site Wix (atual) |
| `novo.yorkshirecanilbrazil.com.br` | Novo site (Cloudflare Pages) |

### Configuração no Wix

1. No painel Wix → Domínios → DNS
2. Adicionar registro CNAME:
   - Nome: `novo`
   - Valor: URL do Cloudflare Pages (ex: `yorkshire-canil-brazil.pages.dev`)
3. Aguardar propagação DNS (até 48h)

### Links de Acesso

- **Site atual:** `https://www.yorkshirecanilbrazil.com.br`
- **Novo site:** `https://novo.yorkshirecanilbrazil.com.br`

### Como Testar (via agência de marketing)

A agência roda 2 campanhas idênticas no Meta Ads:
- **Campanha A** → destino: `www.yorkshirecanilbrazil.com.br` (Wix)
- **Campanha B** → destino: `novo.yorkshirecanilbrazil.com.br` (novo)
- Mesmo público, mesmo orçamento, mesmo criativo
- Duração: 30 dias

### O que Medir

| Métrica | Ferramenta | Meta |
|---|---|---|
| Leads gerados | GA4 + Meta Pixel | Qual gera mais |
| Tempo na página | GA4 | Maior = melhor |
| Taxa de rejeição | GA4 | Menor = melhor |
| Cliques no WhatsApp | Meta Pixel (evento Lead) | Qual converte mais |
| Custo por lead | Meta Ads | Menor = melhor |
| Velocidade de carga | PageSpeed | Nota mais alta |

### Pré-requisitos

- [ ] Google Analytics (GA4) instalado nos dois sites (mesmo property, views separadas)
- [ ] Meta Pixel instalado nos dois sites
- [ ] Subdomínio `novo` configurado no DNS do Wix
- [ ] Novo site deployado no Cloudflare Pages com custom domain
- [ ] Agência ciente do teste e com os dois links

### Resultado Esperado

Após 30 dias:
- Se novo site performa melhor → migra domínio principal para ele
- Se Wix performa melhor → ajustamos o novo site com base nos dados
- Se empate → mantém novo site (mais barato, sem mensalidade Wix)

### Custo do Teste

| Item | Custo |
|---|---|
| Cloudflare Pages | Grátis |
| Subdomínio | Grátis (já tem o domínio) |
| GA4 | Grátis |
| Meta Pixel | Grátis |
| Ads para teste | Orçamento da agência (já existente) |
| **Total adicional** | **R$ 0** |

### Após o Teste (decisão)

**Se novo site vence:**
1. Apontar `www.yorkshirecanilbrazil.com.br` para Cloudflare Pages
2. Wix vira redirect ou desativa quando contrato vencer
3. Economia da mensalidade Wix

**Se Wix vence:**
1. Analisar o que o Wix tem que o novo não tem
2. Implementar melhorias no novo site
3. Rodar novo teste em 30 dias
