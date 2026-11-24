# Session Handoff — Yorkshire Canil Brazil

> Leia este arquivo no início do próximo chat para retomar de onde paramos.

---

## Último Deploy — 30/10/2026

### Landing Page
- Seção `#numeros` removida do frontend (Desde 2014, Melhor Canil, FECAM, Brasil)
- Botão "Sobre o Canil" oculto (comentado no HTML)
- Hero-sub: 2 travessões substituídos por vírgula
- FAQ: travessão `linhagem campeã — sem técnicas` substituído por vírgula
- Seção **Na Mídia 📺** criada entre `#famosos` e `#emocoes`
  - 9 vídeos em `src/videos/na tv/` com nomes, posters WebP gerados via ffmpeg
  - CTA próprio: "📺 Quero um filhote igual ao da TV"
  - CSS centralizado (`#natv` adicionado às regras de `#famosos`)
- **`bindWhatsAppLinks()`** refatorado:
  - `sessionStorage` persiste origem pago/orgânico durante a sessão
  - `wpp_secao` adicionado ao evento `whatsapp_click`
  - Mensagem contextual no FAQ (valores/disponibilidade)
  - Chamado após cada `renderVideoSection()` para capturar CTAs dinâmicos
- Banners hero: `Bannerdesktop.jpeg` → `hero-banner.webp` (230KB, 1600x900), `BannerMobile.jpeg` → `hero-banner-mobile.webp` (221KB, 1092x1440)
- GTM `GTM-PTLTVTHG` instalado em todos os 9 HTMLs do blog
- `lazyLoadVideos` removido do `main.js` (código morto)

### Blog
- `yorkshire-canil-brazil-historia.html` — página oculta SEO com conteúdo da seção `#numeros` expandido
- `yorkshire-terrier-sao-paulo.html` — página SEO para SP com keywords da campanha, schema FAQPage
- Links internos apontando para página SP em `quanto-custa` e `como-escolher`
- CBKC → SOBRACI em todos os arquivos (4 arquivos, 7 ocorrências)
- 43 travessões `—` substituídos por vírgula/ponto em 3 arquivos
- Datas aleatórias nos posts (não mais todos "10 de janeiro"):
  - `como-cuidar-filhote-yorkshire` → 14/03/2022
  - `yorkshire-terrier-temperamento` → 22/08/2023
  - `como-escolher-canil` → 07/05/2024
  - `quanto-custa-yorkshire` → 18/11/2025
  - `adotar-ou-comprar-cachorro` → 03/04/2026
- Imagem substituindo vídeo no post `como-proteger-cachorro-furtos.html`
- Cards das 2 páginas novas **ainda não adicionados** ao `blog/index.html` (pendente)

### SEO / Sitemap
- `sitemap.xml` atualizado com `yorkshire-canil-brazil-historia.html` (priority 0.8) e datas corrigidas
- `yorkshire-terrier-sao-paulo.html` no sitemap (priority 0.9)

### Infraestrutura
- Git LFS configurado para todos os `.mp4` (53 arquivos, 444MB migrados)
- `.gitignore` atualizado: arquivos temporários do bot e `.amazonq/prompts/`
- `sharp` instalado como devDependency para conversão WebP
- ffmpeg em `C:\ffmpeg\bin\ffmpeg.exe`

---

## Pendências no Radar (aguardando ordem)

### SEO / Código
- [ ] **#1 CRÍTICO** — Canônico sem www: alinhar `canonical`, `og:url`, JSON-LD, sitemap e robots.txt para `https://yorkshirecanilbrazil.com.br/` (sem www) em todos os arquivos
- [ ] **#3** — Cards das 2 páginas novas (`historia` e `sao-paulo`) no `blog/index.html`
- [ ] **#4** — Feed RSS: remover `<link rel="alternate">` do index ou corrigir build *(aguarda escolha: a ou b)*
- [ ] **#2** — Meta Pixel: preencher ID real ou remover snippet *(aguarda: anuncia no Meta?)*
- [ ] **#5** — Schema `aggregateRating`: remover se reviews não forem verificáveis *(aguarda confirmação)*
- [ ] **#6** — Endereço no Schema: expor rua/CEP ou manter só cidade *(aguarda escolha)*
- [ ] **#7** — Robots.txt: declarar bots de IA (GPTBot, ClaudeBot, etc.) *(aguarda: quer bloquear?)*

### Google Ads / GTM
- [ ] Configurar acionador GTM: tipo "Evento personalizado", nome `whatsapp_click`
- [ ] Tag de Conversão Google Ads (`17082407599 / GwLWCJ__4MgaEK-1w9E_`) — "Uma vez por evento"
- [ ] Confirmar Conversion Linker ativo em "Todas as páginas" no GTM
- [ ] Eventos GA4 com `wpp_origem`, `wpp_secao`, `wpp_btn`
- [ ] Pausar/eliminar campanha Wix (autorizado pelo Thiago em 11/08/2026)

### Landing Page
- [ ] Logo definitiva do cliente
- [ ] Fotos reais dos filhotes
- [ ] Depoimentos reais
- [ ] Deploy final (Cloudflare Pages + domínio) + ativar SEO
- [ ] Configurar GA4 + Meta Pixel
- [ ] Validar `renderVideoSection` no celular real

