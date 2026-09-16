# CHANGELOG

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

## [v1.2.0] - 2026-09-16
### Adicionado
- **Observabilidade Completa & Tracing (Langfuse v2)**:
  - Servidor Langfuse (`langfuse/langfuse:2`) integrado via Docker na porta `:3001` com persistência em PostgreSQL 15 (`postgres:15-alpine`).
  - Bucket MinIO S3 dedicado `/data/langfuse` para retenção persistente de eventos e payloads de LLM.
  - Spans de ciclo de vida de requisição (`icepol_query_handler`), parsing de ontologia (`semantic_ontology_parsing`), inferência de raciocínio (`deepseek_r1_sql_synthesis`) e execução colunar (`duckdb_columnar_query`).
- **Banco de Dados de Métricas e Auditoria (MySQL 8.0)**:
  - Container MySQL 8.0 (`mysql-db`) na porta `:3306` com schema `icepol_metrics` e autenticação nativa estável.
  - Tabela `query_metrics` registrando sessões, modelo utilizado, prompt em linguagem natural, SQL compilado, contagem de linhas retornadas, latências parciais e totais, e estimativa de tokens.
- **Novo Modelo Gratuito de Raciocínio (DeepSeek-R1 1.5B)**:
  - Download e integração via Ollama do `deepseek-r1:1.5b` (1.1 GB) com suporte a Chain-of-Thought determinístico.
- **Painel de Telemetria e Traces no Frontend**:
  - Novo botão e popover interativo `Métricas & Traces` no cabeçalho do Icepol com status ao vivo de Langfuse, MinIO e MySQL.
- **Produção de Vídeos Demonstrativos em Full HD 1080p e Novas Trilhas Sonoras**:
  - `video/icepol_chat_ui_journey_1.5x_funky_upbeat.mp4` (40s): **Gravação na UI de Chat Acelerada em 1.5x com Trilha Animada & Groovy** — Roteiro ágil de 40s passando pela tela inicial, digitação rápida de prompt, resposta analítica com DuckDB, diagrama conceitual Mermaid (Crow's foot), popover de observabilidade, cockpit Langfuse, waterfall de spans e gráfico de distribuição de tokens.
  - `video/soundtrack_funky_upbeat_lofi_40s.wav`: **Nova trilha sonora Funky Upbeat Lo-Fi (Animada, Alegre e Confortável)** — 112 BPM (Eb Major), piano elétrico Rhodes sincopado, linha de baixo slap acústico saltitante e percussão swingada sem ruídos estridentes.
  - `video/icepol_chat_ui_journey_lofi_chill.mp4` (60s): Versão em velocidade normal com trilha relaxante Lo-Fi Ambient Rhodes (82 BPM).
  - `video/icepol_user_journey_langfuse_tokens.mp4` (60s): Jornada completa com navegação e clone no GitHub, build de terminal, chat e Langfuse (trilha estilo Depeche Mode).
  - `video/icepol_journey_complete.mp4` (36s) e `video/langfuse_metrics_decision_tree.mp4` (36s).

---

## [v1.1.0] - 2026-09-15
### Adicionado
- **Diagramas Interativos Mermaid no Chat**:
  - Renderização automática de diagramas Mermaid (`erDiagram`, `graph TD`, `sequenceDiagram`) em formato SVG de alta resolução no tema escuro.
  - Aba dedicada `📐 Diagrama Mermaid` ao lado dos resultados analíticos do DuckDB.
  - Sanitização inteligente de sintaxe Mermaid (`sanitizeMermaidCode`) e fallback resiliente.
  - Correção estrita para notação *Crow's foot* (`||--o{`, `}|--|{`) evitando que atributos colunas virassem nós isolados.
- **Melhorias de Interatividade no Chat**:
  - Nova saudação de boas-vindas: *"Como posso ajudar com sua pesquisa hoje?"*.
  - Seletor dinâmico de modelos LLM locais (listando `llama3.2:3b`, `deepseek-r1:1.5b`, `qwen2.5:1.5b`).
  - Placeholder dinâmico no input: `Peça ao <modelo_selecionado>`.
  - Botão `+` para anexo de arquivos e imagens com pré-visualização e remoção de tags.
  - Botão de microfone funcional com transcrição de voz em tempo real via Web Speech API.

---

## [v0.4.0] - 2026-09-14
### Adicionado
- **Licenciamento Open Source**: Adicionado arquivo [`LICENSE`](file:///Users/mauriciohelfstein/dev/icepol-semantic/LICENSE) (MIT License).
- **Modelagem de Domínio Expandida (7 Tabelas Físicas)**:
  - `financial_statements` (Demonstrativos Financeiros, Dívida Líquida, EBITDA).
  - `credit_limits` (Limites Globais Aprovados vs Utilizados).
  - `covenants` (Cláusulas Contratuais e Status de Desenquadramento).
- **Novas Métricas Semânticas**:
  - `avg_net_debt_ebitda` (Alavancagem Financeira Média).
  - `total_approved_credit_limit` (Volume Global de Limite de Crédito).
  - `credit_limit_utilization_rate` (Taxa de Utilização de Limite).
  - `covenant_breach_rate` (Taxa de Descumprimento de Covenants).
- **Diagrama Visual Interativo SVG para AWS Cloud**:
  - Adicionado [`docs/aws_architecture.svg`](file:///Users/mauriciohelfstein/dev/icepol-semantic/docs/aws_architecture.svg) integrado diretamente no `README.md`.
- **Carga de Dados Sintéticos**: `seed_iceberg.py` atualizado para 7 parquets analíticos.

---

## [v0.3.0] - 2026-09-14
### Adicionado
- **Expansão do Modelo Ontológico**: Adicionadas as entidades `collateral` (garantias/colaterais) e `credit_proposal` (propostas de crédito).
- **Novas Métricas de Crédito**: `total_collateral_value`, `ltv_ratio`, `total_proposed_amount`, `proposal_approval_rate`.
- **Carga de Dados Sintéticos**: Atualização do `seed_iceberg.py` para gerar e popular as 4 tabelas de Crédito Corporativo.
- **Portabilidade para Nuvem AWS**: Documentação de arquitetura no `README.md`.

---

## [v0.2.0] - 2026-09-14
### Adicionado
- **Model Context Protocol (MCP) Server**: Implementado `core/mcp_server.py` utilizando FastMCP.
- **Ferramentas MCP**: `query_llama`, `execute_semantic_sql`, `get_semantic_ontologies`.
- **Integração Docker & Configuração**: Serviço `mcp-server` no `docker-compose.yml` e `mcp_config.json`.

---

## [v0.1.0] - 2026-09-14
### Adicionado
- **Estrutura Base do Ecossistema**: MinIO (S3), Apache Polaris (Iceberg REST Catalog), DuckDB (Engine), `llama.cpp` (LLM) e Open WebUI (Frontend).
- **Parser Semântico**: Leitor YAML e compilador AST de métricas/dimensões (`semantic/parser.py`).
- **Middleware Agent**: Servidor FastAPI (`core/agent.py`) integrando Open WebUI e `llama.cpp`.
- **Automação**: `Makefile` e `docker-compose.yml`.
