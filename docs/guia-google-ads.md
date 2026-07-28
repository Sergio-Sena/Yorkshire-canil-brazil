# Guia Google Ads — Supervisão de Campanhas

**Objetivo:** Entender o suficiente pra supervisionar a agência GOB sem ser enganado.

---

## 1. Métricas Essenciais

| Métrica | O que é | Bom pra Yorkshire | Red Flag |
|---------|---------|-------------------|----------|
| **Impressões** | Quantas vezes o anúncio apareceu | 500+/dia | < 100/dia (orçamento baixo ou keyword ruim) |
| **Cliques** | Quantas vezes clicaram no anúncio | 30+/dia | < 10/dia |
| **CTR** | % de quem viu e clicou (Cliques ÷ Impressões) | 3-8% | < 2% (anúncio ruim ou keyword errada) |
| **CPC** | Custo por clique | R$ 0,80-2,00 | > R$ 3,00 (competição alta ou quality score baixo) |
| **Conversões** | Leads gerados (WhatsApp, formulário) | 5+/dia | < 1/dia |
| **Taxa de conversão** | % de quem clicou e virou lead | 10-15% | < 5% (landing page ruim ou público errado) |
| **CPA (Custo por Lead)** | Quanto custa cada lead | R$ 5-10 | > R$ 20 |
| **ROAS** | Retorno sobre investimento em ads | 5x+ | < 2x (gastando mais do que gera) |
| **Quality Score** | Nota do Google pro seu anúncio (1-10) | 7+ | < 5 (anúncio/keyword/landing page desalinhados) |
| **Impression Share** | % do total de buscas que você apareceu | 50%+ | < 20% (orçamento insuficiente) |

### Fórmulas importantes:
```
CTR = Cliques ÷ Impressões × 100
CPC = Investimento ÷ Cliques
CPA = Investimento ÷ Conversões
ROAS = Receita ÷ Investimento
Taxa de Conversão = Conversões ÷ Cliques × 100
```

---

## 2. Estrutura do Google Ads

```
Conta (CID: 550-651-2270)
└── Campanha (orçamento diário, segmentação geográfica, tipo)
    └── Grupo de Anúncios (keywords agrupadas por tema)
        ├── Keywords (palavras que ativam o anúncio)
        └── Anúncios (texto que aparece na busca)
```

### Tipos de campanha:
| Tipo | Onde aparece | Quando usar |
|------|-------------|-------------|
| **Rede de Pesquisa** | Resultados do Google | Quem já está buscando (intenção alta) |
| **Performance Max** | Google, YouTube, Gmail, Maps, Display | Automação total do Google com IA |
| **Display** | Banners em sites parceiros | Remarketing, awareness |
| **YouTube** | Vídeos antes/durante conteúdo | Branding, demonstração |
| **Shopping** | Aba Shopping do Google | E-commerce (não se aplica) |

### No caso do Yorkshire:
- **[BP] [GOB] [.COM] [22.04.26] - Rede de Pesquisa** → site Wix
- **[BP] [GOB] [.COM.BR] [06.26] - Rede de Pesquisa** → site novo
- **[BP] [GOB] [22.04.26] - Performance Max** → automática

---

## 3. Keywords — Como Funciona

### Tipos de correspondência:
| Tipo | Símbolo | Exemplo | Ativa quando buscam |
|------|---------|---------|---------------------|
| **Ampla** | nenhum | yorkshire preço | yorkshire valor, quanto custa york, filhote yorkshire barato |
| **Frase** | "aspas" | "yorkshire preço" | yorkshire preço SP, qual yorkshire preço |
| **Exata** | [colchetes] | [yorkshire preço] | yorkshire preço (só isso) |

### O que cobrar da agência:
- Quais keywords estão ativas?
- Qual tipo de correspondência?
- Ampla demais = gasta dinheiro com busca irrelevante
- Exata demais = perde volume

### Palavras negativas:
- Termos que você **não quer** que ativem o anúncio
- Exemplo: "adoção", "grátis", "doação" (já estão negativadas ✅)
- Revisar semanalmente os **Termos de Pesquisa** pra encontrar novos termos irrelevantes

---

## 4. Orçamento e Lances

### Como o dinheiro é gasto:
1. Você define um **orçamento diário** por campanha
2. O Google pode gastar até **2x** o diário num dia, mas no mês não passa do total (diário × 30,4)
3. Cada clique custa o **CPC** — definido por leilão em tempo real

### Estratégias de lance:
| Estratégia | Como funciona | Quando usar |
|-----------|---------------|-------------|
| **Maximizar cliques** | Google busca mais cliques possível | Início, gerar dados |
| **Maximizar conversões** | Google prioriza quem vai converter | Quando já tem 30+ conversões/mês |
| **CPA desejado** | Você define quanto quer pagar por lead | Campanha madura com histórico |
| **ROAS desejado** | Você define o retorno esperado | E-commerce (não se aplica) |
| **CPC manual** | Você define o lance de cada keyword | Controle total, mais trabalho |

### Red flags de orçamento:
- Orçamento diário muito baixo → poucas impressões → poucos dados → otimização lenta
- Orçamento concentrado em horários ruins (madrugada)
- Sem limite de CPC máximo em estratégia automática

---

## 5. Red Flags — Sinais de Agência Ruim