### Bot
- [ ] Verificar token WhatsApp (erro 400 nos logs)
- [ ] Testes unitários nos Lambdas críticos (processor, bedrock)
- [ ] Sentry no frontend dos painéis
- [ ] Cidades da Grande SP com mesmo preço de SP capital (35 cidades — ver versão anterior do handoff)

---

## Key Insights

- **Deploy**: GitHub Pages, branch `main`, push dispara GitHub Actions (lint + build)
- **DNS .com.br**: GitHub Pages via registro.br (`185.199.108-111.153`), NS em `a.sec.dns.br`
- **DNS .com**: Wix (`NS12/13.WIXDNS.NET`), expira mai/2027, redirect 301 para `.com.br`
- **GTM**: `GTM-PTLTVTHG` com GA4 (`GT-WBKZXHGC`) e Google Ads (`AW-17082407599`)
- **ffmpeg**: `C:\ffmpeg\bin\ffmpeg.exe`
- **Git LFS**: ativo para `*.mp4`
- **API bot**: `https://8x17umz5s7.execute-api.us-east-1.amazonaws.com/dev/` — key: `7e63f385192f40acb7b096d6cab74a13`
- **Google Ads**: MCC `967-971-4188` | Customer `550-651-2270` | Budget R$220/dia | MAXIMIZE_CONVERSIONS
- **Número Thiago**: `5511977118201`
- **Schema FAQ**: erro de texto solto no JSON do `index.html` (pergunta sobre outras raças) — corrigir junto com item #1


**Landing Page — Ajustes visuais e de conteúdo**
- Título da seção famosos: "Famosos que Já Passaram por Aqui" → "ALGUNS FAMOSOS"
- 2 novos vídeos adicionados à seção famosos: `famoso-sidnei-magal.mp4` e `famoso-dionizio-santos.mp4`
  - Sidnei Magal inserido após Fábio Junior (por relevância)
  - Dionizio Santos inserido no final
  - Posters gerados via `scripts/generate-posters.js` (ffmpeg em `C:\ffmpeg\bin\ffmpeg.exe`)
- Seção `#filhotes` — texto atualizado: incluso pedigree, microchip, vacina e vermifugo. Entrega para todo o Brasil.
- FAQ entrega atualizado para alinhar com novo texto
- Cards de títulos (🏆🏆📜) em linha única no mobile — `repeat(3, 1fr)` sempre
- Animação pulse nas setas do carrossel (`:active` → `scale(1.2)` em 200ms)
  - `-webkit-tap-highlight-color: transparent` e `touch-action: manipulation` para iOS/Safari
- Correção do erro 404 `data/media.json` nas páginas do blog — `loadMedia()` retorna cedo se nenhum grid existir

**Blog — 2 novos posts com vídeo**
- `adotar-ou-comprar-cachorro.html` — Vlog1, data 2026-01-10
- `como-proteger-cachorro-furtos.html` — Vlog2, data 2026-07-10
- Posters dos vlogs gerados: `blog-vlog1.webp` (576x1024) e `blog-vlog2.webp` (1024x576)
- Datas dos 4 posts existentes atualizadas (1 por ano retroativo):
  - Quanto Custa Yorkshire → 2025-01-10
  - Como Escolher Canil → 2024-01-10
  - Temperamento Yorkshire → 2023-01-10
  - Como Cuidar Filhote → 2022-01-10
- `blog/index.html` atualizado com 6 cards em ordem decrescente

---

### O que foi feito na sessão anterior (25/ago/2026):

**Troca de modelo Bedrock — Sonnet 4.5 → Haiku 4.5**
- Custo agosto: ~$229 Sonnet 4.5 (~R$ 2.200) — 10x acima do orçado
- Modelo trocado via env var: `us.anthropic.claude-haiku-4-5-20251001-v1:0`
- `config.py` atualizado com novo default
- Projeção setembro: ~$20-25 (~R$ 120-150)

**Prompt otimizado para Haiku**
- Backup do prompt anterior em `s3://.../backup/prompt.txt`
- 3 ajustes aplicados: JSON obrigatório reforçado, conhecimento técnico condensado, exemplos de preço por região (R1/R2/R3)
- Testado: Guarulhos (R1), Campinas (R2), Curitiba (R3) — todos passando ✅

**Lambda de custo corrigida (`yorkshire-bot-cost-dev`)**
- Bedrock não aceita tags de recurso — não aparecia no card
- Nova lógica: Bedrock por dimensão de serviço + demais por tag `Project=yorkshire-bot`
- Card agora mostra valor real: ~$24 em agosto (com Bedrock)

**AWS Support case aberto**
- Pedido de goodwill credit para $229 do Sonnet 4.5
- Texto salvo em `docs/aws-support-case.md`
- Categoria: Other billing questions

**Mensagem redigida para o Thiago**
- Explicação transparente do erro, correção e pedido de contribuição parcial no custo de agosto

---

## Key Insights

