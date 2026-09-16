import os
import subprocess

pwd = os.path.abspath(os.curdir)
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ffmpeg = "/opt/homebrew/bin/ffmpeg"

def capture_html(html_path, out_png):
    file_url = f"file://{pwd}/{html_path}"
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--window-size=1920,1080",
        f"--screenshot={out_png}",
        file_url
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"Captured: {out_png}")

# SCENE 1: Terminal with All Services (including MySQL, Postgres, Langfuse)
scene1_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Terminal - Build & Launch</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 flex items-center justify-center min-h-screen p-8 font-mono antialiased">
    <div class="w-full max-w-5xl bg-[#0d1117] border border-slate-700/80 rounded-2xl shadow-2xl overflow-hidden">
        <div class="bg-[#161b22] px-4 py-3 border-b border-slate-800 flex items-center justify-between">
            <div class="flex items-center space-x-2">
                <span class="w-3 h-3 rounded-full bg-rose-500/90 inline-block shadow"></span>
                <span class="w-3 h-3 rounded-full bg-amber-500/90 inline-block shadow"></span>
                <span class="w-3 h-3 rounded-full bg-emerald-500/90 inline-block shadow"></span>
            </div>
            <div class="text-xs text-slate-400 font-medium tracking-wide">
                mauricio@MacBook-Air: ~/dev/icepol-semantic — zsh — 144x38
            </div>
            <div class="w-12"></div>
        </div>
        <div class="p-6 text-sm leading-relaxed space-y-2 text-slate-300">
            <div class="flex items-center gap-2">
                <span class="text-emerald-400 font-bold">➜</span>
                <span class="text-cyan-400 font-bold">icepol-semantic</span>
                <span class="text-purple-400 font-bold">git:(main)</span>
                <span class="text-white font-semibold">podman compose up -d</span>
            </div>
            <div class="pt-2 text-slate-300 space-y-1.5">
                <div class="flex items-center gap-2">
                    <span class="text-emerald-400 font-bold">✔</span>
                    <span class="text-slate-200 font-medium">Container <strong class="text-white">minio-storage</strong></span>
                    <span class="text-slate-500 text-xs font-mono">(S3 Lakehouse & Langfuse Blobs :9000, :9001)</span>
                    <span class="text-emerald-400 font-bold text-xs bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">Up 25h</span>
                </div>
                <div class="flex items-center gap-2">
                    <span class="text-emerald-400 font-bold">✔</span>
                    <span class="text-slate-200 font-medium">Container <strong class="text-white">polaris-catalog</strong></span>
                    <span class="text-slate-500 text-xs font-mono">(Apache Iceberg REST Metastore :8181)</span>
                    <span class="text-emerald-400 font-bold text-xs bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">Up 25h</span>
                </div>
                <div class="flex items-center gap-2">
                    <span class="text-emerald-400 font-bold">✔</span>
                    <span class="text-slate-200 font-medium">Container <strong class="text-white">mysql-db</strong></span>
                    <span class="text-slate-500 text-xs font-mono">(MySQL 8.0 Audit & Metrics :3306)</span>
                    <span class="text-emerald-400 font-bold text-xs bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">Healthy</span>
                </div>
                <div class="flex items-center gap-2">
                    <span class="text-emerald-400 font-bold">✔</span>
                    <span class="text-slate-200 font-medium">Container <strong class="text-white">postgres-langfuse</strong></span>
                    <span class="text-slate-500 text-xs font-mono">(PostgreSQL 15 Tracing DB :5432)</span>
                    <span class="text-emerald-400 font-bold text-xs bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">Healthy</span>
                </div>
                <div class="flex items-center gap-2">
                    <span class="text-emerald-400 font-bold">✔</span>
                    <span class="text-slate-200 font-medium">Container <strong class="text-white">langfuse-server</strong></span>
                    <span class="text-slate-500 text-xs font-mono">(Langfuse LLM Observability & Dashboard :3001)</span>
                    <span class="text-purple-400 font-bold text-xs bg-purple-500/10 px-2 py-0.5 rounded border border-purple-500/20">Ready</span>
                </div>
                <div class="flex items-center gap-2">
                    <span class="text-emerald-400 font-bold">✔</span>
                    <span class="text-slate-200 font-medium">Container <strong class="text-white">semantic-agent</strong></span>
                    <span class="text-slate-500 text-xs font-mono">(FastAPI + DuckDB + Langfuse Tracer :8000)</span>
                    <span class="text-emerald-400 font-bold text-xs bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">Running</span>
                </div>
            </div>
            <div class="pt-4 p-4 rounded-xl bg-slate-900/90 border border-slate-800 text-xs space-y-1.5 font-mono">
                <div class="text-emerald-300 font-bold flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    ICEPOL SEMANTIC LAYER & OBSERVABILITY INICIALIZADOS COM SUCESSO!
                </div>
                <div class="text-slate-400">
                    • Modelos LLM Conectados: <strong class="text-indigo-300">deepseek-r1:1.5b | qwen2.5:1.5b | llama3.2:3b</strong>
                </div>
                <div class="text-slate-400">
                    • Observabilidade Ativa: <strong class="text-purple-300">Langfuse (:3001)</strong> | <strong class="text-amber-300">MySQL (:3306)</strong> | <strong class="text-rose-300">MinIO (:9001)</strong>
                </div>
                <div class="text-slate-400">
                    • Interface Web: <span class="text-sky-400 underline font-bold">http://localhost:8000</span>
                </div>
            </div>
            <div class="flex items-center gap-2 pt-2">
                <span class="text-emerald-400 font-bold">➜</span>
                <span class="text-cyan-400 font-bold">icepol-semantic</span>
                <span class="text-purple-400 font-bold">git:(main)</span>
                <span class="text-slate-400">open http://localhost:8000</span>
                <span class="w-2 h-4 bg-sky-400 animate-pulse inline-block ml-1"></span>
            </div>
        </div>
    </div>
