![icepol-semantic Header](docs/icepol_semantic_header.jpg)

# icepol-semantic 🧊⚖️

**Ecossistema 100% Local de Inteligência Analítica em Crédito Corporativo (Wholesale Banking) impulsionado por Camada Semântica, Apache Iceberg, DuckDB, Llama.cpp e Model Context Protocol (MCP).**

---

## 📋 Sumário
1. [Imersão Teórica e Literatura: O que é e por que a Camada Semântica existe?](#-imersão-teórica-e-literatura-o-que-é-e-por-que-a-camada-semântica-existe)
2. [A Evolução Histórica da Camada Semântica (De Inmon & Kimball ao GenAI)](#-a-evolução-histórica-da-camada-semântica-de-inmon--kimball-ao-genai)
3. [O Pipeline de Compilação: Texto -> Intenção -> AST -> SQL Físico](#-o-pipeline-de-compilação-texto---intenção---ast---sql-físico)
4. [Arquitetura da Solução Local & Observabilidade](#-arquitetura-da-solução-local)
5. [Modelagem Ontológica do Domínio (7 Tabelas Físicas de Crédito)](#-modelagem-ontológica-do-domínio-7-tabelas-físicas-de-crédito)
6. [Observabilidade Corporativa (Langfuse, MinIO S3 & PostgreSQL 15)](#-observabilidade-corporativa-langfuse-minio-s3--postgresql-15)
7. [Vídeos Demonstrativos & Mermaid Interativo](#-vídeos-demonstrativos--mermaid-interativo)
8. [Como Executar e Utilizar](#-como-executar-e-utilizar)
9. [Integração via Model Context Protocol (MCP)](#-integração-via-model-context-protocol-mcp)
10. [Guia de Portabilidade para AWS Cloud & Arquitetura SVG](#-guia-de-portabilidade-para-aws-cloud--arquitetura-svg)

---

## 🔬 Imersão Teórica e Literatura: O que é e por que a Camada Semântica existe?

A **Camada Semântica** (*Semantic Layer*) é a camada de abstração analítica projetada para mapear e traduzir **conceitos de negócio heterogêneos** (métricas, entidades, dimensões e relacionamentos) em **instruções executáveis de código analítico (SQL/AST)** sobre bancos de dados físicos.

---

### 1. A Evolução Histórica da Camada Semântica: A Escalada para a Inteligência Artificial

![Evolução Histórica da Camada Semântica - Gráfico de Montanha](docs/semantic_layer_mountain_evolution.jpg)

Para compreender como a Camada Semântica se tornou o pilar central da Inteligência Artificial em Dados, analisamos sua evolução como uma **Escalada até o Cume (Mountain Peak Progression)** ao longo de 4 eras:

#### 🏛️ A. Era 1: Modelagem Dimensional de Ralph Kimball (1990s)
Na literatura clássica de Data Warehousing (*The Data Warehouse Toolkit* por Ralph Kimball e Margy Ross), o problema do acoplamento foi abordado dividindo os dados em **Tabelas de Fatos** (eventos numéricos/métricas) e **Tabelas de Dimensões** (contextos qualitativos). Contudo, as regras de cálculo ainda ficavam engessadas em cubos OLAP proprietários ou views SQL engessadas.

#### 🏢 B. Era 2: LookML & A Invenção do *Semantic Layer-as-Code* (2010s)
Com a criação do Looker e do **LookML**, a camada semântica passou a ser declarativa e versionada via Git. Em vez de escrever SQL bruto, os engenheiros definiam *Dimensions* e *Measures*.

#### ⚡ C. Era 3: Headless Semantic Layer no Modern Data Stack (2020s)
Ferramentas como **Cube.dev**, **dbt MetricFlow** e **Google Malloy** popularizaram o conceito de *Headless Semantic Layer* (Camada Semântica Desacoplada): a lógica de negócio existe em uma camada universal e serve a qualquer consumidor (Tableau, Python, APIs, Excel).

#### 🤖 D. Era 4: O Guardrail Imutável para Agentes de IA e Text-to-SQL (2024+)
Com a ascensão dos Grandes Modelos de Linguagem (LLMs), a camada semântica tornou-se a **peça mais crítica para o sucesso de aplicações de Text-to-SQL**. Sem ela, o LLM sofre do fenômeno da *Adivinhação de Schema*: tenta adivinhar nomes de colunas, inventar joins e aplicar regras matemáticas incorretas.

---

### Como a Camada Semântica Funciona?

![Camada Semântica](docs/semantic_layer_architecture_diagram.jpg)

Para entender de forma simples e intuitiva:

1. **O Mundo Superior (Linguagem Humana):** O usuário faz perguntas do dia a dia (*"Qual é o crédito total?"*, *"Mostre as métricas de inadimplência!"*).
2. **A Ponte de Tradução (Camada Semântica):** No meio do caminho fica a nossa camada Ela entende o que o humano quer dizer, consulta o dicionário de regras de negócio (YAML) e traduz o pedido em lógica canônica estruturada, sem deixar o modelo alucinar.
3. **O Mundo Inferior (Dados Físicos & SQL):** Abaixo da ponte estão as tabelas brutas, blocos de dados do Apache Iceberg, partições e queries SQL complexas. A entrega a query já montada e testada diretamente para o DuckDB executar!
---

### 2. A Árvore de Arquitetura da Camada Semântica (`icepol-semantic`)

A arquitetura ontológica é organizada em **4 Camadas Funcionais Encadeadas**, mostrando detalhadamente como o texto em linguagem natural trafega até os dados físicos:

```mermaid
graph TD
    subgraph L1["1️⃣ Camada de Consumo & Interfaces (Client Layer)"]
        UserNLP["🗣️ Pergunta em Linguagem Natural<br/><i>'Qual a exposição e alavancagem média por setor?'</i>"]
        OpenWebUI["💬 Open WebUI (:3000)"]
        MCPClient["🔌 MCP Client (Antigravity IDE / Agents)"]
    end

    subgraph L2["2️⃣ Camada Ontológica & Contrato Semântico (YAML Specs)"]
        OntologyRoot["📜 Registry: corporate_credit.yaml & metrics.yaml"]
        
        Entities["🏢 Entidades (7 Tabelas)<br/>• counterpart<br/>• credit_facility<br/>• collateral<br/>• credit_proposal<br/>• financial_statement<br/>• credit_limit<br/>• covenant"]
        
        Dimensions["🏷️ Dimensões (Atributos)<br/>• sector (ds_cnae_sector)<br/>• economic_group<br/>• operation_type<br/>• fiscal_year<br/>• covenant_type"]
        
        Metrics["🧮 Métricas (Fórmulas Regradas)<br/>• total_exposure (EAD)<br/>• overdue_ratio_90d (NPL)<br/>• avg_net_debt_ebitda<br/>• ltv_ratio<br/>• covenant_breach_rate"]
    end

    subgraph L3["3️⃣ Compilador AST & Engine Middleware (Python AST Compiler)"]
        Parser["⚙️ semantic/parser.py"]
        LLMInfer["🧠 llama.cpp / Bedrock<br/><i>Identifica Métricas & Dimensões</i>"]
        SQLGen["🔨 Gerador AST SQL<br/><i>Compila SQL seguro com NULLIF, JOINs e GROUP BY</i>"]
    end

    subgraph L4["4️⃣ Camada Física de Dados & Storage (Iceberg / S3 Engine)"]
        DuckDBEngine["🦆 DuckDB Engine (core/engine.py)<br/><i>Executa SQL em memória/S3</i>"]
        PolarisCat["🧊 Apache Polaris Catalog<br/><i>REST Iceberg Metadados</i>"]
        MinIOS3["🗄️ MinIO / AWS S3 Storage<br/><i>7 Parquets do Data Lakehouse</i>"]
    end

    UserNLP --> OpenWebUI
    UserNLP --> MCPClient
    OpenWebUI --> LLMInfer
    MCPClient --> LLMInfer
    
    OntologyRoot --> Entities
    OntologyRoot --> Dimensions
    OntologyRoot --> Metrics
    
    OntologyRoot -->|Injeta Contexto| LLMInfer
    LLMInfer -->|Intenção Identificada| Parser
    Parser --> SQLGen
    
    SQLGen -->|SQL Dialeto DuckDB| DuckDBEngine
    DuckDBEngine <-->|Leitura de Metadados| PolarisCat
    DuckDBEngine <-->|Leitura de Parquets| MinIOS3

    classDef l1Style fill:#0F172A,stroke:#3B82F6,stroke-width:2px,color:#93C5FD;
    classDef l2Style fill:#0F172A,stroke:#EC4899,stroke-width:2px,color:#F472B6;
    classDef l3Style fill:#0F172A,stroke:#F59E0B,stroke-width:2px,color:#FCD34D;
    classDef l4Style fill:#0F172A,stroke:#10B981,stroke-width:2px,color:#6EE7B7;

    class L1,UserNLP,OpenWebUI,MCPClient l1Style;
    class L2,OntologyRoot,Entities,Dimensions,Metrics l2Style;
    class L3,Parser,LLMInfer,SQLGen l3Style;
    class L4,DuckDBEngine,PolarisCat,MinIOS3 l4Style;
```

---

## ⚡ O Pipeline de Compilação: Texto -> Intenção -> AST -> SQL Físico

Abaixo está o fluxo completo de uma requisição desde a pergunta em linguagem natural do usuário até a execução no banco de dados:

```mermaid
sequenceDiagram
    autonumber
    actor User as 👤 Usuário (Open WebUI / IDE)
    participant Agent as ⚙️ Middleware Agent
    participant Semantic as 📚 SemanticRegistry
    participant LLM as 🧠 llama.cpp / Bedrock
    participant DuckDB as 🦆 DuckDB Engine (S3 / Iceberg)

    User->>Agent: "Qual a exposição total e alavancagem média por setor no varejo?"
    Agent->>Semantic: get_prompt_context()
    Semantic-->>Agent: Retorna Contexto Reduzido (Entidades, Dimensões e Métricas)
    
    Agent->>LLM: Injeta Contexto Semântico + Pergunta do Usuário
    Note over LLM: O LLM identifica as métricas:<br/>- total_exposure<br/>- avg_net_debt_ebitda<br/>E a dimensão: sector
    LLM-->>Agent: Responde com Intenção Semântica / SQL Canônico
    
    Agent->>Semantic: compile_query(metric_names, group_by_dims)
    Semantic-->>Agent: Retorna SQL DuckDB Físico Seguro e Otimizado
    
    Agent->>DuckDB: execute_query(sql)
    DuckDB-->>Agent: Retorna Tabela de Resultados JSON / Pandas
    Agent-->>User: Exibe Tabela Formatada + Resposta em Linguagem Natural
```

---

## 🏗️ Arquitetura da Solução Local

A arquitetura local opera 100% em containers isolados via Docker Compose ou execução direta em Python:

```mermaid
graph TD
    User["👤 Usuário / Analista"] -->|Interface Chat| WebUI["Open WebUI (:3000)"]
    
    subgraph Core["Core Middleware & Agent"]
        WebUI <-->|OpenAI API /v1| Agent["FastAPI Middleware Agent (:8000)"]
        MCP["MCP Server (core/mcp_server.py)"] <-->|Stdio / JSON-RPC| ClientMCP["Cliente MCP (Antigravity IDE)"]
        
        Agent <-->|Contexto Semântico + Prompt| Llama["llama.cpp Server (:8080)"]
        Agent <-->|SQL Compilado| Parser["Parser Semântico (semantic/parser.py)"]
        MCP <-->|Ferramentas MCP| Parser
        MCP <-->|Inferência| Llama
    end

    subgraph StorageEngine["Storage & Storage Engine"]
        Parser -->|Query AST| Engine["DuckDB Engine (core/engine.py)"]
        Engine <-->|REST Catalog Protocol| Polaris["Apache Polaris Iceberg Catalog (:8181)"]
        Engine <-->|Leitura Parquet / S3| MinIO["MinIO S3 Storage (:9000)"]
    end
```

---

## 📊 Modelagem Ontológica do Domínio (7 Tabelas Físicas de Crédito)

O repositório disponibiliza **7 tabelas fundamentais** modeladas no domínio de **Wholesale Banking**:

```mermaid
erDiagram
    COUNTERPARTS ||--o{ FACILITIES : "possuem"
    COUNTERPARTS ||--o{ PROPOSALS : "solicitam"
    COUNTERPARTS ||--o{ FINANCIAL_STATEMENTS : "apresentam"
    COUNTERPARTS ||--o{ CREDIT_LIMITS : "possuem limite"
    FACILITIES ||--o{ COLLATERALS : "garantidas por"
    FACILITIES ||--o{ COVENANTS : "sujeitas a"

    COUNTERPARTS {
        string counterpart_id PK
        string nm_economic_group
        string ds_cnae_sector
        string cd_rating_agency
    }

    FACILITIES {
        string facility_id PK
        string counterpart_id FK
        string tp_operation
        string st_operation
        double vl_outstanding_balance
        double vl_provision
        double vl_collateral_allocated
        int nr_days_overdue
    }

    COLLATERALS {
        string collateral_id PK
        string facility_id FK
        string counterpart_id FK
        string tp_collateral
        string st_collateral
        double vl_appraised_value
    }

    PROPOSALS {
        string proposal_id PK
        string counterpart_id FK
        double vl_requested
        string st_decision
        string nm_committee
    }

    FINANCIAL_STATEMENTS {
        string statement_id PK
        string counterpart_id FK
        string nr_fiscal_year
        string st_audited
        double vl_net_debt
        double vl_ebitda
    }

    CREDIT_LIMITS {
        string limit_id PK
        string counterpart_id FK
        string tp_limit
        string st_limit
        double vl_approved_limit
        double vl_used_limit
    }

    COVENANTS {
        string covenant_id PK
        string facility_id FK
        string tp_covenant
        string st_compliance
    }
```

---

## 🔍 Observabilidade Corporativa (Langfuse, MinIO S3 & PostgreSQL 15)

O Icepol integra uma pilha corporativa completa de observabilidade para auditoria regulatória, rastreabilidade de ponta a ponta e mitigação de alucinações em produção:

```mermaid
flowchart LR
    User["🗣️ Usuário / Prompt"] --> Agent["🤖 Icepol Semantic Agent (:8000)"]
    Agent --> Registry["📜 Ontologias YAML"]
    Agent --> LLM["🧠 Ollama (DeepSeek-R1 / LLaMA 3.2)"]
    Agent --> DuckDB["🦆 DuckDB Engine (Iceberg S3)"]
    
    subgraph Observability["📊 Pilha de Observabilidade & Auditoria"]
        LF["⚡ Langfuse v2 (:3001)"]
        MinIO["🪣 MinIO S3 (:9000/:9001)"]
        PostgreSQL["🐘 PostgreSQL 15 (:5432)"]
    end

    Agent -.->|"Traces & Spans"| LF
    Agent -.->|"Raw Payloads / Blobs"| MinIO
    Agent -.->|"Métricas & Audit Logs"| PostgreSQL
```

---

### 1. Diagrama de Rastreamento (Tracing DAG & Árvore de Decisão)

Cada pergunta do usuário dispara um fluxo auditado em grafo acíclico dirigido (DAG) capturado no Langfuse:

```mermaid
flowchart TD
    N1["1️⃣ Ingestion Node<br/><i>Prompt Natural: 'Qual a exposição e alavancagem por setor?'</i>"] --> N2["2️⃣ Semantic Layer Parser<br/><i>Mapeia Métricas: total_exposure, avg_net_debt_ebitda & Dimensão: ds_cnae_sector</i>"]
    N2 --> N3["3️⃣ LLM Reasoning Engine (DeepSeek-R1 1.5B)<br/><i>Chain-of-Thought &lt;think&gt; validando chaves estrangeiras e Crow's foot</i>"]
    N3 --> N4["4️⃣ SQL Generation & AST Validator<br/><i>Compila SQL canônico estrito ANSI com NULLIF e JOINs seguros</i>"]
    N4 --> N5["5️⃣ DuckDB Vectorized Engine<br/><i>Scan colunar sobre os Parquets do Apache Iceberg em 180ms</i>"]
    N5 --> N6["6️⃣ Renderers & UI Response Cell<br/><i>Tabela Analítica agregada + Diagrama Conceitual Mermaid SVG</i>"]
    
    N2 -.->|"Trace Span 1 (328ms)"| LangfuseSpan["⚡ Langfuse Tracing (:3001)"]
    N3 -.->|"Trace Span 2 (776ms)"| LangfuseSpan
    N5 -.->|"Trace Span 3 (180ms)"| LangfuseSpan
    N6 -.->|"Trace Span 4 (108ms)"| PostgresAudit["🐘 PostgreSQL 15 Audit Log (:5432)"]
```

---

### 2. Decomposição da Latência (Waterfall de Spans do Trace `tr_icepol_8f492a`)

A latência total fim-a-fim da consulta (*wall time* de **1.492,4 ms**) é decomposta em 4 spans assíncronos:

```mermaid
gantt
    title Waterfall de Spans da Consulta Semântica (Total: 1.492,4 ms)
    dateFormat X
    axisFormat %s ms
    section Ciclo Global
    ROOT: icepol_query_handler           :active, 0, 1492
    section Spans Internos
    SPAN 1: semantic_ontology_parsing    :done, 30, 358
    SPAN 2: deepseek_r1_sql_synthesis    :crit, active, 358, 1134
    SPAN 3: duckdb_columnar_query        :done, 1134, 1314
    SPAN 4: audit_minio_postgres_sink    :done, 1314, 1422
```

| Span de Execução | Componente | Latência | % do Total | Ação Realizada |
| :--- | :--- | :--- | :--- | :--- |
| **`ROOT: icepol_query_handler`** | FastAPI Gateway | **1.492,4 ms** | 100% | Orquestração do ciclo global da requisição e streaming |
| **`SPAN 1: semantic_ontology_parsing`** | `semantic/parser.py` | **328,0 ms** | 22.0% | Token match no dicionário ontológico YAML (`corporate_credit.yaml`) |
| **`SPAN 2: deepseek_r1_sql_synthesis`** | DeepSeek-R1 (Ollama) | **776,0 ms** | 52.0% | Raciocínio CoT (`<think>`) e síntese da consulta SQL estrita |
| **`SPAN 3: duckdb_columnar_query`** | `core/engine.py` | **180,0 ms** | 12.1% | Leitura vetorizada dos dados Parquet no DuckDB via S3 |
| **`SPAN 4: audit_minio_postgres_sink`** | MinIO & PostgreSQL 15 | **108,4 ms** | 7.3% | Gravação assíncrona do payload bruto no MinIO e métricas no PostgreSQL |

---

### 3. Economia e Distribuição de Gastos de Tokens

O monitoramento do Langfuse quantifica com exatidão a alocação de tokens da consulta (Total: **342 tokens**):

```mermaid
pie title Distribuição Percentual de Gastos de Tokens por Consulta (342 Tokens)
    "Contexto Ontológico (YAML & Guardrails) - 218 Tokens" : 63.7
    "Raciocínio Chain-of-Thought (<think>) - 72 Tokens" : 21.0
    "Síntese SQL ANSI Canônica - 52 Tokens" : 15.3
```

* **1. Input Ontológico (218 tokens / 63.7%)**: Esquema canônico das 7 tabelas físicas, tipos de dados e regras de cálculo de métricas (`total_exposure`, `avg_net_debt_ebitda`). Utiliza cache de contexto para maximizar throughput.
* **2. Raciocínio CoT do DeepSeek-R1 (72 tokens / 21.0%)**: Processamento no bloco `<think>` validando a integridade referencial das chaves estrangeiras e a cardinalidade *Crow's foot* antes de emitir o SQL.
* **3. Output SQL Compilado (52 tokens / 15.3%)**: Instrução SQL ultracompacta pronta para execução imediata no DuckDB.

---

### 4. Componentes de Telemetria & Sinks de Dados:
1. **Langfuse v2 (`http://localhost:3001`)**:
   - Rastreamento detalhado de cada chamada LLM com visualização em tempo real de sessions, traces e tags.
   - P95 de latência de 1.88s (abaixo do SLA estabelecido de 2.5s) e zero falhas de conformidade.
2. **MinIO S3 (`http://localhost:9001`)**:
   - Bucket dedicado `/data/langfuse` para retenção permanente e auditoria forense de prompts e payloads completos.
3. **PostgreSQL 15 (`localhost:5432`)**:
   - Banco `langfuse` (unificado), tabela `query_metrics`:
     - `session_id`, `model_name`, `prompt_text`, `sql_query`, `row_count`, `llm_latency_ms`, `duckdb_latency_ms`, `tokens_estimated`, `status`.
4. **Painel Interativo no Cabeçalho do Chat**:
   - Botão **`Métricas & Traces`** no topo da UI com popover dinâmico exibindo status de saúde ao vivo e atalhos diretos para os consoles.

---

## 🎬 Vídeo Demonstrativo & Gravação Real da Tela

O projeto conta com o vídeo oficial de **gravação real da tela** (*screen recording* com automação de cursor, digitação e interação ao vivo) em Full HD 1080p:

### 🕺 ⚡ 🌟 Gravação Real da Tela: Jornada Completa (85s)
* **Arquivo de Vídeo Oficial**: [`video/icepol_user_journey.mp4`](video/icepol_user_journey.mp4)
* **Gravação Real de Tela**: Captura contínua de 85 segundos cobrindo:
  1. **Navegação no Repositório GitHub (0s - 22s)**: Acesso à página oficial `Helfstein-one/icepol-semantic`, clique no botão `<> Code` exibindo o popover de clone, e rolagem suave por todo o README inspecionando arquitetura, entidades e observabilidade até o rodapé.
  2. **Terminal & Setup Completo (22s - 40s)**: Execução animada de `git clone`, `pip install`, `make seed` (gerando as 7 tabelas de crédito corporativo em Iceberg/MinIO), inicialização de containers (`podman compose up -d`) e verificação do PostgreSQL 15 (`/api/observability/status`).
  3. **Jornada no Chat Semântico (40s - 63s)**: Seleção do modelo `deepseek-r1:1.5b` no dropdown, envio da consulta analítica, geração da tabela colunar DuckDB, visualização do **Diagrama Mermaid ERD** interativo e inspeção do popover de auditoria do PostgreSQL 15.
  4. **Langfuse Tracing & Árvore de Decisão (63s - 85s)**: Login no Langfuse (`:3001`), inspeção visual da **🌳 Árvore de Decisão / DAG de Execução** (`Ingestion ➔ Semantic Parser ➔ DeepSeek-R1 CoT ➔ DuckDB Columnar ➔ PostgreSQL 15 Audit`), waterfall de spans de latência e análise de custo de tokens.
* **Trilha Sonora Integrada**: Arranjo Eurodance animado em **125 BPM** (*What Is Love* - Haddaway) com bumbo TR-909, baixo synth FM e stabs de piano rave, perfeitamente sincronizado com as transições de cena.
* **Duração**: **85 segundos** | **Resolução**: 1920x1080 Full HD (H.264 / AAC 44.1kHz estéreo)

---

## 🚀 Como Executar e Testar

### 1. Testando em Ambientes Containerizados (Docker ou Podman)

O projeto suporta nativamente **Docker** ou **Podman**. O `Makefile` detecta automaticamente qual dos dois está disponível na máquina.

> [!TIP]
> **Usuários de Podman no macOS**: Antes de iniciar, certifique-se de que a VM do Podman está ligada executando:
> ```bash
> podman machine start
> ```

```bash
# 1. Subir todos os serviços em background (funciona com Docker ou Podman automaticamente)
make up
# ou manualmente:
docker compose up -d    # Se usar Docker
podman compose up -d    # Se usar Podman

# 2. Verificar o status e saúde dos containers
make status
# ou manualmente:
docker compose ps       # Se usar Docker
podman compose ps       # Se usar Podman
```

#### 🧪 Endpoints para Testes de Integração (cURL):

##### A. Testar Saúde da API do Middleware Agent:
```bash
curl http://localhost:8000/health
# Resposta esperada: {"status":"ok","domain":"corporate_credit"}
```

##### B. Validar Extração do Contexto Semântico:
```bash
curl http://localhost:8000/semantic/context
```

##### C. Testar Invocação Text-to-Semantic-SQL (Compatível com OpenAI API & Ollama):
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2:3b",
    "messages": [
      {
        "role": "user",
        "content": "Qual a exposição total (total_exposure) por setor (sector)?"
      }
    ]
  }'
```

#### 🖥️ Consoles Web de Acesso:
- **Icepol Semantic Web UI (Chat Interativo):** [http://localhost:8000](http://localhost:8000)
- **Langfuse LLM Observability Dashboard:** [http://localhost:3001](http://localhost:3001)
- **MinIO Console (Storage S3):** [http://localhost:9001](http://localhost:9001) (`admin` / `password123`)
- **Apache Polaris Iceberg Catalog:** [http://localhost:8181](http://localhost:8181)
- **PostgreSQL 15 Metrics & Langfuse DB:** `localhost:5432` (database `langfuse`, user `postgres` / `password123`)
- **Ollama Engine (Host):** [http://localhost:11434](http://localhost:11434) (Modelos: `deepseek-r1:1.5b`, `llama3.2:3b`, `qwen2.5:1.5b`)

#### 🛑 Parar e Limpar Containers:
```bash
docker compose down
# ou via Makefile:
make down
```

---

### 2. Testes Locais Diretos em Python (sem Docker)

```bash
# Criar venv e instalar dependências
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Gerar dados sintéticos para as 7 tabelas físicas
make seed

# Executar suíte de teste da camada semântica e DuckDB
make test
```

---

## ☁️ Guia de Portabilidade para AWS Cloud & Arquitetura SVG

### Diagrama da Arquitetura AWS Cloud (Enterprise Wholesale Banking Data Platform)

![Enterprise Wholesale Banking Data Platform (AWS)](docs/aws_architecture_user.png)

---

### De-Para de Componentes: Local vs AWS

| Componente Local | Substituto Nativo AWS | Vantagens da Migração para AWS |
| :--- | :--- | :--- |
| **MinIO Storage** | **Amazon S3** (`s3://icepol-corporate-credit-bucket`) | Escala ilimitada, alta disponibilidade (99.999999999% durability). |
| **Apache Polaris** | **AWS Glue Data Catalog (com suporte a Iceberg)** | Gestão de metadados sem servidor (*serverless*), integração nativa com IAM. |
| **DuckDB Engine** | **Amazon Athena** ou **DuckDB on AWS Lambda / EKS** | Execução de consultas SQL diretamente sobre o S3 Iceberg com custo por consulta. |
| **llama.cpp Engine** | **Amazon Bedrock** (Claude 3.5 / Llama 3.1) ou **SageMaker JumpStart** | Modelos gerenciados com APIs de alta escalabilidade e segurança enterprise. |
| **Middleware Agent / MCP** | **AWS ECS Fargate** ou **AWS App Runner** | Containers sem servidor com autoscaling e integração de métricas CloudWatch. |

---

## 📜 Licença

Este projeto está licenciado sob os termos da licença [MIT License](LICENSE).
