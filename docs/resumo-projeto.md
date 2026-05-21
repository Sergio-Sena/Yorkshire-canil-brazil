# Resumo do Projeto: Yorkshire Canil Brasil

Este documento consolida as diretrizes, a estrutura de equipe, as necessidades técnicas e as estratégias discutidas para o início do projeto de desenvolvimento da plataforma web para o cliente **Yorkshire Canil Brasil**.

---

## 1. Visão Geral do Escopo do Projeto

O objetivo principal é construir uma presença digital robusta, iniciando com uma solução ágil e de alta performance que possa evoluir gradualmente para um ecossistema integrado de marketing e atendimento.

1. **Fase Inicial:** Criação de uma Landing Page estática, minimalista, responsiva e com foco total em SEO (otimização para motores de busca).
2. **Fase Intermediária:** Integração de sistemas de captação de métricas, CAPIs de campanhas (Meta/Facebook Business) e relatórios automatizados utilizando conectores nativos do Google Ads no Looker Studio.
3. **Fase Avançada:** Implementação de um chatbot com Inteligência Artificial integrada para atendimento inicial, triagem de clientes e direcionamento estratégico para o fechamento de vendas por atendimento humano.

---

## 2. Estrutura da Landing Page Inicial (Foco em SEO e Conversão)

Como o tráfego orgânico e o ranqueamento no Google são prioridades absolutas, a página deve seguir rigorosamente as melhores práticas de mercado:

* **Estética Minimalista & Elegante:** Alinhada ao nicho de criação de cães de raça com alto padrão.
* **Performance Técnica:** Código limpo, carregamento extremamente rápido (Core Web Vitals) e responsividade impecável.
* **Otimização de Conversão:** Gatilhos visuais e informativos sobre a qualidade, linhagem, saúde dos filhotes, depoimentos de clientes e canais diretos de contato.

---

## 3. Matriz de Profissionais e Personas Recomendadas

Para cobrir as lacunas de execução técnica, design e estratégia, estruturamos quatro perfis profissionais essenciais. Eles podem ser utilizados tanto para contratação quanto para a criação de personas de orientação dentro de ferramentas de IA.

### 👤 Persona 1: O Especialista em SEO (Search Engine Optimization)
* **Papel:** Garantir que o site alcance as primeiras posições do Google de forma orgânica.
* **Atividades:** Pesquisa aprofundada de palavras-chave do nicho (ex: *"filhotes de Yorkshire em SP"*, *"canil de Yorkshire registrado"*), estruturação de tags HTML (`<h1>`, `<h2>`, metadescrições), otimização de imagens e arquitetura de conteúdo para indexação rápida.

### 👤 Persona 2: O UI/UX Designer (Interface e Experiência do Usuário)
* **Papel:** Criar a identidade visual minimalista, fluida e focada na experiência do visitante.
* **Atividades:** Prototipação das telas (desktop e mobile), escolha de tipografia e paleta de cores sofisticada, desenho do fluxo de navegação e mapeamento da jornada do cliente até o clique de conversão (WhatsApp ou formulário).

### 👤 Persona 3: O Desenvolvedor Front-End / Full Stack
* **Papel:** Transcrever o design em código performático e implementar as integrações de dados.
* **Atividades:** Codificação da landing page (HTML5/CSS3/JavaScript estático), garantia de semântica para SEO, e futura integração via APIs (Google Ads, Meta CAPI) para o envio e leitura de dados de conversão.

### 👤 Persona 4: O Engenheiro de IA / Desenvolvedor NLP
* **Papel:** Desenvolver a lógica e a inteligência do assistente virtual.
* **Atividades:** Configuração e treinamento do chatbot com contexto específico do canil (regras de criação, perguntas frequentes sobre a raça, preço, entrega), integração com a API de IA escolhida e lógica de transição fluida do robô para o atendente humano.

---

## 4. Integrações de Marketing & Métricas

Ficou definido o alinhamento estratégico sobre como os dados de tráfego pago serão tratados no ecossistema:

1. **Parceria com a Agência:** A agência de marketing do cliente continuará rodando as campanhas. Para integrar as métricas de conversão ao sistema ou exibir relatórios integrados, será necessária a solicitação de acessos, tokens ou chaves de API diretamente a eles.
2. **Meta Business API:** Uso prévio ou planejado da API de conversões do Meta para traqueamento de anúncios do Facebook/Instagram.
3. **Looker Studio & Google Ads:** Para exibir as métricas de anúncios do Google de forma segura e automatizada, deve-se utilizar os **conectores nativos** do Looker Studio apontando para a conta de anúncios gerenciada, sem a necessidade de passar pelo ambiente do Google AI Studio (que é restrito ao desenvolvimento de modelos de IA como o Gemini).

---

### Próximos Passos Sugeridos
1. Definir o framework/tecnologia da página estática (HTML Puro, Next.js estático, etc.).
2. Alinhar com a agência de marketing o fornecimento dos acessos para planejamento dos dashboards e rastreamento de conversões.
3. Desenhar a árvore de decisão e o tom de voz que a IA do chatbot deverá adotar.
