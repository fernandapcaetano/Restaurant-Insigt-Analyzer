
# Restaurant Insight Analyzer

**Visão Geral**
- **Descrição:** Sistema de análise de dados para restaurantes que cruza informações de vendas, comentários (reviews), cardápio e registros de entrega para identificar por que as vendas subiram ou caíram e recomendar ações práticas.
- **Objetivo:** Fornecer resumos acionáveis e recomendações para aumentar receita, otimizar cardápio e melhorar a experiência do cliente.

**Recursos Principais**
- **Análise de vendas:** agrega vendas por prato, identifica horário de pico, total de pedidos e receita por produto.
- **Análise de comentários:** classifica reviews em positivos/negativos, extrai pontos relevantes para ações (reclamações, elogios).
- **Integração com modelagem de linguagem:** usa um agente (modelo de chat) para gerar resumos e recomendações consolidadas.
- **Formato estruturado de insights:** resultado validado por modelos Pydantic/typing para facilitar uso em dashboards ou relatórios.

**Instalação Rápida**
- **Requisitos:** `Python 3.10+` e `pip`.
- **Criar e ativar ambiente virtual (Windows PowerShell):**
```
python -m venv venv
; .\venv\Scripts\Activate.ps1
```
- **Instalar dependências:**
```
pip install -r requirements.txt
```

**Variáveis de Ambiente (obrigatórias)**
- `MODEL_BASE_URL` : URL base do serviço do modelo (ex.: endpoint da API do provedor).
- `API_KEY` : Chave de API para autenticação do modelo.
- `MODEL_NAME` : Nome do modelo de chat a ser usado.
- `MODEL_EMBEDDING_NAME` : (se aplicável) nome do modelo de embedding.

Exemplo (PowerShell):
```
$env:MODEL_BASE_URL = 'https://api.exemplo.com'
$env:API_KEY = 'sua_chave_aqui'
$env:MODEL_NAME = 'gpt-5-mini'
$env:MODEL_EMBEDDING_NAME = 'embed-model'
```

**Executando o projeto**
- **Carregar dados e gerar insights:**
```
python main.py
```
- **Descrição do `main.py`:** carrega dados das pastas `resource/`, categoriza vendas e reviews, e invoca o `Agent` para gerar um resumo geral (`AiInsightResumo`).

**Estrutura do Projeto**
- `main.py` : ponto de entrada para gerar insights.
- `model/` : modelos Pydantic/entidades do domínio (ex.: `prato.py`, `venda.py`, `review.py`, `insight.py`, `agent_insight.py`).
- `service/` : lógica de carregamento e orquestração (`load_data.py`, `agent.py`).
- `resource/` : datasets CSV de exemplo (`menu.csv`, `venda.csv`, `reviews.csv`).
- `view/` : (espaço para futuras visualizações ou exportadores de relatório).

**Detalhes de Implementação**
- `service/load_data.py` : lê CSVs, faz parsing de datas, normaliza colunas e produz listas de objetos (`Prato`, `Venda`, `Review`). Também gera listas de insights (`VendaInsight`, `ReviewInsight`).
- `service/agent.py` : encapsula chamada ao modelo de chat (via `ChatOpenAI`), envia schema esperado e os dados consolidados para que o modelo retorne um JSON compatível com `AiInsightResumo`.

**Exemplo de uso prático**
- Verifique quais pratos têm maior receita e poucos comentários positivos — investigue preço, tempo de entrega e qualidade.
- Filtre reclamações frequentes por horário de pico para otimizar equipe/entregas.
- Use os insights estruturados para atualizar a página do cardápio (destacar pratos mais lucrativos) ou criar promoções em horários de menor movimento.

**Boas práticas e extensões sugeridas**
- Adicionar validação e testes unitários sobre `load_data` e as transformações de insight.
- Criar scripts de ETL para atualização periódica dos dados.
- Integrar com visualização (ex.: Dash, Streamlit) para painéis interativos.
- Capturar métricas de qualidade das previsões do agente (ex.: avaliação humana dos resumos).

**Limitações Conhecidas**
- A qualidade das recomendações depende da qualidade dos dados (formatos corretos em `resource/`).
- O agente depende de um serviço de modelo externo — custos e latência podem variar.

**Próximos Passos Rápidos**
- Adicionar um `examples/` com notebooks ou scripts demonstrando análises comuns.
- Automatizar a execução e salvar relatórios em `output/`.

Se quiser, eu posso: gerar um exemplo de notebook que consome `AiInsightResumo`, criar testes unitários para `load_data.py` ou preparar um script de deploy simples. Diga qual próximo passo prefere.
