import os
import subprocess
import time

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUTPUT_DIR = "video"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 8 Realistic UI Scenes representing the real chat session & Langfuse metrics:
# 1. UI Chat Empty State: Greeting "Como posso ajudar com sua pesquisa hoje?", Polar bear logo, model selector, upload, mic.
# 2. UI Chat Typing State: User typing prompt into pill, selecting deepseek-r1:1.5b.
# 3. UI Chat Response State: Streamed output with DuckDB analytical table, metadata tags and execution metrics.
# 4. UI Chat Mermaid Diagram Tab: Full-screen interactive dark Mermaid Crow's foot relational model (7 entities).
# 5. UI Chat Observability Popover: Popover open showing Langfuse (:3001), MinIO (:9000), MySQL 8 (:3306) real-time links.
# 6. Langfuse Dashboard: Real-time latency, trace count, P95 SLA, tokens processed.
# 7. Langfuse Spans Waterfall: Detailed waterfall of the query lifecycle.
# 8. Langfuse Token Economics: Where tokens are spent (Prompt context vs CoT vs SQL output).

scenes = [
    # Scene 1: Real Chat UI Initial Screen
    ("chat_s1.html", """<!DOCTYPE html>
<html lang="pt-BR" class="h-full bg-slate-950">
<head>
  <meta charset="utf-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body { width: 1920px; height: 1080px; overflow: hidden; }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 flex flex-col h-full font-sans antialiased">
  <header class="border-b border-slate-800/80 bg-slate-900/70 backdrop-blur-md px-10 py-4 flex items-center justify-between sticky top-0 z-20">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-sky-500/20 via-slate-800 to-slate-900 border border-sky-500/30 flex items-center justify-center shadow-lg shadow-sky-950/40">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><path d="M12 2C6.48 2 2 6.48 2 12c0 5.52 4.48 10 10 10s10-4.48 10-10C22 6.48 17.52 2 12 2zm1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
      </div>
      <div>
        <h1 class="text-xl font-bold tracking-tight text-white flex items-center gap-2">
          Icepol Semantic Layer
          <span class="text-[10px] uppercase font-mono px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">v1.2.0</span>
        </h1>
        <p class="text-xs text-slate-400">Inteligência Analítica em Crédito Corporativo • Apache Iceberg & DuckDB</p>
      </div>
    </div>
    
    <div class="flex items-center gap-3">
      <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
        <span>LLM: <strong class="text-emerald-300">deepseek-r1:1.5b</strong></span>
      </div>
      <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full font-medium bg-blue-500/10 text-blue-400 border border-blue-500/20 text-xs">
        <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
        <span>DuckDB Engine: <strong class="text-blue-300">Ativo (7 Tabelas)</strong></span>
      </div>
      <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full font-medium bg-purple-500/10 text-purple-400 border border-purple-500/20 text-xs">
        <span>⚡ Métricas & Traces (Langfuse)</span>
      </div>
    </div>
  </header>

  <main class="flex-1 flex flex-col items-center justify-center px-6 max-w-5xl mx-auto w-full">
    <div class="text-center space-y-4 mb-10">
      <h2 class="text-4xl font-extrabold tracking-tight text-slate-100 sm:text-5xl">Como posso ajudar com sua pesquisa hoje?</h2>
      <p class="text-slate-400 text-base max-w-xl mx-auto leading-relaxed">
        Consulte métricas regradas de balanço, alavancagem, limites e garantias com geração de SQL canônico e diagramas conceituais.
      </p>
    </div>

    <!-- Suggestions -->
    <div class="flex flex-wrap justify-center gap-3 mb-10 w-full max-w-4xl">
      <div class="px-4 py-2.5 rounded-xl border border-slate-800 bg-slate-900/50 text-slate-300 text-xs font-medium shadow-sm flex items-center gap-2">
        <span class="text-sky-400">📊</span> Exposição total por setor e alavancagem média
      </div>
      <div class="px-4 py-2.5 rounded-xl border border-slate-800 bg-slate-900/50 text-slate-300 text-xs font-medium shadow-sm flex items-center gap-2">
        <span class="text-emerald-400">🏢</span> Limite global aprovado por grupo econômico
      </div>
      <div class="px-4 py-2.5 rounded-xl border border-slate-800 bg-slate-900/50 text-slate-300 text-xs font-medium shadow-sm flex items-center gap-2">
        <span class="text-amber-400">⚠️</span> Cláusulas de desenquadramento de covenants
      </div>
      <div class="px-4 py-2.5 rounded-xl border border-sky-500/40 bg-sky-950/20 text-sky-300 text-xs font-semibold shadow-sm flex items-center gap-2">
        <span class="text-sky-400">📐</span> Diagrama Relacional Mermaid (Crow's Foot)
      </div>
    </div>

    <!-- Gemini-style Prompt Pill -->
    <div class="w-full max-w-3xl">
      <div class="relative bg-slate-900/90 border border-slate-700/80 focus-within:border-sky-500 rounded-3xl p-3 shadow-2xl backdrop-blur-xl flex items-center gap-3">
        <button class="w-10 h-10 rounded-full bg-slate-800 hover:bg-slate-700 flex items-center justify-center text-slate-300 text-lg font-bold border border-slate-700">+</button>
        <div class="px-3 py-1.5 rounded-full bg-slate-800 border border-sky-500/40 text-xs font-semibold text-sky-400 flex items-center gap-1.5">
          <span>deepseek-r1:1.5b</span>
          <span class="text-[10px]">▾</span>
        </div>
        <input type="text" placeholder="Peça ao deepseek-r1:1.5b..." class="bg-transparent text-sm text-slate-200 placeholder-slate-500 focus:outline-none flex-1" />
        <button class="w-10 h-10 rounded-full bg-slate-800 text-slate-400 flex items-center justify-center text-base hover:text-white">🎙️</button>
        <button class="w-10 h-10 rounded-full bg-sky-600 text-white flex items-center justify-center text-sm font-bold shadow-md shadow-sky-600/30">➔</button>
      </div>
    </div>
  </main>
</body>
</html>
"""),

    # Scene 2: Real Chat UI - User Typing Query
    ("chat_s2.html", """<!DOCTYPE html>
<html lang="pt-BR" class="h-full bg-slate-950">
<head>
  <meta charset="utf-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body { width: 1920px; height: 1080px; overflow: hidden; }
    .cursor-blink { display: inline-block; width: 2px; height: 18px; background: #38bdf8; vertical-align: middle; animation: blink 1s infinite; }
    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 flex flex-col h-full font-sans antialiased">
  <header class="border-b border-slate-800/80 bg-slate-900/70 backdrop-blur-md px-10 py-4 flex items-center justify-between sticky top-0 z-20">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-sky-500/20 via-slate-800 to-slate-900 border border-sky-500/30 flex items-center justify-center shadow-lg shadow-sky-950/40">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><path d="M12 2C6.48 2 2 6.48 2 12c0 5.52 4.48 10 10 10s10-4.48 10-10C22 6.48 17.52 2 12 2zm1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
      </div>
      <div>
        <h1 class="text-xl font-bold tracking-tight text-white flex items-center gap-2">Icepol Semantic Layer</h1>
        <p class="text-xs text-slate-400">Inteligência Analítica em Crédito Corporativo • Apache Iceberg & DuckDB</p>
      </div>
    </div>
    
    <div class="flex items-center gap-3">
      <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
        <span>LLM: <strong class="text-emerald-300">deepseek-r1:1.5b</strong></span>
      </div>
      <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full font-medium bg-blue-500/10 text-blue-400 border border-blue-500/20 text-xs">
        <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
        <span>DuckDB Engine: <strong class="text-blue-300">Ativo</strong></span>
      </div>
    </div>
  </header>

  <main class="flex-1 flex flex-col items-center justify-center px-6 max-w-5xl mx-auto w-full">
    <div class="text-center space-y-4 mb-12">
      <h2 class="text-4xl font-extrabold tracking-tight text-slate-100 sm:text-5xl">Como posso ajudar com sua pesquisa hoje?</h2>
      <p class="text-slate-400 text-base max-w-xl mx-auto leading-relaxed">
        Consulte métricas regradas de balanço, alavancagem, limites e garantias com geração de SQL canônico.
      </p>
    </div>

    <!-- Active Input Bar -->
    <div class="w-full max-w-3xl">
      <div class="relative bg-slate-900/95 border-2 border-sky-500 rounded-3xl p-3.5 shadow-2xl shadow-sky-950/60 flex items-center gap-3">
        <button class="w-10 h-10 rounded-full bg-slate-800 text-slate-300 text-lg font-bold border border-slate-700">+</button>
        <div class="px-3.5 py-1.5 rounded-full bg-sky-950/80 border border-sky-500/60 text-xs font-bold text-sky-300 flex items-center gap-1.5">
          <span>deepseek-r1:1.5b</span>
        </div>
        <div class="text-sm font-medium text-slate-100 flex-1 flex items-center">
          <span>Qual a exposição total e alavancagem média por setor? Gere o diagrama conceitual Mermaid.</span>
          <span class="cursor-blink ml-1"></span>
        </div>
        <button class="w-10 h-10 rounded-full bg-slate-800 text-slate-400 flex items-center justify-center text-base">🎙️</button>
        <button class="w-10 h-10 rounded-full bg-sky-500 text-white flex items-center justify-center text-sm font-bold shadow-lg shadow-sky-500/40">➔</button>
      </div>
    </div>
  </main>
</body>
</html>
"""),

    # Scene 3: Real Chat Response Cell with DuckDB Analytical Output
    ("chat_s3.html", """<!DOCTYPE html>
<html lang="pt-BR" class="h-full bg-slate-950">
<head>
  <meta charset="utf-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body { width: 1920px; height: 1080px; overflow: hidden; }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 flex flex-col h-full font-sans antialiased">
  <header class="border-b border-slate-800/80 bg-slate-900/70 backdrop-blur-md px-10 py-4 flex items-center justify-between sticky top-0 z-20">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-sky-500/20 via-slate-800 to-slate-900 border border-sky-500/30 flex items-center justify-center shadow-lg shadow-sky-950/40">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><path d="M12 2C6.48 2 2 6.48 2 12c0 5.52 4.48 10 10 10s10-4.48 10-10C22 6.48 17.52 2 12 2zm1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
      </div>
      <div>
        <h1 class="text-xl font-bold tracking-tight text-white flex items-center gap-2">Icepol Semantic Layer</h1>
        <p class="text-xs text-slate-400">Resposta da Camada Semântica • DuckDB In-Memory Execution</p>
      </div>
    </div>
    
    <div class="flex items-center gap-3">
      <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
        <span>Modelo: <strong class="text-emerald-300">deepseek-r1:1.5b</strong></span>
      </div>
      <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full font-medium bg-purple-500/10 text-purple-400 border border-purple-500/20 text-xs">
        <span>⚡ 1492.4ms (DuckDB + R1)</span>
      </div>
    </div>
  </header>

  <main class="flex-1 overflow-y-auto p-10 max-w-5xl mx-auto w-full space-y-8">
    <!-- User Message -->
    <div class="flex justify-end">
      <div class="bg-sky-600 text-white rounded-2xl rounded-tr-none px-5 py-3 max-w-xl text-sm font-medium shadow-md shadow-sky-900/30">
        Qual a exposição total e alavancagem média por setor? Gere o diagrama conceitual Mermaid.
      </div>
    </div>

    <!-- Assistant Response Notebook Cell -->
    <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2 text-xs text-slate-400">
          <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
          <span><b>deepseek-r1:1.5b</b> • DuckDB Engine • ⚡ 1492.4ms</span>
        </div>
        <div class="flex items-center gap-2 text-xs">
          <span class="px-2 py-1 rounded-md bg-slate-800 text-slate-300 font-mono text-[11px]">Audit ID: tr_icepol_8f492a</span>
        </div>
      </div>

      <!-- Result Table -->
      <div>
        <h4 class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">Tabela Analítica (Agregação Vectorizada DuckDB)</h4>
        <div class="overflow-hidden border border-slate-800 rounded-xl bg-slate-950/60">
          <table class="w-full text-left text-sm">
            <thead class="bg-slate-900/80 text-xs text-slate-400 border-b border-slate-800 font-semibold">
              <tr>
                <th class="p-3">Setor Econômico (CNAE)</th>
                <th class="p-3">Exposição Total (total_exposure)</th>
                <th class="p-3">Alavancagem Média (Dívida/EBITDA)</th>
                <th class="p-3">Risco Consolidado</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800/60 text-slate-300">
              <tr>
                <td class="p-3 font-medium text-white">Indústria & Manufatura</td>
                <td class="p-3 font-mono text-sky-400 font-semibold">R$ 4.820.000.000</td>
                <td class="p-3 font-mono">2.1x</td>
                <td class="p-3"><span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Baixo</span></td>
              </tr>
              <tr>
                <td class="p-3 font-medium text-white">Agronegócio & Grãos</td>
                <td class="p-3 font-mono text-sky-400 font-semibold">R$ 3.650.000.000</td>
                <td class="p-3 font-mono">1.8x</td>
                <td class="p-3"><span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Baixo</span></td>
              </tr>
              <tr>
                <td class="p-3 font-medium text-white">Varejo & Consumo</td>
                <td class="p-3 font-mono text-sky-400 font-semibold">R$ 2.410.000.000</td>
                <td class="p-3 font-mono text-amber-400 font-bold">3.4x</td>
                <td class="p-3"><span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">Atenção</span></td>
              </tr>
              <tr>
                <td class="p-3 font-medium text-white">Energia & Infraestrutura</td>
                <td class="p-3 font-mono text-sky-400 font-semibold">R$ 1.950.000.000</td>
                <td class="p-3 font-mono">1.4x</td>
                <td class="p-3"><span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Ótimo</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Action Tabs -->
      <div class="flex items-center gap-3 pt-2">
        <button class="px-3.5 py-1.5 rounded-lg bg-sky-600/20 text-sky-300 border border-sky-500/40 text-xs font-semibold flex items-center gap-1.5">
          <span>📐 Diagrama Visual Mermaid (Ativo)</span>
        </button>
        <button class="px-3.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium flex items-center gap-1.5">
          <span>📄 Ver SQL Compilado</span>
        </button>
        <button class="px-3.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium flex items-center gap-1.5">
          <span>💾 Exportar CSV</span>
        </button>
      </div>
    </div>
  </main>
</body>
</html>
"""),

    # Scene 4: Real Chat Mermaid Diagram Tab (Full-Screen Clean ERD)
    ("chat_s4.html", """<!DOCTYPE html>
<html lang="pt-BR" class="h-full bg-slate-950">
<head>
  <meta charset="utf-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body { width: 1920px; height: 1080px; overflow: hidden; }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 flex flex-col h-full font-sans antialiased">
  <header class="border-b border-slate-800/80 bg-slate-900/70 backdrop-blur-md px-10 py-4 flex items-center justify-between sticky top-0 z-20">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-xl bg-sky-500/20 border border-sky-500/40 flex items-center justify-center">📐</div>
      <div>
        <h1 class="text-xl font-bold tracking-tight text-white">Modelo Conceitual de Crédito Corporativo (Mermaid ERD)</h1>
        <p class="text-xs text-slate-400">Renderização ao vivo com cardinalidade estrita Crow's Foot • Zero erros de sintaxe</p>
      </div>
    </div>
    <div class="px-3 py-1.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-semibold">
      ✔ 7 Entidades Conectadas (1:N & N:M)
    </div>
  </header>

  <main class="flex-1 p-10 flex items-center justify-center">
    <div class="w-full max-w-6xl bg-slate-900/90 border border-slate-800 rounded-3xl p-8 shadow-2xl relative">
      <div class="grid grid-cols-4 gap-6 mb-8">
        <!-- Entity 1 -->
        <div class="bg-slate-950 border border-sky-500/40 rounded-xl overflow-hidden shadow-lg">
          <div class="bg-sky-600 text-white text-xs font-bold text-center py-2">COUNTERPARTS</div>
          <div class="p-3 text-[11px] font-mono space-y-1 text-slate-300">
            <div class="text-pink-400 font-bold">PK counterpart_id</div>
            <div>string nm_counterpart</div>
            <div>string ds_cnae_sector</div>
            <div>string cd_rating</div>
          </div>
        </div>

        <!-- Entity 2 -->
        <div class="bg-slate-950 border border-sky-500/40 rounded-xl overflow-hidden shadow-lg">
          <div class="bg-sky-600 text-white text-xs font-bold text-center py-2">FACILITIES</div>
          <div class="p-3 text-[11px] font-mono space-y-1 text-slate-300">
            <div class="text-pink-400 font-bold">PK facility_id</div>
            <div class="text-sky-400 font-semibold">FK counterpart_id</div>
            <div>string tp_operation</div>
            <div>double vl_credit_limit</div>
          </div>
        </div>

        <!-- Entity 3 -->
        <div class="bg-slate-950 border border-sky-500/40 rounded-xl overflow-hidden shadow-lg">
          <div class="bg-sky-600 text-white text-xs font-bold text-center py-2">COLLATERALS</div>
          <div class="p-3 text-[11px] font-mono space-y-1 text-slate-300">
            <div class="text-pink-400 font-bold">PK collateral_id</div>
            <div class="text-sky-400 font-semibold">FK facility_id</div>
            <div>string tp_collateral</div>
            <div>double vl_appraised</div>
          </div>
        </div>

        <!-- Entity 4 -->
        <div class="bg-slate-950 border border-sky-500/40 rounded-xl overflow-hidden shadow-lg">
          <div class="bg-sky-600 text-white text-xs font-bold text-center py-2">PROPOSALS</div>
          <div class="p-3 text-[11px] font-mono space-y-1 text-slate-300">
            <div class="text-pink-400 font-bold">PK proposal_id</div>
            <div class="text-sky-400 font-semibold">FK counterpart_id</div>
            <div>string st_decision</div>
            <div>double vl_requested</div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-3 gap-6">
        <!-- Entity 5 -->
        <div class="bg-slate-950 border border-purple-500/40 rounded-xl overflow-hidden shadow-lg">
          <div class="bg-purple-600 text-white text-xs font-bold text-center py-2">FINANCIAL_STATEMENTS</div>
          <div class="p-3 text-[11px] font-mono space-y-1 text-slate-300">
            <div class="text-pink-400 font-bold">PK statement_id</div>
            <div class="text-sky-400 font-semibold">FK counterpart_id</div>
            <div>double vl_net_debt</div>
            <div>double vl_ebitda</div>
          </div>
        </div>

        <!-- Entity 6 -->
        <div class="bg-slate-950 border border-purple-500/40 rounded-xl overflow-hidden shadow-lg">
          <div class="bg-purple-600 text-white text-xs font-bold text-center py-2">CREDIT_LIMITS</div>
          <div class="p-3 text-[11px] font-mono space-y-1 text-slate-300">
            <div class="text-pink-400 font-bold">PK limit_id</div>
            <div class="text-sky-400 font-semibold">FK counterpart_id</div>
            <div>double approved_limit</div>
            <div>double used_limit</div>
          </div>
        </div>

        <!-- Entity 7 -->
        <div class="bg-slate-950 border border-purple-500/40 rounded-xl overflow-hidden shadow-lg">
          <div class="bg-purple-600 text-white text-xs font-bold text-center py-2">COVENANTS</div>
          <div class="p-3 text-[11px] font-mono space-y-1 text-slate-300">
            <div class="text-pink-400 font-bold">PK covenant_id</div>
            <div class="text-sky-400 font-semibold">FK facility_id</div>
            <div>string tp_covenant</div>
            <div>string st_compliance</div>
          </div>
        </div>
      </div>

      <div class="mt-8 flex justify-between items-center text-xs text-slate-400 border-t border-slate-800 pt-4">
        <div class="flex items-center gap-4">
          <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-sky-400"></span> ||--o{ (1 para Muitos)</span>
          <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-purple-400"></span> }|--|{ (Muitos para Muitos)</span>
        </div>
        <div class="text-emerald-400 font-mono">100% Compatível com Mermaid v10.9.8 • Sanitização Ativa</div>
      </div>
    </div>
  </main>
</body>
</html>
"""),

    # Scene 5: Real Chat UI with Observability Popover Open
    ("chat_s5.html", """<!DOCTYPE html>
<html lang="pt-BR" class="h-full bg-slate-950">
<head>
  <meta charset="utf-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body { width: 1920px; height: 1080px; overflow: hidden; }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 flex flex-col h-full font-sans antialiased">
  <header class="border-b border-slate-800/80 bg-slate-900/70 backdrop-blur-md px-10 py-4 flex items-center justify-between sticky top-0 z-20">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-xl bg-sky-500/20 border border-sky-500/40 flex items-center justify-center">🧊</div>
      <div>
        <h1 class="text-xl font-bold tracking-tight text-white">Icepol Semantic Layer</h1>
        <p class="text-xs text-slate-400">Cockpit de Observabilidade Aberto no Chat</p>
      </div>
    </div>

    <!-- Active Popover Trigger -->
    <div class="relative">
      <button class="inline-flex items-center gap-2 px-4 py-2 rounded-full font-semibold bg-purple-500/20 text-purple-300 border-2 border-purple-500 text-xs shadow-lg shadow-purple-900/40">
        <span class="w-2 h-2 rounded-full bg-purple-400 animate-pulse"></span>
        <span>Métricas & Traces (Conectado)</span>
        <span>▾</span>
      </button>

      <!-- The Real Opened Popover -->
      <div class="absolute right-0 mt-3 w-96 bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl p-5 space-y-4 backdrop-blur-2xl z-50">
        <div class="flex items-center justify-between pb-3 border-b border-slate-800">
          <div class="flex items-center gap-2">
            <span class="text-purple-400 font-bold text-sm">Cockpit de Telemetria</span>
          </div>
          <span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">3 Sinks Vivos</span>
        </div>

        <div class="space-y-2.5 text-xs">
          <!-- Item 1: Langfuse -->
          <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 flex justify-between items-center">
            <div>
              <div class="font-semibold text-white">Langfuse v2 Tracing</div>
              <div class="text-[11px] text-slate-400 font-mono">http://localhost:3001</div>
            </div>
            <a href="#" class="px-2.5 py-1 bg-purple-600 text-white rounded-md text-[11px] font-bold">Abrir ➔</a>
          </div>

          <!-- Item 2: MinIO -->
          <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 flex justify-between items-center">
            <div>
              <div class="font-semibold text-white">MinIO S3 Payload Blobs</div>
              <div class="text-[11px] text-slate-400 font-mono">/data/langfuse (Bucket)</div>
            </div>
            <span class="text-emerald-400 font-bold">Conectado</span>
          </div>

          <!-- Item 3: MySQL -->
          <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 flex justify-between items-center">
            <div>
              <div class="font-semibold text-white">MySQL 8.0 Audit Store</div>
              <div class="text-[11px] text-slate-400 font-mono">icepol_metrics.query_metrics</div>
            </div>
            <span class="text-sky-400 font-bold">1 Linha Gravada</span>
          </div>
        </div>

        <div class="text-[11px] text-slate-400 bg-slate-950/60 p-2.5 rounded-lg border border-slate-800/80">
          Todas as chamadas LLM e consultas DuckDB são auditadas assincronamente com retenção persistente.
        </div>
      </div>
    </div>
  </header>

  <main class="flex-1 p-10 flex items-center justify-center opacity-40">
    <div class="text-center">
      <div class="text-4xl mb-2">⚡</div>
      <div class="text-lg font-bold">Navegando para a Interface de Métricas do Modelo...</div>
    </div>
  </main>
</body>
</html>
"""),

    # Scene 6: Langfuse Dashboard (Real Observability View)
    ("chat_s6.html", """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  body { background: #0b0f19; color: #f1f5f9; width: 1920px; height: 1080px; overflow: hidden; display: flex; flex-direction: column; }
  header { height: 64px; background: #111827; border-bottom: 1px solid #1f2937; display: flex; align-items: center; justify-content: space-between; padding: 0 40px; }
  .brand { display: flex; align-items: center; gap: 14px; font-size: 18px; font-weight: 700; }
  .brand svg { width: 28px; height: 28px; fill: #38bdf8; }

  .content { flex: 1; padding: 36px 48px; display: flex; flex-direction: column; gap: 28px; }
  .title-bar { display: flex; justify-content: space-between; align-items: flex-end; }
  .title-bar h2 { font-size: 28px; font-weight: 800; }
  .title-bar p { font-size: 15px; color: #94a3b8; margin-top: 4px; }

  .metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }
  .card { background: #111827; border: 1px solid #1e293b; border-radius: 14px; padding: 24px; display: flex; flex-direction: column; justify-content: space-between; }
  .card-label { font-size: 13px; color: #94a3b8; font-weight: 600; text-transform: uppercase; }
  .card-val { font-size: 38px; font-weight: 900; margin: 12px 0 6px; }
  .card-sub { font-size: 12px; color: #10b981; font-weight: 600; }

  .table-box { background: #111827; border: 1px solid #1e293b; border-radius: 14px; padding: 24px; flex: 1; }
  table { width: 100%; border-collapse: collapse; font-size: 14px; text-align: left; }
  th { padding: 12px; color: #64748b; font-size: 12px; text-transform: uppercase; border-bottom: 1px solid #1e293b; }
  td { padding: 14px 12px; border-bottom: 1px solid #1a2234; color: #cbd5e1; }
</style>
</head>
<body>
  <header>
    <div class="brand">
      <svg viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
      <span>Langfuse Tracing & Observability • Cockpit Aberto</span>
    </div>
    <div style="font-size: 13px; color: #10b981; font-weight: bold;">✔ Projeto: icepol-semantic (v1.2.0)</div>
  </header>

  <div class="content">
    <div class="title-bar">
      <div>
        <h2>Métricas de Execução do Modelo em Produção</h2>
        <p>Acompanhamento ao vivo de volume de traces, SLAs de latência, contagem de tokens e integridade dos sinks.</p>
      </div>
      <div style="font-size:13px; color:#38bdf8; font-family:monospace; background:#0c4a6e33; padding:8px 16px; border-radius:8px; border:1px solid #0284c7;">
        Model: deepseek-r1:1.5b (Ollama Local)
      </div>
    </div>

    <div class="metrics-grid">
      <div class="card">
        <div class="card-label">Volume Total de Traces</div>
        <div class="card-val" style="color: #38bdf8;">1,482</div>
        <div class="card-sub">↑ 100% de cobertura</div>
      </div>
      <div class="card">
        <div class="card-label">Latência Média End-to-End</div>
        <div class="card-val" style="color: #c084fc;">1.42s</div>
        <div class="card-sub">P95: 1.88s (Abaixo do SLA)</div>
      </div>
      <div class="card">
        <div class="card-label">Tokens Totais Monitorados</div>
        <div class="card-val" style="color: #34d399;">324.8k</div>
        <div class="card-sub">Zero Alucinação de Schema</div>
      </div>
      <div class="card">
        <div class="card-label">Confiabilidade dos Sinks</div>
        <div class="card-val" style="color: #fbbf24;">100%</div>
        <div class="card-sub">MinIO S3 + MySQL 8.0 OK</div>
      </div>
    </div>

    <div class="table-box">
      <h3 style="font-size: 16px; font-weight: 700; margin-bottom: 16px; color: #ffffff;">Sessões Recentes Monitoradas</h3>
      <table>
        <thead>
          <tr>
            <th>Trace ID</th>
            <th>Prompt da Consulta</th>
            <th>Modelo</th>
            <th>Latência</th>
            <th>Tokens</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style="font-family: monospace; color: #38bdf8; font-weight: bold;">tr_icepol_8f492a</td>
            <td>Qual a exposição total e alavancagem média por setor?</td>
            <td><span style="background:#1e293b; color:#93c5fd; padding:3px 8px; border-radius:4px;">deepseek-r1:1.5b</span></td>
            <td>1.492s</td>
            <td>342 tokens</td>
            <td><span style="color:#34d399; font-weight:bold;">SUCCESS (200)</span></td>
          </tr>
          <tr>
            <td style="font-family: monospace; color: #38bdf8; font-weight: bold;">tr_icepol_7b109e</td>
            <td>Gere o diagrama conceitual completo em Mermaid</td>
            <td><span style="background:#1e293b; color:#93c5fd; padding:3px 8px; border-radius:4px;">llama3.2:3b</span></td>
            <td>2.110s</td>
            <td>410 tokens</td>
            <td><span style="color:#34d399; font-weight:bold;">SUCCESS (200)</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</body>
</html>
"""),

    # Scene 7: Langfuse Waterfall Spans Deep-Dive
    ("chat_s7.html", """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; }
  body { background: #0b0f19; color: #f1f5f9; width: 1920px; height: 1080px; overflow: hidden; display: flex; flex-direction: column; }
  header { height: 64px; background: #111827; border-bottom: 1px solid #1f2937; display: flex; align-items: center; justify-content: space-between; padding: 0 32px; }
  .brand { display: flex; align-items: center; gap: 14px; font-size: 18px; font-weight: 700; }
  .brand svg { width: 28px; height: 28px; fill: #38bdf8; }

  .content { flex: 1; padding: 32px 48px; display: grid; grid-template-columns: 440px 1fr; gap: 32px; }
  .panel-meta { background: #111827; border: 1px solid #1e293b; border-radius: 14px; padding: 24px; display: flex; flex-direction: column; gap: 16px; }
  .meta-title { font-size: 14px; font-weight: 700; color: #94a3b8; text-transform: uppercase; border-bottom: 1px solid #1e293b; padding-bottom: 10px; }
  .field { display: flex; flex-direction: column; gap: 3px; }
  .f-label { font-size: 11px; color: #64748b; font-weight: 600; text-transform: uppercase; }
  .f-val { font-size: 13px; color: #f1f5f9; font-family: monospace; }

  .panel-wf { background: #111827; border: 1px solid #1e293b; border-radius: 14px; padding: 28px; display: flex; flex-direction: column; }
  .wf-head { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e293b; padding-bottom: 16px; margin-bottom: 24px; }
  .wf-head h2 { font-size: 20px; font-weight: 700; }

  .span-row { margin-bottom: 20px; }
  .span-info { display: flex; justify-content: space-between; font-size: 14px; margin-bottom: 6px; font-weight: 600; }
  .bar-bg { width: 100%; height: 28px; background: #0f172a; border-radius: 6px; border: 1px solid #1e293b; position: relative; overflow: hidden; }
  .bar-fill { height: 100%; position: absolute; border-radius: 5px; display: flex; align-items: center; padding-left: 12px; font-size: 12px; font-weight: 700; color: #fff; }
  
  .b1 { background: linear-gradient(90deg, #3b82f6, #60a5fa); left: 0%; width: 100%; }
  .b2 { background: linear-gradient(90deg, #8b5cf6, #a78bfa); left: 3%; width: 22%; }
  .b3 { background: linear-gradient(90deg, #ec4899, #f472b6); left: 26%; width: 52%; }
  .b4 { background: linear-gradient(90deg, #10b981, #34d399); left: 79%; width: 12%; }
  .b5 { background: linear-gradient(90deg, #f59e0b, #fbbf24); left: 92%; width: 8%; }
</style>
</head>
<body>
  <header>
    <div class="brand">
      <svg viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
      <span>Langfuse Tracing: Waterfall de Spans da Consulta</span>
    </div>
    <div style="font-size:13px; color:#10b981; font-weight:600;">Trace ID: tr_icepol_8f492a</div>
  </header>

  <div class="content">
    <div class="panel-meta">
      <div class="meta-title">Metadados da Sessão Auditada</div>
      <div class="field">
        <div class="f-label">Prompt Original</div>
        <div class="f-val" style="color:#38bdf8;">"Qual a exposição total e alavancagem média por setor?"</div>
      </div>
      <div class="field">
        <div class="f-label">Modelo LLM</div>
        <div class="f-val">deepseek-r1:1.5b (Ollama Local)</div>
      </div>
      <div class="field">
        <div class="f-label">Motor OLAP</div>
        <div class="f-val">DuckDB v1.1.3 In-Memory Columnar</div>
      </div>
      <div class="field">
        <div class="f-label">Audit Sink</div>
        <div class="f-val" style="color:#fbbf24;">MySQL 8.0 (Tabela: query_metrics)</div>
      </div>
      <div class="field">
        <div class="f-label">Latência Total (Wall Time)</div>
        <div class="f-val" style="color:#34d399; font-size:15px; font-weight:bold;">1.492,4 ms</div>
      </div>
    </div>

    <div class="panel-wf">
      <div class="wf-head">
        <h2>Decomposição da Latência em Spans</h2>
        <span style="font-size:13px; color:#94a3b8;">100% de cobertura</span>
      </div>

      <div class="span-row">
        <div class="span-info"><span style="color:#93c5fd;">ROOT: icepol_query_handler</span><span>1.492,4 ms (100%)</span></div>
        <div class="bar-bg"><div class="bar-fill b1">Ciclo Global da Requisição</div></div>
      </div>

      <div class="span-row">
        <div class="span-info"><span style="color:#c4b5fd;">SPAN 1: semantic_ontology_parsing</span><span>328,0 ms (22%)</span></div>
        <div class="bar-bg"><div class="bar-fill b2">Validação de Dimensões e Fórmulas no YAML</div></div>
      </div>

      <div class="span-row">
        <div class="span-info"><span style="color:#f472b6;">SPAN 2: deepseek_r1_sql_synthesis</span><span>776,0 ms (52%)</span></div>
        <div class="bar-bg"><div class="bar-fill b3">Raciocínio CoT do Modelo (342 Tokens)</div></div>
      </div>

      <div class="span-row">
        <div class="span-info"><span style="color:#6ee7b7;">SPAN 3: duckdb_columnar_query</span><span>180,0 ms (12%)</span></div>
        <div class="bar-bg"><div class="bar-fill b4">Scan Vetorizado no DuckDB</div></div>
      </div>

      <div class="span-row">
        <div class="span-info"><span style="color:#fde047;">SPAN 4: audit_minio_mysql_sink</span><span>108,4 ms (7%)</span></div>
        <div class="bar-bg"><div class="bar-fill b5">Persistência Assíncrona no MinIO e MySQL</div></div>
      </div>
    </div>
  </div>
</body>
</html>
"""),

    # Scene 8: Langfuse Token Economics Breakdown
    ("chat_s8.html", """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  body { background: #0b0f19; color: #f1f5f9; width: 1920px; height: 1080px; overflow: hidden; display: flex; flex-direction: column; }
  header { height: 64px; background: #111827; border-bottom: 1px solid #1f2937; display: flex; align-items: center; justify-content: space-between; padding: 0 32px; }
  .brand { display: flex; align-items: center; gap: 14px; font-size: 18px; font-weight: 700; }
  .brand svg { width: 28px; height: 28px; fill: #38bdf8; }

  .content { flex: 1; padding: 36px 48px; display: flex; flex-direction: column; gap: 28px; }
  .title-bar h2 { font-size: 28px; font-weight: 800; color: #ffffff; }
  .title-bar p { font-size: 15px; color: #94a3b8; margin-top: 4px; }

  .cards-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
  .t-card { background: #111827; border: 1px solid #1e293b; border-radius: 14px; padding: 24px; display: flex; flex-direction: column; justify-content: space-between; }
  .t-head { font-size: 14px; font-weight: 600; color: #94a3b8; display: flex; justify-content: space-between; }
  .t-num { font-size: 42px; font-weight: 900; margin: 12px 0; }
  .t-desc { font-size: 13px; color: #64748b; line-height: 1.4; }

  .breakdown-box { background: #111827; border: 1px solid #1e293b; border-radius: 14px; padding: 28px; flex: 1; display: flex; flex-direction: column; }
  .box-title { font-size: 18px; font-weight: 700; color: #ffffff; margin-bottom: 16px; }
  
  .big-bar { width: 100%; height: 44px; border-radius: 8px; display: flex; overflow: hidden; margin-bottom: 24px; border: 1px solid #334155; }
  .seg1 { width: 63.7%; background: linear-gradient(90deg, #0284c7, #38bdf8); display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 800; color: #000; }
  .seg2 { width: 21.0%; background: linear-gradient(90deg, #7c3aed, #a78bfa); display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 800; color: #fff; }
  .seg3 { width: 15.3%; background: linear-gradient(90deg, #059669, #34d399); display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 800; color: #000; }

  .details-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; font-size: 13px; }
  .item-box { background: #0f172a; border: 1px solid #1e293b; border-radius: 10px; padding: 16px; }
  .item-title { font-weight: 700; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
  .dot { width: 10px; height: 10px; border-radius: 50%; }
</style>
</head>
<body>
  <header>
    <div class="brand">
      <svg viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
      <span>Langfuse Token Intelligence • Onde os Tokens São Gastos</span>
    </div>
    <span style="color:#38bdf8; font-family:monospace; font-size:13px;">Modelo: deepseek-r1:1.5b</span>
  </header>

  <div class="content">
    <div class="title-bar">
      <h2>Auditoria e Eficiência de Tokens na Consulta</h2>
      <p>Detalhamento de consumo: contexto ontológico de entrada, cadeia de raciocínio e saída SQL.</p>
    </div>

    <div class="cards-grid">
      <div class="t-card" style="border-top: 4px solid #38bdf8;">
        <div class="t-head"><span>Prompt Context Tokens</span><span>📥 Input</span></div>
        <div class="t-num" style="color: #38bdf8;">218</div>
        <div class="t-desc">Mapeamento ontológico das 7 tabelas físicas, métricas de crédito e instruções de guardrail semântico.</div>
      </div>

      <div class="t-card" style="border-top: 4px solid #a78bfa;">
        <div class="t-head"><span>Reasoning / Thought Tokens</span><span>🧠 CoT</span></div>
        <div class="t-num" style="color: #a78bfa;">72</div>
        <div class="t-desc">Tokens gastos dentro do bloco <code>&lt;think&gt;</code> do DeepSeek-R1 validando cardinalidade de chaves.</div>
      </div>

      <div class="t-card" style="border-top: 4px solid #34d399;">
        <div class="t-head"><span>Completion Tokens</span><span>📤 SQL / Output</span></div>
        <div class="t-num" style="color: #34d399;">52</div>
        <div class="t-desc">Geração direta da query SQL ANSI canônica executada diretamente pelo motor DuckDB.</div>
      </div>
    </div>

    <div class="breakdown-box">
      <div class="box-title">Distribuição Percentual por Consulta (Total: 342 Tokens)</div>
      
      <div class="big-bar">
        <div class="seg1">Input Ontologia (63.7% - 218 Tokens)</div>
        <div class="seg2">Raciocínio CoT (21.0% - 72 Tokens)</div>
        <div class="seg3">SQL Output (15.3% - 52 Tokens)</div>
      </div>

      <div class="details-grid">
        <div class="item-box">
          <div class="item-title"><div class="dot" style="background:#38bdf8;"></div><b>1. Input Ontológico (218 tokens)</b></div>
          <p style="color:#94a3b8; line-height:1.4;">Definições de colunas de <code>counterparts</code>, <code>facilities</code> e métrica <code>avg_net_debt_ebitda</code>.</p>
        </div>
        <div class="item-box">
          <div class="item-title"><div class="dot" style="background:#a78bfa;"></div><b>2. Raciocínio DeepSeek-R1 (72 tokens)</b></div>
          <p style="color:#94a3b8; line-height:1.4;">O modelo avalia a integridade referencial e Crow's foot antes de emitir a query final.</p>
        </div>
        <div class="item-box">
          <div class="item-title"><div class="dot" style="background:#34d399;"></div><b>3. Síntese SQL e Diagrama (52 tokens)</b></div>
          <p style="color:#94a3b8; line-height:1.4;">Payload ultracompacto pronto para compilação colunar instantânea pelo DuckDB.</p>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
""")
]

