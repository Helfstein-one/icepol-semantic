# CHANGELOG

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

## [v1.4.0] - 2026-09-16
### Limpeza & Otimização
- **Consolidação do Vídeo Oficial & Limpeza Total de Mídia**:
  - Remoção de todos os arquivos temporários do recorder (`video/recorder/`), sintetizadores Python (`synth_*.py`), trilhas brutas não compactadas (`soundtrack_*.wav`) e vídeos intermediários.
  - Manutenção exclusiva de [`video/icepol_user_journey.mp4`](video/icepol_user_journey.mp4) como o vídeo oficial e definitivo do projeto.
  - Gravação estendida de 85 segundos em Full HD 1080p, cobrindo a navegação completa no GitHub até o rodapé, terminal com `make seed`, Chat UI com seletor de modelos e diagrama Mermaid ERD, e login no Langfuse com a Árvore de Decisão / DAG e decomposição de custos de tokens.
  - Trilha sonora Eurodance 90s (*What Is Love* a 125 BPM) integrada em áudio AAC de alta fidelidade.

## [v1.3.0] - 2026-09-16
### Otimizado
- **Consolidação de Banco de Dados no PostgreSQL 15**:
  - Eliminação do container redundante `mysql:8.0` (`mysql-db`), liberando mais de 500 MB de memória RAM no host.
  - Migração da tabela `query_metrics` para o PostgreSQL 15 (`postgres-langfuse`) nativo, unificando a persistência de observabilidade e telemetria em um único SGBD.
  - Driver Python atualizado para `psycopg2-binary>=2.9.9` com queries compatíveis e resilientes.
  - Interface Web atualizada com telemetria `🐘 PostgreSQL 15 Audit` na porta `:5432`.

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
- **Documentação de Observabilidade & Diagramas Mermaid**:
  - **Árvore de Decisão do Tracing (DAG)**: Diagrama em fluxo direcionado conectando Prompt &rarr; Semantic Parser &rarr; DeepSeek-R1 (CoT) &rarr; AST Validator &rarr; DuckDB &rarr; MinIO/MySQL 8.
  - **Waterfall de Spans (Gráfico Gantt)**: Decomposição temporal precisa da latência total (1.492ms) evidenciando spans de ciclo de vida e tempo de resposta de cada serviço.
  - **Gráfico de Distribuição de Tokens (Pie Chart)**: Mapeamento da eficiência de 342 tokens (63.7% contexto ontológico, 21.0% raciocínio CoT e 15.3% síntese SQL ANSI).
- **Produção de Vídeos Demonstrativos em Full HD 1080p e Novas Trilhas Sonoras**:
  - `video/icepol_user_journey_daft_punk.mp4` (60s): **Gravação Real da Tela com Trilha Estilo 'Around the World / Harder Better Faster' (Daft Punk)** — 123 BPM em Mi menor (Em), reproduzindo a estética French House com baixo funk slap (Chic style), batida 909 com open hi-hats sincopados nos contratempos, stabs de guitarra disco funk com phaser e vocoder robótico.
  - `video/soundtrack_daft_punk_60s.wav`: Trilha sonora sintetizada de 60 segundos com arranjo paramétrico em áudio PCM 44.1kHz.
  - `video/synth_daft_punk.py`: Script gerador paramétrico em áudio WAV estéreo.
  - `video/icepol_user_journey_sweet_dreams.mp4` (60s): **Gravação Real da Tela com Trilha Estilo 'Sweet Dreams' (Eurythmics)** — 125 BPM em Dó menor (Cm), com arpejo analógico no Roland SH-101 e bateria industrial.
  - `video/soundtrack_sweet_dreams_60s.wav`: Trilha sonora sintetizada de 60 segundos com arranjo paramétrico em áudio PCM 44.1kHz.
  - `video/synth_sweet_dreams.py`: Script gerador paramétrico em áudio WAV estéreo.
  - `video/icepol_user_journey.mp4` (60s): **Gravação Real da Tela (Screen Recording) com Trilha Estilo 'Take On Me' (A-ha)** — 168 BPM em Si menor (Bm), gravado em tempo real com automação de cursor do mouse, efeito visual ripple de cliques, scroll fluido pelo GitHub oficial, digitação humana no terminal e no chat da camada semântica e inspeção do Langfuse.
  - `video/soundtrack_take_on_me_60s.wav`: Trilha sonora sintetizada de 60 segundos com arranjo paramétrico fiel ao clássico do A-ha.
  - `video/synth_take_on_me.py`: Script gerador paramétrico em áudio PCM WAV estéreo 44.1kHz.
  - `video/recorder/record_live_screen.js`: Script de automação e gravação contínua de tela em 1080p via Playwright e Chromium.
  - Roteiro cobrindo navegação no repositório GitHub com scroll do README, clone no terminal, execução de `make seed` e subida com Podman Compose, chat com consultas de crédito corporativo, modelagem conceitual Mermaid ERD (Crow's foot com as 7 entidades), tracing detalhado no Langfuse e decomposição de custos de tokens (evidenciando contexto ontológico de 218 tokens como maior volume e raciocínio CoT de 776ms como maior tempo de execução).
- **Limpeza e Otimização do Repositório**:
  - Remoção definitiva de todos os vídeos antigos e intermediários, mantendo unicamente o vídeo oficial gravado em tela [`video/icepol_user_journey.mp4`](file:///Users/mauriciohelfstein/dev/icepol-semantic/video/icepol_user_journey.mp4).

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
