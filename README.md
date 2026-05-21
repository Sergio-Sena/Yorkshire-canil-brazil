# Yorkshire Canil Brazil

Landing page estática e performática para o Yorkshire Canil Brazil — canil campeão nacional e sul-americano, referência em Yorkshire Terrier na América Latina desde 2014.

## 🌐 Preview

**Live:** [sergio-sena.github.io/Yorkshire-canil-brazil](https://sergio-sena.github.io/Yorkshire-canil-brazil/)

> ⚠️ Site em modo preview (noindex). Deploy final pendente aprovação do cliente.

## 🛠️ Stack

- HTML5 semântico
- CSS3 (Glassmorphism, variáveis, mobile-first)
- JavaScript vanilla (ES6+)
- Google Fonts (Playfair Display + Montserrat)
- Sem frameworks — zero dependências em produção

## 📁 Estrutura

```
src/
├── blog/           # Artigos SEO (3 posts)
├── css/            # Estilos (temas claro/escuro)
├── data/           # media.json (mídias dinâmicas)
├── images/         # Imagens otimizadas (WebP)
├── js/             # Carrossel, tema, lazy load
├── videos/         # Vídeos de famosos e campanhas
├── index.html      # Página principal
├── manifest.json   # PWA
├── robots.txt      # Bloqueio crawlers (MVP)
└── sitemap.xml     # Mapa do site
docs/
├── checklist-lancamento.md    # Deploy, tracking, migração
├── chatbot-ia-arquitetura.md  # Bot IA futuro (Lex/Bedrock)
├── seo-strategy.md            # Estratégia SEO
└── planejamento.md            # Planejamento inicial
```

## 🚀 Comandos

```bash
# Instalar dependências
npm install

# Servidor local
npm run dev

# Lint
npm run lint

# Build (minifica HTML/CSS/JS → dist/)
npm run build
```

## 🎨 Temas

| Tema | Accent | Background |
|------|--------|------------|
| Claro | Esmeralda `#059669` | `#f8fafc` |
| Escuro | Azul Petróleo `#0ea5e9` | `#0a0f1a` |

## 📊 Performance

| Métrica | Desktop | Mobile |
|---------|---------|--------|
| Performance | 100 | 89 |
| Acessibilidade | 100 | 100 |
| Práticas recomendadas | 100 | 100 |
| SEO | 63* | 63* |

*SEO bloqueado intencionalmente (noindex) durante preview.

## 🔄 CI/CD

Push na `main` → GitHub Actions (lint + build) → Deploy automático no GitHub Pages.

## 📋 Documentação

- [Checklist de Lançamento](docs/checklist-lancamento.md) — Deploy, tracking, migração Wix
- [Chatbot IA](docs/chatbot-ia-arquitetura.md) — Arquitetura futura com AWS
- [Estratégia SEO](docs/seo-strategy.md) — Palavras-chave e conteúdo
- [Planejamento](docs/planejamento.md) — Escopo e fases do projeto

## 📝 Próximos Passos

- [ ] Logo definitiva do cliente
- [ ] Fotos reais dos filhotes
- [ ] Depoimentos reais
- [ ] Deploy final (Cloudflare Pages + domínio)
- [ ] Ativar SEO (remover noindex)
- [ ] Configurar GA4 + Meta Pixel
- [ ] Teste A/B vs site Wix atual

---

**Desenvolvido por:** Sergio Sena  
**Cliente:** Yorkshire Canil Brazil  
**Status:** MVP em preview
