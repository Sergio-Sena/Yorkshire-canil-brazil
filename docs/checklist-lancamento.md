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
