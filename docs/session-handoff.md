# Session Handoff — Yorkshire Canil Brazil

> Leia este arquivo no início do próximo chat para retomar de onde paramos.

---

## Último Deploy (canil)

**Commit:** `feat: post preco yorkshire + blog grid 2col + cards semanticos + cores titulo ajustadas`

### O que foi feito na última sessão:
- **SEO index.html** — `<h1>` visually-hidden com keyword principal, alt text hero com keywords reais, texto `#filhotes` com São Paulo/Grande SP, texto `#sobre` com "comprar um Yorkshire Terrier", meta description atualizada
- **Sitemap** — `lastmod` atualizado para datas reais
- **Novo post de blog** — "Quanto Custa um Yorkshire Terrier?" cobrindo keywords `yorkshire preço` (223 conv), `yorkshire terrier preço` (+150%), `quanto custa um yorkshire` (+40%)
- **Blog grid** — fixo em 2 colunas (2x2 simétrico), mobile 1 coluna
- **Cards do blog** — data visível, título completo, link "Leia mais →", cores: verde padrão / escuro no hover
- **`white-space: nowrap`** removido do `h1` dos posts de blog

---

## Problema Crítico em Aberto

`landingPage: 2` em todas as keywords do Google Ads — Quality Score baixo, impression share 10-15%, CPC alto. SEO em andamento para corrigir.

---

## Key Insights

- **CDN/Deploy**: CloudFront distribution `E9ZQJ3RPSA04N` — invalidação necessária após cada deploy do painel
- **Lambda deploy**: `Compress-Archive -Path *.py -DestinationPath lambda.zip -Force` no diretório `src/bot/lambda/`
- **Dois projetos**: Bot em `c:\Projetos Git\Yorkshire-canil-brazil`, painel em `C:\Projetos Git\SS-Gestao-de-Trafego`
- **Número Thiago**: `5511977118201` (8201)
- **API bot**: `https://8x17umz5s7.execute-api.us-east-1.amazonaws.com/dev/` — key: `7e63f385192f40acb7b096d6cab74a13`
- **Google Ads**: MCC `9679714188` | Customer `5506512270` — credenciais em `C:\Projetos Git\SS-Gestao-de-Trafego\.env`
- **Keywords que mais convertem**: `yorkshire preço` (223 conv), `filhote yorkshire mini` (36), `yorkshire terrier São Paulo` (36), `canil yorkshire` (31)

---

## Radar Pendente

### SEO
1. ⏳ Schema.org — adicionar tipo `PetStore` ao `LocalBusiness`
2. ⏳ Testar FAQ no [Rich Results Test](https://search.google.com/test/rich-results)
3. ⏳ Monitorar Quality Score após mudanças (aguardar ~7 dias)

### Bot / Painel
4. ⏳ Migração de status antigos no DynamoDB (`interessado→em_contato`, etc.)

### Conteúdo
5. ⏳ 5º post de blog — sugestão: "Yorkshire Terrier em São Paulo" (keyword 36 conv, CTR 17%)
