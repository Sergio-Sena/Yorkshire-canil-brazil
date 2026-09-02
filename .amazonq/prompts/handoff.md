# Handoff — Yorkshire Canil Brazil

Use este prompt no início de cada sessão para restaurar o contexto completo do projeto.

---

## Estado Atual do Projeto

### Commits recentes (branch `main`)
- `892e1d4` — chore: atualiza poster do Fabio Junior
- `94dfa51` — chore: adiciona novo video do Fabio Junior
- `cfb474e` — feat: renderVideoSection com player central + thumbs
- `7ad67cc` — fix: corrigir corte de vídeo no mobile
- `e81826a` — fix: separar regras CSS filhote-card e video-item no mobile

### O que foi resolvido
1. **Vídeos blog responsivos** — `.blog-post video` com `aspect-ratio: 16/9` no CSS
2. **Scroll carrossel** — `scrollAmount` substituído por `getScrollAmount()` chamada no clique
3. **Player de vídeo mobile** — `renderVideoSection()`: player central grande + thumbnails clicáveis. Resolve corte, descentralização e snap
4. **Vídeo Fábio Junior** — arquivo substituído + poster gerado via ffmpeg
5. **Bot restaurado** — variáveis de ambiente sumiram do Lambda, bot caía em DLQ. Restauradas via `update_env.py` com Haiku

---

## Arquivos-chave e estado

| Arquivo | Estado |
|---|---|
| `src/css/style.css` | ✅ Limpo, lint ok |
| `src/js/main.js` | ✅ `renderVideoSection()` para vídeos; `renderCarousel()` apenas para filhotes |
| `src/data/media.json` | ✅ Estrutura: `titulosVideos`, `famosos`, `emocoes`, `emocoesExtras` |
| `src/bot/lambda/update_env.py` | ✅ Modelo corrigido para Haiku — usar sempre este arquivo para atualizar variáveis |

---

## Arquitetura de vídeos

### `renderVideoSection(container, items, aspect)`
- Player central (`video-section-player`) com `aspect-ratio` passado como parâmetro
- Thumbnails clicáveis (`video-section-thumb`) abaixo do player
- Clicar na thumb → pausa, troca `src`, dá play, marca `active`
- Títulos: `aspect = "9/16"`, `max-width: 320px`
- Famosos/Emoções: `aspect = "16/9"`, `max-width: 560px`

### `renderCarousel(container, items)` — apenas filhotes
- `.filhote-card` com snap mobile (`width: 100%; min-width: 100%`)

---

## Bot — Estado atual

### Modelo em produção
- **Haiku 4.5** (`us.anthropic.claude-haiku-4-5-20251001-v1:0`) nos 3 Lambdas
- Sonnet 4.5 gerou $229 antes da troca — Haiku é ~20x mais barato

### Teste realizado (02/09/2026)
- ✅ Saudação + captura de nome
- ✅ Identificação de cidade/região (SP capital → Região 1)
- ✅ Preferência de sexo
- ✅ Foto enviada
- ✅ Preço com ancoragem (de R$5.949 por R$4.949) — intencional
- ✅ Transferência para Thiago (final 8201)
- ⚠️ Não testado: pagamento, parcelamento, entrega, objeções

### Backup e fallback
- **Prompt:** armazenado no S3 com versionamento — 6 versões disponíveis
- **`has_backup: true`** — rollback via `POST /prompt/rollback`
- **Versão mais recente:** `mkeGxj1l` (25/08/2026, 8.036 bytes)
- **Falha no processor:** mensagem cai na DLQ → `dlq-consumer` responde com mensagem de erro técnico + notifica equipe via SNS
- **Variáveis sumiram:** causa raíz foi atualização parcial do Lambda (só `BEDROCK_MODEL_ID`). Sempre usar `update_env.py` para atualizar

### Preços por região (prompt ativo)
| Região | Macho | Fêmea |
|---|---|---|
| SP capital + Grande SP | de R$4.949 por R$3.949 | de R$5.949 por R$4.949 |
| Interior SP | de R$6.449 por R$5.449 | de R$7.449 por R$6.449 |
| Outros estados | de R$7.990 por R$6.990 | de R$8.990 por R$7.990 |

---

## Infraestrutura

- **ffmpeg:** `C:\ffmpeg\bin\ffmpeg.exe` — usar `-y` para auto-confirmar sobrescrita
- **GitHub:** `https://github.com/Sergio-Sena/Yorkshire-canil-brazil.git` — branch `main`, deploy via GitHub Actions → GitHub Pages
- **CloudFront:** `E9ZQJ3RPSA04N`
- **Bot endpoint:** `https://8x17umz5s7.execute-api.us-east-1.amazonaws.com/dev/`
- **API Key bot:** `7e63f385192f40acb7b096d6cab74a13`
- **Thiago phone:** `5511977118201`
- **Painel:** CloudFront + S3 (`painel-thiago.html`, `painel-gestor.html`)
- **Segundo repo (painéis):** `C:\Projetos Git\SS-Gestao-de-Trafego`

---

## Pendências / Próximos passos

### Landing page
- [ ] Validar `renderVideoSection` no celular real (Títulos, Famosos, Emoções)
- [ ] Remover funções mortas `lazyLoadVideos` do `main.js`
- [ ] Logo definitiva, fotos reais dos filhotes, depoimentos reais
- [ ] Deploy final (Cloudflare Pages + domínio) + ativar SEO (remover noindex)
- [ ] Configurar GA4 + Meta Pixel

### Bot
- [ ] Testar pagamento, parcelamento, entrega e objeções
- [ ] Verificar token WhatsApp (erro 400 nos logs — pode estar expirado)
- [ ] Testes unitários nos Lambdas críticos (`processor.py`, `bedrock.py`)
- [ ] Sentry no frontend dos painéis
- [ ] Implementar preços por região no `context.md` (já está no prompt e no `config.py`)