</body>
</html>"""

# SCENE 2: Icepol Home with new Logo and DeepSeek-R1 selected
scene2_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Icepol - Home</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-[#0e1117] text-slate-100 font-sans min-h-screen flex flex-col antialiased">
    <!-- Header -->
    <header class="border-b border-slate-800/80 bg-[#090d16]/80 backdrop-blur-md px-8 py-4 flex items-center justify-between sticky top-0 z-50">
        <div class="flex items-center gap-3.5">
            <div class="w-11 h-11 rounded-2xl bg-gradient-to-br from-sky-400 via-blue-600 to-indigo-700 p-0.5 shadow-lg shadow-sky-500/20">
                <div class="w-full h-full bg-slate-950 rounded-[14px] flex items-center justify-center">
                    <span class="text-2xl">❄️</span>
                </div>
            </div>
            <div>
                <div class="flex items-center gap-2">
                    <h1 class="text-xl font-bold tracking-tight bg-gradient-to-r from-sky-300 via-white to-blue-200 bg-clip-text text-transparent">Icepol</h1>
                    <span class="text-[10px] uppercase font-mono px-2 py-0.5 rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/20 font-semibold">Semantic</span>
                </div>
                <p class="text-xs text-slate-400">Camada Semântica & Copilot de Crédito</p>
            </div>
        </div>

        <!-- Badges -->
        <div class="flex items-center gap-3 text-xs">
            <div class="px-3.5 py-1.5 rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 flex items-center gap-2 font-mono">
                <span class="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-pulse"></span>
                <span>Modelo: <strong class="text-white">deepseek-r1:1.5b</strong></span>
            </div>
            <div class="px-3.5 py-1.5 rounded-full bg-blue-500/10 text-blue-300 border border-blue-500/20 flex items-center gap-2 font-mono">
                <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
                <span>DuckDB: <strong class="text-white">Ativo</strong></span>
            </div>
            <div class="px-3.5 py-1.5 rounded-full bg-purple-500/10 text-purple-300 border border-purple-500/30 flex items-center gap-2 font-mono">
                <span class="w-1.5 h-1.5 rounded-full bg-purple-400 animate-pulse"></span>
                <span>Métricas & Traces: <strong class="text-white">Langfuse + MySQL</strong></span>
            </div>
        </div>
    </header>

    <!-- Welcome Hero -->
    <main class="flex-1 flex flex-col items-center justify-center p-8 text-center space-y-8 max-w-4xl mx-auto">
        <div class="space-y-3">
            <h2 class="text-5xl font-bold tracking-tight bg-gradient-to-r from-sky-300 via-white to-indigo-300 bg-clip-text text-transparent">
                Olá, Mauricio
            </h2>
            <p class="text-2xl text-slate-400 font-normal">
                Como posso ajudar com sua pesquisa hoje?
            </p>
        </div>

        <div class="flex flex-wrap items-center justify-center gap-3 pt-2">
            <div class="px-5 py-3 rounded-full bg-slate-900/90 text-slate-200 border border-slate-700/70 text-sm font-medium shadow-md flex items-center gap-2">
                <span>📊 Exposição total por setor</span>
            </div>
            <div class="px-5 py-3 rounded-full bg-slate-900/90 text-slate-200 border border-slate-700/70 text-sm font-medium shadow-md flex items-center gap-2">
                <span>📈 Alavancagem por grupo econômico</span>
            </div>
            <div class="px-5 py-3 rounded-full bg-sky-950/60 text-sky-300 border border-sky-500/40 text-sm font-medium shadow-md flex items-center gap-2">
                <span>📐 Diagrama de Entidades (Mermaid)</span>
            </div>
        </div>

        <div class="w-full max-w-2xl bg-slate-900/90 border border-slate-700/80 rounded-3xl p-3 shadow-2xl flex items-center justify-between gap-3">
            <div class="flex items-center gap-3 pl-2">
                <button class="w-8 h-8 rounded-full bg-slate-800 text-slate-400 flex items-center justify-center font-bold text-lg">+</button>
                <div class="px-2.5 py-1 rounded-full bg-indigo-500/15 text-indigo-300 border border-indigo-500/30 text-xs font-mono font-semibold">
                    deepseek-r1:1.5b ⌵
                </div>
                <span class="text-slate-500 text-sm">Peça ao deepseek-r1:1.5b...</span>
            </div>
            <div class="flex items-center gap-2 pr-2">
                <button class="w-8 h-8 rounded-full bg-slate-800 text-slate-400 flex items-center justify-center">🎤</button>
                <button class="w-8 h-8 rounded-full bg-sky-500 text-slate-950 flex items-center justify-center font-bold">➔</button>
            </div>
        </div>
    </main>
</body>
</html>"""