### 🚨 Problemas graves:
| Sinal | O que significa |
|-------|----------------|
| Não compartilha acesso à conta | Pode estar escondendo algo |
| CPC subindo sem explicação | Não está otimizando |
| Mesmo anúncio há meses | Não faz teste A/B |
| Sem palavras negativas novas | Não revisa termos de pesquisa |
| Conversões caindo, investimento igual | Campanha deteriorando |
| Só mostra impressões e cliques | Esconde métricas de conversão |
| Campanhas competindo entre si | Canibalismo (nosso caso!) |
| Não responde sobre segmentação geográfica | Pode estar rodando pra lugar errado |

### ⚠️ Sinais de atenção:
| Sinal | O que significa |
|-------|----------------|
| Relatório só com números bonitos | Cherry-picking de dados |
| "O algoritmo precisa de tempo" por mais de 30 dias | Desculpa pra não otimizar |
| Muitas keywords de correspondência ampla | Gasta orçamento com busca irrelevante |
| Sem extensões de anúncio | Preguiça, perde CTR |
| Landing page genérica | Não personaliza por campanha |

### ✅ Sinais de agência boa:
- Compartilha acesso total
- Relatório semanal com ações tomadas
- Testa novos anúncios regularmente
- Revisa termos de pesquisa e adiciona negativas
- Segmentação geográfica correta
- Explica mudanças de estratégia

---

## 6. Relatórios — O Que Cobrar

### Semanal (mínimo):
- Investimento total
- Leads gerados
- CPA (custo por lead)
- Keywords que mais converteram
- Keywords negativas adicionadas
- Ações realizadas na semana

### Mensal:
- Comparativo mês anterior
- Evolução do CPA
- Termos de pesquisa completos
- Teste A/B de anúncios (qual ganhou)
- Sugestões de otimização
- Segmentação geográfica (onde estão os leads)

### Perguntas pra fazer:
1. "Qual a taxa de conversão por campanha?"
2. "Quais termos de pesquisa novos apareceram essa semana?"
3. "Quantas negativas foram adicionadas?"
4. "Qual a segmentação geográfica de cada campanha?"
5. "As campanhas estão competindo entre si?"
6. "Qual o Quality Score médio das keywords?"
7. "Qual estratégia de lance está usando e por quê?"

---

## 7. Glossário Rápido

| Termo | Significado |
|-------|-------------|
| CID | ID da conta Google Ads |
| CPC | Custo por clique |
| CPA | Custo por aquisição (lead) |
| CTR | Taxa de cliques |
| ROAS | Retorno sobre investimento em ads |
| Impressão | Anúncio apareceu na tela |
| Conversão | Ação desejada (lead, venda, ligação) |
| Quality Score | Nota 1-10 do Google (relevância) |
| Impression Share | % das buscas que você apareceu |
| Search Terms | O que as pessoas realmente digitaram |
| Negative Keywords | Palavras que bloqueiam o anúncio |
| Ad Extensions | Informações extras no anúncio (telefone, links, local) |
| Landing Page | Página onde o clique leva |
| Bounce Rate | % que entrou e saiu sem fazer nada |
| Remarketing | Mostrar anúncio pra quem já visitou o site |
| Leilão | Competição em tempo real entre anunciantes |
| Lance | Quanto você aceita pagar por clique |
| Segmentação | Pra quem/onde o anúncio aparece |
| Dispositivo | Desktop, mobile, tablet |
| Programação | Horários/dias que o anúncio roda |
| Performance Max | Campanha automática do Google com IA |

---

## 8. Checklist de Supervisão

### Semanal (5 min):
- [ ] CPA está abaixo de R$ 10?
- [ ] CTR está acima de 3%?
- [ ] Leads estão chegando diariamente?
- [ ] Alguma campanha parou de converter?

### Quinzenal (15 min):
- [ ] Termos de pesquisa — tem lixo?
- [ ] Negativas novas foram adicionadas?
- [ ] Campanhas não estão competindo entre si?
- [ ] Orçamento está distribuído corretamente?

### Mensal (30 min):
- [ ] CPA melhorou vs mês anterior?
- [ ] Anúncios foram testados (A/B)?
- [ ] Segmentação geográfica está correta?
- [ ] Quality Score das keywords principais?
- [ ] Comparar .COM vs .COM.BR (qual performa melhor?)

---

## 9. Referências de Estudo

| Canal | Foco | Link |
|-------|------|------|
| **Pedro Sobral** | Meta Ads (Facebook/Instagram) | YouTube |
| **Tiago Tessmann** | Google Ads (referência #1 BR) | YouTube |
| **Adriano Gianini** (Métricas Boss) | Google Ads avançado | YouTube |
| **Google Skillshop** | Certificação oficial gratuita | skillshop.withgoogle.com |

---

## 10. Situação Atual — Yorkshire

| Item | Status |
|------|--------|
| Negativadas | ✅ Bem feitas (adoção, grátis, OLX, etc.) |
| Canibalismo | ⚠️ .COM e .COM.BR competindo nas mesmas keywords |
| CPA .COM.BR | ✅ R$ 6,21 (bom) |
| CPA .COM | ⚠️ R$ 7,48 (aceitável) |
| Performance Max | ✅ R$ 2,10/lead (melhor CPA) |
| Segmentação geográfica | ❓ Verificar se está regionalizada |
| Acesso visualizador | 🔄 Solicitado à GOB |

---

**Criado em:** 07/07/2026
**Atualizado por:** Sergio Sena
