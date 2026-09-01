# Session Handoff — Yorkshire Canil Brazil

> Leia este arquivo no início do próximo chat para retomar de onde paramos.

---

## Último Deploy

### O que foi feito nesta sessão (data atual):

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
