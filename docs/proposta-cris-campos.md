# Proposta — Cris Campos Prótese Capilar

**Site:** https://criscamposprotesecapilar.com.br/  
**Desenvolvedor atual:** Grupo WebSystem (grupowebsystem.com.br)  
**Plataforma:** WordPress + Elementor + Tema Astra

---

## Diagnóstico

Cris, analisei seu site e ele tem uma boa base visual — o template está bonito e funcional. Porém, existem alguns problemas técnicos que precisam ser corrigidos **antes** de rodar campanha no Google Ads, senão você vai gastar dinheiro sem resultado.

---

## 🚨 Problemas que precisam ser corrigidos

### 1. Endereço fictício no código
O site tem o endereço **"1234 N Spring St"** no rodapé/código. Isso é um endereço de template americano que ficou lá. Mesmo que não apareça visualmente pro visitante, o **Google lê esse código** e entende que seu negócio está nos EUA. Isso prejudica seu posicionamento nas buscas locais.

**Ação:** Remover ou substituir pelo endereço real da clínica.

### 2. "Book A Table" no código
O template usado era originalmente de **restaurante**. Ainda existe referência a "Book A Table" (Reservar Mesa) no código. O Google interpreta isso e pode categorizar seu site incorretamente.

**Ação:** Remover todas as referências a "Book A Table" do código.

### 3. Breadcrumb com "Doméstica"
O schema (código que o Google lê) tem um breadcrumb marcado como "Doméstica" — provavelmente resquício do template. Isso confunde o Google sobre o que seu site realmente é.

**Ação:** Corrigir o breadcrumb para refletir "Prótese Capilar" ou "Saúde e Beleza".

### 4. Sem Google Tag Manager (GTM)
Seu site **não tem nenhum sistema de rastreamento**. Sem GTM, não é possível:
- Medir quantas pessoas clicaram no WhatsApp
- Saber quais anúncios geraram leads
- Otimizar campanhas com dados reais

**Ação:** Instalar GTM com GA4 e eventos de conversão.

### 5. Sem Meta Pixel (Facebook/Instagram)
Sem pixel, não é possível:
- Fazer remarketing (mostrar anúncio pra quem já visitou)
- Otimizar campanhas de Meta Ads
- Criar público semelhante

**Ação:** Instalar Meta Pixel via GTM.

---

## ⚠️ Melhorias de performance

### 6. Página muito pesada
- **30 scripts** carregando (ideal: 5-8)
- **47 arquivos CSS** (ideal: 3-5)
- **201KB de HTML** (ideal: 30-50KB)
- **Nenhuma imagem com lazy loading** (todas carregam de uma vez)

Isso deixa o site lento, especialmente no celular. Página lenta = visitante sai antes de ver o conteúdo = dinheiro de campanha jogado fora.

**Ação:** Pedir pro desenvolvedor:
- Ativar lazy loading nas imagens
- Instalar plugin de cache (WP Rocket ou LiteSpeed Cache)
- Desativar plugins que não usa
- Minificar CSS e JS

### 7. 3 imagens sem texto alternativo (alt)
Prejudica SEO e acessibilidade.

**Ação:** Adicionar alt descritivo em todas as imagens.

---

## ✅ O que já está bom

- Design visual bonito e profissional
- Imagens em WebP (formato otimizado)
- Meta tags configuradas (título, descrição)
- WhatsApp presente com CTAs
- Site responsivo (funciona no celular)
- Schema markup básico presente
- Plugin de agendamento (Bookly) funcionando

---

## Resumo — O que pedir pro seu desenvolvedor

| # | O que fazer | Prioridade | Dificuldade |
|---|-------------|-----------|-------------|
| 1 | Remover endereço "1234 N Spring St" | 🔴 Alta | Fácil |
| 2 | Remover "Book A Table" do código | 🔴 Alta | Fácil |
| 3 | Corrigir breadcrumb "Doméstica" | 🔴 Alta | Fácil |
| 4 | Instalar GTM + GA4 | 🔴 Alta | Médio |
| 5 | Instalar Meta Pixel | 🟡 Média | Fácil |
| 6 | Ativar lazy loading | 🟡 Média | Fácil |
| 7 | Plugin de cache/minificação | 🟡 Média | Fácil |
| 8 | Desativar plugins desnecessários | 🟡 Média | Fácil |
| 9 | Adicionar alt nas imagens | 🟢 Baixa | Fácil |

---

## Próximos passos

1. **Agora:** Enviar essa lista pro desenvolvedor (Grupo WebSystem) corrigir os itens 1-5
2. **Após correções:** Configurar GTM com conversões (clique WhatsApp, agendamento Bookly)
3. **Depois:** Rodar campanha no Google Ads com tracking funcionando

Não tem problema nenhum usar template — a maioria dos sites usa. Mas precisa limpar os resquícios do template original pra não confundir o Google e garantir que a campanha performe bem.

---

**Sergio Sena**  
Desenvolvedor Web & Cloud | Certificado AWS  
WhatsApp: (11) 98496-9596