# SCENE 3: Observability Popover Open
scene3_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Icepol - Observabilidade Popover</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-[#0e1117] text-slate-100 font-sans min-h-screen flex flex-col antialiased">
    <header class="border-b border-slate-800/80 bg-[#090d16]/80 px-8 py-4 flex items-center justify-between relative z-50">
        <div class="flex items-center gap-3">
            <div class="w-11 h-11 rounded-2xl bg-gradient-to-br from-sky-400 via-blue-600 to-indigo-700 p-0.5">
                <div class="w-full h-full bg-slate-950 rounded-[14px] flex items-center justify-center">
                    <span class="text-xl">❄️</span>
                </div>
            </div>
            <h1 class="text-xl font-bold text-white">Icepol</h1>
        </div>

        <div class="relative">
            <div class="px-4 py-2 rounded-full bg-purple-500/20 text-purple-200 border border-purple-500/40 flex items-center gap-2 font-mono text-xs shadow-lg">
                <span class="w-2 h-2 rounded-full bg-purple-400 animate-pulse"></span>
                <span>Métricas & Traces: <strong>Conectado</strong></span>
            </div>

            <!-- Popover Card -->
            <div class="absolute right-0 top-full mt-3 w-96 bg-[#0f172a] border border-purple-500/40 rounded-2xl shadow-2xl p-5 space-y-4 z-50 backdrop-blur-2xl">
                <div class="flex items-center justify-between pb-2.5 border-b border-slate-800">
                    <div class="flex items-center gap-2">
                        <span class="text-xl">📊</span>
                        <span class="font-bold text-sm text-white">Observabilidade & Tracing</span>
                    </div>
                    <span class="text-[10px] font-mono bg-emerald-500/10 text-emerald-400 px-2 py-0.5 rounded-full border border-emerald-500/30 font-bold">● 100% OPERACIONAL</span>
                </div>

                <div class="space-y-3 text-xs">
                    <div class="p-3.5 bg-slate-900/90 rounded-xl border border-purple-500/20 flex items-center justify-between">
                        <div class="space-y-1">
                            <div class="flex items-center gap-1.5 font-bold text-purple-300">
                                <span>🔍 Langfuse Tracing</span>
                                <span class="text-[9px] px-1.5 py-0.2 bg-purple-500/20 text-purple-300 rounded-full font-mono">:3001</span>
                            </div>
                            <p class="text-[11px] text-slate-400">Traces de LLM, latência & tokens ao vivo</p>
                        </div>
                        <span class="px-2.5 py-1 bg-purple-500/20 text-purple-300 border border-purple-500/30 rounded-lg text-[10px] font-bold">Ativo</span>
                    </div>

                    <div class="p-3.5 bg-slate-900/90 rounded-xl border border-rose-500/20 flex items-center justify-between">
                        <div class="space-y-1">
                            <div class="flex items-center gap-1.5 font-bold text-rose-300">
                                <span>🗄️ MinIO S3 Storage</span>
                                <span class="text-[9px] px-1.5 py-0.2 bg-rose-500/20 text-rose-300 rounded-full font-mono">:9001</span>
                            </div>
                            <p class="text-[11px] text-slate-400">Bucket: langfuse (eventos e payloads S3)</p>
                        </div>
                        <span class="px-2.5 py-1 bg-rose-500/20 text-rose-300 border border-rose-500/30 rounded-lg text-[10px] font-bold">Conectado</span>
                    </div>

                    <div class="p-3.5 bg-slate-900/90 rounded-xl border border-amber-500/20 flex items-center justify-between">
                        <div class="space-y-1">
                            <div class="flex items-center gap-1.5 font-bold text-amber-300">
                                <span>🐬 MySQL 8.0 Audit DB</span>
                                <span class="text-[9px] px-1.5 py-0.2 bg-amber-500/20 text-amber-300 rounded-full font-mono">:3306</span>
                            </div>
                            <p class="text-[11px] text-slate-400">Tabela query_metrics sincronizada</p>
                        </div>
                        <span class="px-2.5 py-1 bg-amber-500/20 text-amber-300 border border-amber-500/30 rounded-lg text-[10px] font-bold">Gravando</span>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <main class="flex-1 flex items-center justify-center opacity-30">
        <h2 class="text-5xl font-bold">Como posso ajudar com sua pesquisa hoje?</h2>
    </main>
</body>
</html>"""

# SCENE 4: Semantic Query Execution & Results
scene4_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Icepol - Query Executada</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-[#0e1117] text-slate-100 font-sans min-h-screen p-8 antialiased flex flex-col justify-center max-w-5xl mx-auto space-y-6">
    <div class="flex justify-end">
        <div class="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-3.5 rounded-2xl rounded-tr-none shadow-lg max-w-md font-medium text-sm">
            Qual a exposição total por setor?
        </div>
    </div>

    <div class="bg-[#0d121f] border border-slate-700/80 rounded-2xl p-6 shadow-2xl space-y-4">
        <div class="flex items-center justify-between pb-3 border-b border-slate-800 text-xs font-mono">
            <div class="flex items-center gap-2.5">
                <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-bold">[Out 1]</span>
                <span class="text-indigo-300 font-semibold">deepseek-r1:1.5b</span>
                <span class="text-slate-500">•</span>
                <span class="text-blue-300">DuckDB Engine</span>
                <span class="text-slate-500">•</span>
                <span class="text-purple-300">⚡ 14.9s</span>
            </div>
            <div class="text-xs text-slate-400 font-mono">
                Gravado no MySQL & Langfuse Trace ✓
            </div>
        </div>

        <div class="space-y-1.5">
            <span class="text-xs text-slate-400 font-mono font-semibold">SQL Compilado da Camada Semântica:</span>
            <pre class="bg-slate-950 p-4 rounded-xl border border-slate-800 text-xs text-cyan-300 font-mono overflow-x-auto"><code>SELECT c.ds_cnae_sector AS sector,
       SUM(f.vl_outstanding_balance) AS total_exposure,
       COUNT(DISTINCT f.facility_id) AS total_facilities
FROM corporate_credit.facilities f
JOIN corporate_credit.counterparts c ON f.counterpart_id = c.counterpart_id
GROUP BY c.ds_cnae_sector
ORDER BY total_exposure DESC;</code></pre>
        </div>

        <div class="space-y-1.5">
            <span class="text-xs text-slate-400 font-mono font-semibold">Resultados do DuckDB Lakehouse:</span>
            <div class="overflow-x-auto rounded-xl border border-slate-800">
                <table class="w-full text-left text-xs font-mono">
                    <thead class="bg-slate-900 text-slate-300 border-b border-slate-800">
                        <tr>
                            <th class="py-2.5 px-4">Setor (CNAE)</th>
                            <th class="py-2.5 px-4 text-right">Exposição Total (R$)</th>
                            <th class="py-2.5 px-4 text-right">Operações</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-800/60 bg-slate-950/60">
                        <tr>
                            <td class="py-2.5 px-4 text-white font-medium">Agronegócio</td>
                            <td class="py-2.5 px-4 text-right text-emerald-400 font-bold">R$ 450.000.000,00</td>
                            <td class="py-2.5 px-4 text-right text-slate-300">142</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-4 text-white font-medium">Indústria Química</td>
                            <td class="py-2.5 px-4 text-right text-emerald-400 font-bold">R$ 280.000.000,00</td>
                            <td class="py-2.5 px-4 text-right text-slate-300">89</td>
                        </tr>
                        <tr>
                            <td class="py-2.5 px-4 text-white font-medium">Varejo & Consumo</td>
                            <td class="py-2.5 px-4 text-right text-emerald-400 font-bold">R$ 195.000.000,00</td>
                            <td class="py-2.5 px-4 text-right text-slate-300">65</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>"""

# SCENE 5: Mermaid ERD Diagram 100% Connected with Crow's Foot
scene5_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Icepol - Diagrama Visual Mermaid</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.8/dist/mermaid.min.js"></script>
</head>
<body class="bg-[#0e1117] text-slate-100 font-sans min-h-screen p-8 antialiased flex flex-col justify-center items-center">
    <div class="w-full max-w-5xl bg-[#090d16] border border-slate-700/80 rounded-3xl p-6 shadow-2xl space-y-4">
        <div class="flex items-center justify-between pb-3 border-b border-slate-800 text-xs font-mono">
            <span class="flex items-center gap-2 text-sky-400 font-bold text-sm">
                <span>📐</span> Diagrama Visual Mermaid — Modelo Relacional Canônico
            </span>
            <span class="px-3 py-1 rounded-full bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 font-bold">
                ✓ 7 Entidades Conectadas (Crow's Foot)
            </span>
        </div>

        <div class="mermaid flex justify-center py-2">
erDiagram
    counterparts ||--o{ facilities : "possui"
    facilities ||--o{ collaterals : "garantido_por"
    counterparts ||--o{ proposals : "solicita"
    counterparts ||--o{ financial_statements : "declara"
    counterparts ||--o{ credit_limits : "possui"
    facilities ||--o{ covenants : "sujeito_a"

    counterparts {
        string counterpart_id PK
        string nm_counterpart
        string nm_economic_group
        string ds_cnae_sector
        string cd_rating_agency
    }
    facilities {
        string facility_id PK
        string counterpart_id FK
        string tp_operation
        string st_operation
        float limit_amount
    }
    collaterals {
        string collateral_id PK
        string facility_id FK
        string tp_collateral
        string st_collateral
    }
    proposals {
        string proposal_id PK
        string counterpart_id FK
        string st_decision
        string nm_committee
    }
    financial_statements {
        string statement_id PK
        string counterpart_id FK
        string nr_fiscal_year
        string st_audited
    }
    credit_limits {
        string limit_id PK
        string counterpart_id FK
        string tp_limit
        string st_limit
    }
    covenants {
        string covenant_id PK
        string facility_id FK
        string tp_covenant
        string st_compliance
    }
        </div>
    </div>
    <script>
        mermaid.initialize({
            startOnLoad: true,
            theme: 'dark',
            themeVariables: {
                darkMode: true,
                background: '#090d16',
                primaryColor: '#1e293b',
                primaryTextColor: '#f8fafc',
                primaryBorderColor: '#38bdf8',
                lineColor: '#38bdf8',
                secondaryColor: '#0f172a',
                tertiaryColor: '#1e1b4b'
            }
        });
    </script>
</body>
</html>"""

# SCENE 6: Outro Tech Stack
scene6_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Icepol - Tech Stack Outro</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-white min-h-screen flex flex-col items-center justify-center p-8 antialiased font-sans">
    <div class="max-w-4xl w-full text-center space-y-8">
        <div class="space-y-3">
            <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-sky-500/10 border border-sky-500/30 text-sky-400 font-mono text-xs font-semibold">
                ICEPOL SEMANTIC COPILOT 2026
            </div>
            <h1 class="text-6xl font-black tracking-tight bg-gradient-to-r from-sky-400 via-indigo-200 to-purple-400 bg-clip-text text-transparent">
                Arquitetura Enterprise
            </h1>
            <p class="text-slate-400 text-lg">
                Camada Semântica Vetorial, Raciocínio com LLM Local e Observabilidade Completa
            </p>
        </div>

        <div class="grid grid-cols-3 gap-4 pt-4 text-left">
            <div class="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-1">
                <span class="text-xl">🦆</span>
                <h3 class="font-bold text-white text-sm">DuckDB In-Memory</h3>
                <p class="text-xs text-slate-400">Motor analítico ultra-rápido sobre Apache Iceberg e Parquet</p>
            </div>
            <div class="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-1">
                <span class="text-xl">🤖</span>
                <h3 class="font-bold text-white text-sm">Multi-Model Ollama</h3>
                <p class="text-xs text-slate-400">DeepSeek-R1 (Raciocínio) + Qwen2.5 + LLaMA 3.2 100% Offline</p>
            </div>
            <div class="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-1">
                <span class="text-xl">🔍</span>
                <h3 class="font-bold text-white text-sm">Langfuse Tracing</h3>
                <p class="text-xs text-slate-400">Monitoramento de latência, spans, tokens e qualidade de LLM</p>
            </div>
            <div class="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-1">
                <span class="text-xl">🐬</span>
                <h3 class="font-bold text-white text-sm">MySQL 8.0 Audit</h3>
                <p class="text-xs text-slate-400">Histórico relacional e auditoria persistente de queries</p>
            </div>
            <div class="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-1">
                <span class="text-xl">🗄️</span>
                <h3 class="font-bold text-white text-sm">MinIO S3 Lakehouse</h3>
                <p class="text-xs text-slate-400">Armazenamento distribuído S3 compatível com Apache Polaris</p>
            </div>
            <div class="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-1">
                <span class="text-xl">📐</span>
                <h3 class="font-bold text-white text-sm">Mermaid Auto-Healing</h3>
                <p class="text-xs text-slate-400">Diagramas conceituais com unificação e notação Crow's foot</p>
            </div>
        </div>

        <div class="pt-6 flex justify-center items-center gap-4 text-xs text-slate-500 font-mono">
            <span>github.com/Helfstein-one/icepol-semantic</span>
            <span>•</span>
            <span>MIT License</span>
        </div>
    </div>
</body>
</html>"""

files = {
    "video/journey_s1.html": scene1_html,
    "video/journey_s2.html": scene2_html,
    "video/journey_s3.html": scene3_html,
    "video/journey_s4.html": scene4_html,
    "video/journey_s5.html": scene5_html,
    "video/journey_s6.html": scene6_html,
}

for path, content in files.items():
    with open(path, "w") as f:
        f.write(content)

capture_html("video/journey_s1.html", "video/journey_s1.png")
capture_html("video/journey_s2.html", "video/journey_s2.png")
capture_html("video/journey_s3.html", "video/journey_s3.png")
capture_html("video/journey_s4.html", "video/journey_s4.png")
capture_html("video/journey_s5.html", "video/journey_s5.png")
capture_html("video/journey_s6.html", "video/journey_s6.png")

scenes = [
    ("video/journey_s1.png", 5.5),
    ("video/journey_s2.png", 5.0),
    ("video/journey_s3.png", 5.5),
    ("video/journey_s4.png", 6.5),
    ("video/journey_s5.png", 8.0),
    ("video/journey_s6.png", 5.5),
]

temp_clips = []
for idx, (img, dur) in enumerate(scenes):
    clip_path = f"video/j_clip_{idx+1}.mp4"
    cmd = [
        ffmpeg,
        "-y",
        "-loop", "1",
        "-i", img,
        "-t", str(dur),
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
        "-r", "30",
        "-c:v", "libx264",
        "-preset", "fast",
        clip_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    temp_clips.append(clip_path)

concat_txt = "video/concat_journey.txt"
with open(concat_txt, "w") as f:
    for clip in temp_clips:
        f.write(f"file '{os.path.basename(clip)}'\n")

output_mp4 = "video/icepol_journey_complete.mp4"
audio_file = "video/soundtrack_80s.wav"

cmd_final = [
    ffmpeg,
    "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", concat_txt,
    "-i", audio_file,
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "18",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    "-movflags", "+faststart",
    output_mp4
]

subprocess.run(cmd_final, check=True)
print(f"Generated Video 1: {output_mp4}")

for clip in temp_clips:
    try: os.remove(clip)
    except: pass
try: os.remove(concat_txt)
except: pass

