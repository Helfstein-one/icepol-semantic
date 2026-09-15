# CHANGELOG

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

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