# 1. Write HTML files
for fname, html_code in scenes:
    fpath = os.path.join(OUTPUT_DIR, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(html_code)
    print(f"Written: {fpath}")

# 2. Render each HTML to PNG with headless Chrome (1920x1080)
for fname, _ in scenes:
    png_name = fname.replace(".html", ".png")
    html_path = os.path.abspath(os.path.join(OUTPUT_DIR, fname))
    png_path = os.path.abspath(os.path.join(OUTPUT_DIR, png_name))
    cmd = [
        CHROME_BIN,
        "--headless=new",
        "--disable-gpu",
        "--window-size=1920,1080",
        f"--screenshot={png_path}",
        f"file://{html_path}"
    ]
    subprocess.run(cmd, check=True)
    print(f"Captured: {png_name}")

# 3. Durations for each of the 8 scenes matching the 60s Cyberpunk soundtrack:
# Total = 60 seconds
# S1: UI Chat Initial (7s)
# S2: UI Chat Typing (7s)
# S3: UI Chat Response DuckDB (8s)
# S4: UI Chat Mermaid Diagram Tab (8s)
# S5: UI Chat Observability Popover (6s)
# S6: Langfuse Dashboard (8s)
# S7: Langfuse Spans Waterfall (8s)
# S8: Langfuse Token Economics (8s)
# Sum = 7 + 7 + 8 + 8 + 6 + 8 + 8 + 8 = 60s
clip_durations = [
    ("chat_s1.png", 7),
    ("chat_s2.png", 7),
    ("chat_s3.png", 8),
    ("chat_s4.png", 8),
    ("chat_s5.png", 6),
    ("chat_s6.png", 8),
    ("chat_s7.png", 8),
    ("chat_s8.png", 8)
]

clip_files = []
for i, (png_name, dur) in enumerate(clip_durations):
    clip_path = os.path.join(OUTPUT_DIR, f"chat_clip_{i}.mp4")
    png_path = os.path.join(OUTPUT_DIR, png_name)
    cmd = [
        "/opt/homebrew/bin/ffmpeg",
        "-y",
        "-loop", "1",
        "-i", png_path,
        "-c:v", "libx264",
        "-t", str(dur),
        "-pix_fmt", "yuv420p",
        "-vf", "scale=1920:1080",
        clip_path
    ]
    subprocess.run(cmd, check=True)
    clip_files.append(clip_path)

# 4. Concat list
concat_path = os.path.join(OUTPUT_DIR, "concat_chat_journey.txt")
with open(concat_path, "w") as f:
    for c in clip_files:
        f.write(f"file '{os.path.abspath(c)}'\n")

# 5. Render final chat journey video with new Cyberpunk Synthwave soundtrack
final_output = os.path.join(OUTPUT_DIR, "icepol_chat_ui_journey_cyberpunk.mp4")
audio_path = os.path.join(OUTPUT_DIR, "soundtrack_cyberpunk_synthwave_60s.wav")

cmd = [
    "/opt/homebrew/bin/ffmpeg",
    "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", concat_path,
    "-i", audio_path,
    "-c:v", "libx264",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    final_output
]
subprocess.run(cmd, check=True)
print(f"Generated Chat Journey Video: {final_output}")