- **CDN/Deploy**: CloudFront distribution `E9ZQJ3RPSA04N` — invalidação necessária após cada deploy do painel
- **Lambda deploy**: `Compress-Archive -Force -Path processor.py,dynamodb.py,... -DestinationPath processor-deploy.zip`
- **Dois projetos**: Bot em `c:\Projetos Git\Yorkshire-canil-brazil`, painel em `C:\Projetos Git\SS-Gestao-de-Trafego`
- **Número Thiago**: `5511977118201` (8201)
- **API bot**: `https://8x17umz5s7.execute-api.us-east-1.amazonaws.com/dev/` — key: `7e63f385192f40acb7b096d6cab74a13`
- **Google Ads**: MCC `9679714188` | Customer `5506512270` — credenciais em `C:\Projetos Git\SS-Gestao-de-Trafego\.env`
- **Keywords que mais convertem**: `yorkshire preço` (223 conv), `filhote yorkshire mini` (36), `yorkshire terrier São Paulo` (36), `canil yorkshire` (31)
- **Status válidos no DynamoDB**: `active`, `recovered`, `pending`, `hot_lead_pending`, `sent`, `fechado`, `new`

---

## Próxima Sessão — Tarefas em Ordem

### Painel / Bot
1. ⏳ **Horário de Brasília** nas conversas do painel do Thiago
2. ⏳ **Tique ✔️** para clientes que já tiveram atendimento humano (`human_takeover: true`)

### Landing Page / SEO
3. ⏳ **"Melhor Canil de Yorkshires do Brasil"** — adicionar no SEO (title, meta, h1 hidden) e em várias partes visíveis do site

### Prompt da Bella
4. ⏳ **Cidades da Grande SP com mesmo preço de SP capital** — adicionar ao prompt:
   São Caetano do Sul, Taboão da Serra, Guarulhos, Santo André, Osasco, São Bernardo do Campo,
   Diadema, Mauá, Carapicuíba, Embu das Artes, Barueri, Ferraz de Vasconcelos, Cotia,
   Ribeirão Pires, Caieiras, Itapecerica da Serra, Jandira, Itapevi, Santana de Parnaíba,
   Arujá, Mairiporã, Itaquaquecetuba, Cajamar, Vargem Grande Paulista, Francisco Morato,
   Poá, Suzano, Rio Grande da Serra, Embu-Guaçu, São Lourenço da Serra, Araçariguama,
   Várzea Paulista, Santa Isabel, Campo Limpo Paulista, Jundiaí (35 cidades)

### Google Ads
5. ⏳ **Pausar/eliminar campanha Wix** — Thiago autorizou em 11/08/2026
6. ⏳ **Redirecionar R$ 6.000/mês** exclusivamente para o site novo (yorkshirecanilbrazil.com.br)

### Custo Bedrock — RESOLVIDO ✅
7. ~~🔴 **Trocar Claude Sonnet 4.5 → Haiku 4.5**~~ — feito em 25/ago/2026
   - Modelo: `us.anthropic.claude-haiku-4-5-20251001-v1:0`
   - Prompt otimizado e testado
   - Card de custo corrigido (Bedrock agora aparece)
   - AWS Support case aberto para goodwill credit
   - Mensagem redigida para o Thiago

### Próxima Sessão — Tarefas em Ordem

---

## 🎯 Radar GEO Avançado — 19/10/2026

Varredura realizada com base no suplemento técnico de GEO, Rastreamento e Qualificação 2026+.

### Estado atual
| Item | Status |
|---|---|
| llms.txt | ✅ Completo — diferenciais, FAQ, contato |
| robots.txt — bots de IA | ⚠️ Apenas `User-agent: * Allow: /` — bots de IA não declarados explicitamente |
| JSON-LD LocalBusiness + PetStore | ✅ Implementado |
| JSON-LD FAQPage | ✅ 7 perguntas |
| AggregateRating | ✅ 5★ — mas apenas 3 reviews (baixo) |
| Endereço no Schema | ⚠️ Sem CEP e sem rua — só cidade/estado |
| Meta Pixel | ⚠️ Comentado no HTML — sem ID real ativo |
| GTM lazy load | ❌ GTM carrega no `<head>` sem lazy load |
| GCLID capturado | ❌ Não implementado (documentado como Fase 1 do LIH) |
| Loop GCLID → CRM → Conversão offline | ❌ Sem CRM — loop não fechado |
| Clarity / Hotjar (mapas de calor) | ❌ Não instalado |

### Pendências no radar (aguardando ordem de execução)
```
[ ] ALTA  — Loop conversão offline: GCLID → CRM → API Google Ads (maior impacto)
[ ] ALTA  — Loop conversão offline: fbp/fbc → Meta CAPI
[ ] MÉDIA — robots.txt: declarar GPTBot, ChatGPT-User, Google-Extended, ClaudeBot, PerplexityBot
[ ] MÉDIA — Schema: adicionar CEP + rua no endereço
[ ] MÉDIA — Meta Pixel: ativar com ID real
[ ] MÉDIA — GTM: mover para lazy load (impacto Core Web Vitals)
[ ] BAIXA — Instalar Microsoft Clarity para mapas de calor e gravações
```