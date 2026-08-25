# Session Handoff — Yorkshire Canil Brazil

> Leia este arquivo no início do próximo chat para retomar de onde paramos.

---

## Último Deploy

**Commits:**
- `6674e2c` — seo: schema LocalBusiness + PetStore
- `1d616c4` — fix: status e human_takeover no nível raiz da conversa, não dentro de lead_data
- `dd48392` — test: valida status e human_takeover no nível raiz da conversa

### O que foi feito nesta sessão:
- **Rich Results Test** — 6 itens válidos: LocalBusiness+PetStore, Organização, 4 Snippets de avaliação ✅
- **Schema.org** — `@type: ["LocalBusiness", "PetStore"]` no index.html
- **Bug fix DynamoDB** — `status` e `human_takeover` agora salvos no nível raiz da conversa, não dentro de `lead_data`
- **`save_conversation`** — aceita parâmetros opcionais `status` e `human_takeover`
- **`_mark_human_takeover`** — simplificado, sem buscar conversa desnecessariamente
- **Deduplicação** — confirmada correta: `handler.py` + SQS FIFO com `MessageDeduplicationId`
- **DynamoDB scan** — sem status antigos (`interessado`, `em_contato`), item do handoff era falso alarme
- **Testes** — 22 passando (novo: `test_save_conversation_status_at_root`)

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

### Custo Bedrock — PRIORIDADE ALTA
7. 🔴 **Trocar Claude Sonnet 4.5 → Haiku 3.5** — custo atual ~$490/mês, estimativa com Haiku ~$40/mês (12x mais barato)
   - Ver `src/bot/lambda/bedrock.py` — trocar `BEDROCK_MODEL_ID`
   - Ajustar prompt caching para persistir entre Lambda instances
   - Histórico já limitado a 40 entradas (ok)
   - Dados: cacheWrite ~2400-2800 tokens por nova instance, input cresce por turn
   - Cost Explorer 01-14/ago: Claude Sonnet 4.5 = $229, Bedrock geral = $23

### Monitoramento
8. ⏳ **Quality Score** — aguardar ~7 dias após mudanças SEO para medir impacto
