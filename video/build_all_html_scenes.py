import os
import subprocess

pwd = os.path.abspath(os.curdir)
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def capture_html(html_path, out_png):
    file_url = f"file://{pwd}/{html_path}"
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--window-size=1440,900",
        f"--screenshot={out_png}",
        file_url
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"Captured: {out_png}")

# Common SVG Polar Bear Logo
polar_bear_svg = """
<div class="w-9 h-9 rounded-xl bg-gradient-to-br from-sky-500/15 via-slate-800/60 to-slate-900 border border-sky-500/30 flex items-center justify-center shadow-lg shadow-sky-950/40">
    <svg width="24" height="24" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="iceBearGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#ffffff"/>
                <stop offset="45%" stop-color="#7dd3fc"/>
                <stop offset="100%" stop-color="#0284c7"/>
            </linearGradient>
            <linearGradient id="iceBearFill" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.22"/>
                <stop offset="100%" stop-color="#0284c7" stop-opacity="0.05"/>
            </linearGradient>
        </defs>
        <path d="M10 6 C10 4 12 3 14 4 C15 4.8 15 6 15 7" stroke="url(#iceBearGrad)" stroke-width="1.6" stroke-linecap="round" fill="rgba(56, 189, 248, 0.25)"/>
        <path d="M15 7 L21 11 L28 14 L29 15.5 L26 17 L22 17" stroke="url(#iceBearGrad)" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round" fill="url(#iceBearFill)"/>
        <path d="M22 17 L20 21 L17 26 L12 26 L8 21 L8 14 L10 6" stroke="url(#iceBearGrad)" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round" fill="url(#iceBearFill)"/>
        <path d="M15 7 L17 14 L28 14" stroke="url(#iceBearGrad)" stroke-width="1.2" stroke-linejoin="round" stroke-opacity="0.8"/>
        <path d="M17 14 L22 17" stroke="url(#iceBearGrad)" stroke-width="1.2" stroke-linejoin="round" stroke-opacity="0.75"/>
        <path d="M17 14 L14 20 L20 21" stroke="url(#iceBearGrad)" stroke-width="1.2" stroke-linejoin="round" stroke-opacity="0.65"/>
        <path d="M8 14 L17 14" stroke="url(#iceBearGrad)" stroke-width="1.1" stroke-linejoin="round" stroke-opacity="0.5"/>
        <path d="M14 20 L12 26" stroke="url(#iceBearGrad)" stroke-width="1.1" stroke-linejoin="round" stroke-opacity="0.5"/>
        <circle cx="19.5" cy="12.5" r="1.1" fill="#ffffff"/>
        <circle cx="28.5" cy="14.8" r="0.8" fill="#7dd3fc"/>
    </svg>
</div>
<span class="text-xl font-bold tracking-tight text-white font-mono">Icepol</span>
"""

# Common browser chrome bar
def browser_header(active_popover=None):
    duck_popover_class = "block" if active_popover == "duckdb" else "hidden"
    llm_popover_class = "block" if active_popover == "llm" else "hidden"

    return f"""
    <!-- Browser Top Bar -->
    <div class="bg-[#1e1f20] px-4 py-2 border-b border-slate-800 flex items-center justify-between text-xs select-none">
        <div class="flex items-center space-x-2">
            <span class="w-3 h-3 rounded-full bg-[#ff5f56]"></span>
            <span class="w-3 h-3 rounded-full bg-[#ffbd2e]"></span>
            <span class="w-3 h-3 rounded-full bg-[#27c93f]"></span>
        </div>
        <div class="flex-1 max-w-xl mx-auto bg-[#121316] text-slate-300 py-1.5 px-4 rounded-full border border-slate-700/60 flex items-center gap-2 font-mono text-[11px]">
            <svg class="w-3.5 h-3.5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
            <span class="text-slate-400">http://localhost:8000</span>
            <span class="text-slate-600">—</span>
            <span class="text-sky-300">Icepol Copilot</span>
        </div>
        <div class="w-12"></div>
    </div>

    <!-- App Header -->
    <header class="border-b border-slate-800/80 bg-slate-900/70 backdrop-blur-md px-8 py-4 flex items-center justify-between sticky top-0 z-20">
        <div class="flex items-center gap-3">
            {polar_bear_svg}
        </div>
        <div class="flex items-center space-x-3 text-xs">
            <!-- LLM Pill -->
            <div class="relative">
                <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 shadow-sm cursor-pointer">
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span>LLM: <strong class="font-semibold text-emerald-300">llama3.2:3b</strong> <span class="opacity-75">(Ollama)</span></span>
                    <svg class="w-3 h-3 text-emerald-400/80" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
                </div>
                
                <!-- LLM Popover Menu -->
                <div class="{llm_popover_class} absolute top-full right-0 mt-2.5 w-72 bg-slate-900/95 border border-slate-700/80 rounded-2xl shadow-2xl p-4 z-50 backdrop-blur-xl space-y-3">
                    <div class="flex items-center justify-between pb-2.5 border-b border-slate-800">
                        <div class="flex items-center gap-2">
                            <div class="w-6 h-6 rounded-lg bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
                                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                            </div>
                            <span class="font-semibold text-white text-xs">Ollama Model Central</span>
                        </div>
                        <span class="inline-flex items-center gap-1 text-[10px] text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
                            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                            Conectado
                        </span>
                    </div>
                    <div class="space-y-1.5">
                        <div class="text-[10px] font-mono text-slate-400 uppercase tracking-wider">Modelos Disponíveis</div>
                        <div class="space-y-1">
                            <div class="px-2.5 py-1.5 text-xs rounded-xl flex items-center justify-between font-mono bg-emerald-500/20 text-emerald-300 font-semibold border border-emerald-500/30">
                                <span>llama3.2:3b</span>
                                <span class="text-emerald-400 font-bold ml-1.5 text-xs">✓ Ativo</span>
                            </div>
                            <div class="px-2.5 py-1.5 text-xs rounded-xl flex items-center justify-between font-mono text-slate-300 bg-slate-800/60">
                                <span>llama3.2:1b</span>
                                <span class="text-slate-500 text-xs">Disponível</span>
                            </div>
                        </div>
                    </div>
                    <div class="bg-slate-950/70 rounded-xl p-2.5 border border-slate-800/80 space-y-1.5 text-[11px]">
                        <div class="flex justify-between text-slate-400"><span>Provedor:</span><span class="text-slate-200 font-mono">Ollama Local</span></div>
                        <div class="flex justify-between text-slate-400"><span>Temperatura:</span><span class="text-slate-200 font-mono">0.2 (SQL Exato)</span></div>
                        <div class="flex justify-between text-slate-400"><span>Latência do Engine:</span><span class="text-emerald-400 font-mono">⚡ 13.5ms (OK)</span></div>
                    </div>
                    <button class="w-full py-2 bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 rounded-xl text-xs font-medium flex items-center justify-center gap-1.5">
                        <span>⚡ Testar Latência do LLM</span>
                    </button>
                </div>
            </div>

            <!-- DuckDB Pill -->
            <div class="relative">
                <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full font-medium bg-blue-500/10 text-blue-400 border border-blue-500/30 shadow-sm cursor-pointer">
                    <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
                    <span>DuckDB Engine: <strong class="font-semibold text-blue-300">Ativo</strong></span>
                    <svg class="w-3 h-3 text-blue-400/80" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
                </div>

                <!-- DuckDB Popover Menu -->
                <div class="{duck_popover_class} absolute top-full right-0 mt-2.5 w-80 bg-slate-900/95 border border-slate-700/80 rounded-2xl shadow-2xl p-4 z-50 backdrop-blur-xl space-y-3">
                    <div class="flex items-center justify-between pb-2.5 border-b border-slate-800">
                        <div class="flex items-center gap-2">
                            <div class="w-6 h-6 rounded-lg bg-blue-500/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
                                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2 1.5 3 3.5 3h9c2 0 3.5-1 3.5-3V7M4 7c0-2 1.5-3 3.5-3h9c2 0 3.5 1 3.5 3M4 7h16m-16 5h16"/></svg>
                            </div>
                            <span class="font-semibold text-white text-xs">DuckDB Lakehouse</span>
                        </div>
                        <span class="inline-flex items-center gap-1 text-[10px] text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded-full border border-blue-500/20">
                            <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
                            In-Memory Ativo
                        </span>
                    </div>
                    <div class="bg-slate-950/70 rounded-xl p-2.5 border border-slate-800/80 space-y-1.5 text-[11px]">
                        <div class="flex justify-between text-slate-400"><span>Schema Canônico:</span><span class="text-blue-300 font-mono font-semibold">corporate_credit</span></div>
                        <div class="flex justify-between text-slate-400"><span>Catálogo Metastore:</span><span class="text-slate-200">Polaris Iceberg REST</span></div>
                        <div class="flex justify-between text-slate-400"><span>Armazenamento:</span><span class="text-slate-200 font-mono">MinIO S3</span></div>
                        <div class="flex justify-between text-slate-400"><span>Tempo de Execução:</span><span class="text-blue-400 font-mono">⚡ 2.01ms (OK)</span></div>
                    </div>
                    <div class="space-y-1.5">
                        <div class="flex items-center justify-between text-[10px] font-mono font-semibold text-slate-400 uppercase">
                            <span>Tabelas (16 tabelas)</span>
                        </div>
                        <div class="flex flex-wrap gap-1.5 max-h-32 overflow-y-auto pt-0.5">
                            <span class="px-2 py-1 bg-slate-800/80 text-slate-300 rounded-lg text-[11px] font-mono border border-slate-700/60">counterparts</span>
                            <span class="px-2 py-1 bg-slate-800/80 text-slate-300 rounded-lg text-[11px] font-mono border border-slate-700/60">facilities</span>
                            <span class="px-2 py-1 bg-slate-800/80 text-slate-300 rounded-lg text-[11px] font-mono border border-slate-700/60">collaterals</span>
                            <span class="px-2 py-1 bg-slate-800/80 text-slate-300 rounded-lg text-[11px] font-mono border border-slate-700/60">proposals</span>
                            <span class="px-2 py-1 bg-slate-800/80 text-slate-300 rounded-lg text-[11px] font-mono border border-slate-700/60">covenants</span>
                            <span class="px-2 py-1 bg-slate-800/80 text-slate-300 rounded-lg text-[11px] font-mono border border-slate-700/60">financial_statements</span>
                            <span class="px-2 py-1 bg-slate-800/80 text-slate-300 rounded-lg text-[11px] font-mono border border-slate-700/60">credit_limits</span>
                        </div>
                    </div>
                    <div class="grid grid-cols-2 gap-2 pt-1">
                        <button class="py-2 px-2 bg-blue-500/15 text-blue-300 border border-blue-500/30 rounded-xl text-[11px] font-medium flex items-center justify-center gap-1">
                            <span>⚡ Testar Engine</span>
                        </button>
                        <button class="py-2 px-2 bg-slate-800 text-slate-200 border border-slate-700 rounded-xl text-[11px] font-medium flex items-center justify-center gap-1">
                            <span>Listar Tabelas →</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </header>
    """

# Footer Pill
def browser_footer(typed_text=""):
    placeholder = "Peça ao llama3.2:3b" if not typed_text else ""
    return f"""
    <footer class="px-8 py-5 sticky bottom-0 z-20 bg-gradient-to-t from-slate-950 via-slate-950/80 to-transparent">
        <div class="max-w-4xl mx-auto">
            <div class="flex items-center bg-[#1e1f20] border border-slate-700/80 rounded-3xl px-3.5 py-2.5 shadow-2xl">
                <!-- + Attachment Button -->
                <button class="w-9 h-9 rounded-full flex items-center justify-center text-slate-300 hover:bg-white/10 shrink-0">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
                </button>
                <!-- Text Input -->
                <div class="flex-1 px-3 text-sm text-white font-sans flex items-center">
                    {f'<span class="text-white font-medium">{typed_text}</span><span class="w-1.5 h-4 bg-sky-400 inline-block ml-1 animate-pulse"></span>' if typed_text else f'<span class="text-slate-400">{placeholder}</span>'}
                </div>
                <!-- Right Controls -->
                <div class="flex items-center space-x-2 shrink-0 pr-1">
                    <div class="flex items-center gap-1.5 text-xs text-slate-300 px-3 py-1.5 rounded-full bg-white/5 border border-slate-700">
                        <span>llama3.2:3b</span>
                        <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
                    </div>
                    <button class="w-9 h-9 rounded-full flex items-center justify-center text-slate-300 hover:bg-white/10 shrink-0">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 02-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/></svg>
                    </button>
                    <button class="w-9 h-9 rounded-full bg-white text-slate-900 flex items-center justify-center shadow shrink-0">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 12h14M12 5l7 7-7 7"/></svg>
                    </button>
                </div>
            </div>
        </div>
    </footer>
    """

# 2. SCENE 2: Home View
scene2_html = f"""<!DOCTYPE html>
<html lang="pt-BR" class="h-full">
<head>
    <meta charset="UTF-8">
    <title>Icepol</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 flex flex-col h-full font-sans antialiased">
    {browser_header()}
    <main class="flex-1 overflow-y-auto px-8 py-8 flex flex-col justify-center">
        <div class="max-w-5xl mx-auto space-y-6 text-center">
            <div class="space-y-2">
                <h1 class="text-5xl font-medium tracking-tight bg-gradient-to-r from-blue-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent">
                    Olá, Mauricio
                </h1>
                <p class="text-2xl text-slate-400 font-normal">
                    Como posso ajudar com sua pesquisa hoje?
                </p>
            </div>
            <div class="flex flex-wrap items-center justify-center gap-2.5 max-w-2xl mx-auto pt-4">
                <span class="px-4 py-2.5 rounded-full bg-[#1e1f20] text-slate-300 border border-slate-700/60 text-sm font-medium">Exposição total por setor</span>
                <span class="px-4 py-2.5 rounded-full bg-[#1e1f20] text-slate-300 border border-slate-700/60 text-sm font-medium">Alavancagem por grupo econômico</span>
                <span class="px-4 py-2.5 rounded-full bg-[#1e1f20] text-slate-300 border border-slate-700/60 text-sm font-medium">Garantias por colateral</span>
                <span class="px-4 py-2.5 rounded-full bg-[#1e1f20] text-slate-300 border border-slate-700/60 text-sm font-medium">Descumprimento de covenants</span>
                <span class="px-4 py-2.5 rounded-full bg-[#1e1f20] text-sky-300 border border-sky-600/50 text-sm font-medium flex items-center gap-1.5 shadow-lg shadow-sky-950/50">
                    <span>📊 Diagrama de Entidades (Mermaid)</span>
                </span>
            </div>
        </div>
    </main>
    {browser_footer()}
</body>
</html>"""

# 3. SCENE 3: DuckDB Popover Active
scene3_html = f"""<!DOCTYPE html>
<html lang="pt-BR" class="h-full">
<head>
    <meta charset="UTF-8">
    <title>Icepol - DuckDB Popover</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 flex flex-col h-full font-sans antialiased">
    {browser_header(active_popover="duckdb")}
    <main class="flex-1 overflow-y-auto px-8 py-8 flex flex-col justify-center opacity-40">
        <div class="max-w-5xl mx-auto space-y-6 text-center">
            <h1 class="text-5xl font-medium tracking-tight text-slate-400">Olá, Mauricio</h1>
        </div>
    </main>
    {browser_footer()}
</body>
</html>"""

# 4. SCENE 4: LLM Popover Active
scene4_html = f"""<!DOCTYPE html>
<html lang="pt-BR" class="h-full">
<head>
    <meta charset="UTF-8">
    <title>Icepol - LLM Popover</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 flex flex-col h-full font-sans antialiased">
    {browser_header(active_popover="llm")}
    <main class="flex-1 overflow-y-auto px-8 py-8 flex flex-col justify-center opacity-40">
        <div class="max-w-5xl mx-auto space-y-6 text-center">
            <h1 class="text-5xl font-medium tracking-tight text-slate-400">Olá, Mauricio</h1>
        </div>
    </main>
    {browser_footer()}
</body>
</html>"""

# 5. SCENE 5: Semantic Query Result (Credit Exposure)
scene5_html = f"""<!DOCTYPE html>
<html lang="pt-BR" class="h-full">
<head>
    <meta charset="UTF-8">
    <title>Icepol - Consulta Analítica</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 flex flex-col h-full font-sans antialiased">
    {browser_header()}
    <main class="flex-1 overflow-y-auto px-8 py-6 space-y-6">
        <div class="max-w-5xl mx-auto space-y-6">
            <!-- User Message -->
            <div class="flex justify-end">
                <div class="bg-[#1e1f20] text-slate-100 px-5 py-3.5 rounded-3xl max-w-2xl border border-slate-700/80 text-sm shadow-xl flex items-center gap-3">
                    <span class="text-slate-300 font-medium">Qual a exposição total (total_exposure) por setor (sector)?</span>
                </div>
            </div>

            <!-- Assistant Notebook Cell -->
            <div class="w-full pt-2">
                <div class="bg-slate-900/90 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl">
                    <!-- Action Bar -->
                    <div class="bg-slate-950/80 border-b border-slate-800 px-5 py-3 flex items-center justify-between text-xs">
                        <div class="flex items-center gap-2.5">
                            <span class="font-mono text-emerald-400 font-bold bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">[Out 1]</span>
                            <span class="inline-flex items-center gap-1.5 font-mono text-purple-300 bg-purple-500/10 px-2.5 py-0.5 rounded-full border border-purple-500/20">llama3.2:3b</span>
                            <span class="text-slate-400 font-mono">DuckDB Engine</span>
                            <span class="text-slate-600">•</span>
                            <span class="text-slate-400 font-mono">⚡ 142ms <strong class="text-sky-300">(DuckDB: 2.1ms)</strong></span>
                            <span class="text-slate-600">•</span>
                            <span class="text-slate-400 font-mono">📊 6 registros</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <button class="px-2.5 py-1 bg-slate-800 text-slate-300 rounded-lg text-xs font-medium border border-slate-700 flex items-center gap-1">
                                <span>Copiar SQL</span>
                            </button>
                            <button class="px-2.5 py-1 bg-slate-800 text-slate-300 rounded-lg text-xs font-medium border border-slate-700 flex items-center gap-1">
                                <span>Exportar CSV</span>
                            </button>
                        </div>
                    </div>

                    <!-- View Tabs -->
                    <div class="flex items-center gap-2 border-b border-slate-800 px-6 pt-3 bg-slate-900/40 text-xs font-mono">
                        <span class="px-3 py-1.5 border-b-2 border-blue-500 text-blue-400 font-semibold">📊 Tabela de Resultados</span>
                        <span class="px-3 py-1.5 border-b-2 border-transparent text-slate-400">📄 Código SQL</span>
                        <span class="px-3 py-1.5 border-b-2 border-transparent text-slate-400">💾 JSON Bruto</span>
                        <span class="px-3 py-1.5 border-b-2 border-transparent text-slate-400">📝 Markdown Completo</span>
                    </div>

                    <!-- Data Table -->
                    <div class="p-6 space-y-4">
                        <div class="overflow-x-auto rounded-2xl border border-slate-800/80 bg-slate-950/60">
                            <table class="w-full text-left border-collapse text-xs">
                                <thead>
                                    <tr class="border-b border-slate-800 bg-slate-900/60 font-mono text-slate-300">
                                        <th class="py-3 px-4 font-semibold uppercase tracking-wider">#</th>
                                        <th class="py-3 px-4 font-semibold uppercase tracking-wider">sector (ds_cnae_sector)</th>
                                        <th class="py-3 px-4 font-semibold uppercase tracking-wider text-right">total_exposure (BRL)</th>
                                        <th class="py-3 px-4 font-semibold uppercase tracking-wider text-right">% Carteira</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-800/60 text-slate-300 font-mono">
                                    <tr class="hover:bg-slate-800/30">
                                        <td class="py-2.5 px-4 text-slate-500">1</td>
                                        <td class="py-2.5 px-4 text-white font-medium">Energia e Utilities</td>
                                        <td class="py-2.5 px-4 text-right text-emerald-400 font-bold">R$ 3.420.000.000,00</td>
                                        <td class="py-2.5 px-4 text-right text-slate-400">26.1%</td>
                                    </tr>
                                    <tr class="hover:bg-slate-800/30">
                                        <td class="py-2.5 px-4 text-slate-500">2</td>
                                        <td class="py-2.5 px-4 text-white font-medium">Indústria de Base & Mineração</td>
                                        <td class="py-2.5 px-4 text-right text-emerald-400 font-bold">R$ 2.910.000.000,00</td>
                                        <td class="py-2.5 px-4 text-right text-slate-400">22.2%</td>
                                    </tr>
                                    <tr class="hover:bg-slate-800/30">
                                        <td class="py-2.5 px-4 text-slate-500">3</td>
                                        <td class="py-2.5 px-4 text-white font-medium">Infraestrutura & Transporte</td>
                                        <td class="py-2.5 px-4 text-right text-emerald-400 font-bold">R$ 2.150.000.000,00</td>
                                        <td class="py-2.5 px-4 text-right text-slate-400">16.4%</td>
                                    </tr>
                                    <tr class="hover:bg-slate-800/30">
                                        <td class="py-2.5 px-4 text-slate-500">4</td>
                                        <td class="py-2.5 px-4 text-white font-medium">Agropecuária & Commodities</td>
                                        <td class="py-2.5 px-4 text-right text-emerald-400 font-bold">R$ 1.850.000.000,00</td>
                                        <td class="py-2.5 px-4 text-right text-slate-400">14.1%</td>
                                    </tr>
                                    <tr class="hover:bg-slate-800/30">
                                        <td class="py-2.5 px-4 text-slate-500">5</td>
                                        <td class="py-2.5 px-4 text-white font-medium">Varejo & Bens de Consumo</td>
                                        <td class="py-2.5 px-4 text-right text-emerald-400 font-bold">R$ 1.780.000.000,00</td>
                                        <td class="py-2.5 px-4 text-right text-slate-400">13.6%</td>
                                    </tr>
                                    <tr class="hover:bg-slate-800/30">
                                        <td class="py-2.5 px-4 text-slate-500">6</td>
                                        <td class="py-2.5 px-4 text-white font-medium">Tecnologia & Telecomunicações</td>
                                        <td class="py-2.5 px-4 text-right text-emerald-400 font-bold">R$ 1.120.000.000,00</td>
                                        <td class="py-2.5 px-4 text-right text-slate-400">8.5%</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
    {browser_footer("Qual a exposição total (total_exposure) por setor (sector)?")}
</body>
</html>"""

# 6. SCENE 6: Mermaid Diagram Result
scene6_html = f"""<!DOCTYPE html>
<html lang="pt-BR" class="h-full">
<head>
    <meta charset="UTF-8">
    <title>Icepol - Diagrama Mermaid</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'dark',
            securityLevel: 'loose',
            themeVariables: {{
                darkMode: true,
                background: '#090d16',
                primaryColor: '#1e293b',
                primaryTextColor: '#f8fafc',
                primaryBorderColor: '#38bdf8',
                lineColor: '#7dd3fc',
                secondaryColor: '#0f172a',
                tertiaryColor: '#1e293b'
            }}
        }});
    </script>
</head>
<body class="bg-slate-950 text-slate-100 flex flex-col h-full font-sans antialiased">
    {browser_header()}
    <main class="flex-1 overflow-y-auto px-8 py-6 space-y-6">
        <div class="max-w-5xl mx-auto space-y-6">
            <!-- User Message -->
            <div class="flex justify-end">
                <div class="bg-[#1e1f20] text-slate-100 px-5 py-3.5 rounded-3xl max-w-2xl border border-slate-700/80 text-sm shadow-xl flex items-center gap-3">
                    <span class="text-sky-300 font-medium">Mostre o diagrama de modelo das entidades (ERD) e relacionamentos de crédito</span>
                </div>
            </div>

            <!-- Assistant Notebook Cell with Mermaid -->
            <div class="w-full pt-2">
                <div class="bg-slate-900/90 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl">
                    <!-- Action Bar -->
                    <div class="bg-slate-950/80 border-b border-slate-800 px-5 py-3 flex items-center justify-between text-xs">
                        <div class="flex items-center gap-2.5">
                            <span class="font-mono text-emerald-400 font-bold bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">[Out 2]</span>
                            <span class="inline-flex items-center gap-1.5 font-mono text-purple-300 bg-purple-500/10 px-2.5 py-0.5 rounded-full border border-purple-500/20">llama3.2:3b</span>
                            <span class="text-slate-400 font-mono">Modelo Semântico Icepol</span>
                            <span class="text-slate-600">•</span>
                            <span class="text-sky-400 font-mono">📐 Mermaid ERD Renderizado</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <button class="px-2.5 py-1 bg-slate-800 text-slate-300 rounded-lg text-xs font-medium border border-slate-700">Copiar Mermaid</button>
                        </div>
                    </div>

                    <!-- Mermaid Card -->
                    <div class="p-6 space-y-4">
                        <div class="p-5 rounded-2xl bg-[#090d16] border border-slate-700/80 shadow-2xl overflow-x-auto flex flex-col items-center">
                            <div class="w-full flex items-center justify-between pb-3 mb-4 border-b border-slate-800 text-xs text-slate-400 font-mono">
                                <span class="flex items-center gap-2 text-sky-400 font-semibold text-sm">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"/></svg>
                                    Diagrama Conceitual de Entidades de Crédito Corporativo
                                </span>
                                <span class="text-xs bg-sky-500/10 text-sky-300 px-2.5 py-1 rounded-full border border-sky-500/20">Schema: corporate_credit</span>
                            </div>

                            <!-- Live Mermaid SVG -->
                            <div class="mermaid w-full flex justify-center py-2">
erDiagram
    COUNTERPARTS ||--o{ FACILITIES : "emits"
    COUNTERPARTS ||--o{ PROPOSALS : "requests"
    FACILITIES ||--o{ COLLATERALS : "secured_by"
    FACILITIES ||--o{ COVENANTS : "bounded_by"

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
        float vl_contracted
        string st_operation
    }

    COLLATERALS {
        string collateral_id PK
        string facility_id FK
        string tp_collateral
        float vl_appraisal
        string st_collateral
    }

    PROPOSALS {
        string proposal_id PK
        string counterpart_id FK
        float vl_requested
        string st_decision
    }

    COVENANTS {
        string covenant_id PK
        string facility_id FK
        string tp_covenant
        float vl_target
        string st_compliance
    }
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
    {browser_footer("Mostre o diagrama de modelo das entidades (ERD) e relacionamentos de crédito")}
</body>
</html>"""

# 7. SCENE 7: 80s Cyberpunk / Depeche Mode Outro Titlecard
scene7_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Icepol - 80s Outro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @keyframes neon-glow {
            0%, 100% { filter: drop-shadow(0 0 15px rgba(56, 189, 248, 0.6)) drop-shadow(0 0 35px rgba(168, 85, 247, 0.4)); }
            50% { filter: drop-shadow(0 0 25px rgba(56, 189, 248, 0.9)) drop-shadow(0 0 55px rgba(168, 85, 247, 0.6)); }
        }
        .neon-box {
            animation: neon-glow 3s ease-in-out infinite;
        }
        .retro-grid {
            background-size: 40px 40px;
            background-image: 
                linear-gradient(to right, rgba(56, 189, 248, 0.08) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(168, 85, 247, 0.08) 1px, transparent 1px);
        }
    </style>
</head>
<body class="bg-[#05070e] text-white flex items-center justify-center min-h-screen p-8 retro-grid font-sans antialiased overflow-hidden relative">
    <!-- Ambient 80s synth lights -->
    <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-600/20 rounded-full blur-[120px] pointer-events-none"></div>
    <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-sky-500/20 rounded-full blur-[120px] pointer-events-none"></div>

    <div class="w-full max-w-4xl bg-slate-950/80 border border-slate-700/80 rounded-3xl p-10 shadow-2xl backdrop-blur-2xl text-center space-y-8 neon-box relative z-10">
        <!-- Logo & Brand -->
        <div class="flex flex-col items-center space-y-4">
            <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-sky-400/20 via-slate-800/80 to-purple-500/20 border border-sky-400/40 flex items-center justify-center shadow-2xl">
                <svg width="48" height="48" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="outroBear" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#ffffff"/>
                            <stop offset="45%" stop-color="#38bdf8"/>
                            <stop offset="100%" stop-color="#a855f7"/>
                        </linearGradient>
                    </defs>
                    <path d="M10 6 C10 4 12 3 14 4 C15 4.8 15 6 15 7" stroke="url(#outroBear)" stroke-width="1.8" stroke-linecap="round" fill="rgba(56, 189, 248, 0.25)"/>
                    <path d="M15 7 L21 11 L28 14 L29 15.5 L26 17 L22 17" stroke="url(#outroBear)" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/>
                    <path d="M22 17 L20 21 L17 26 L12 26 L8 21 L8 14 L10 6" stroke="url(#outroBear)" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/>
                    <path d="M15 7 L17 14 L28 14" stroke="url(#outroBear)" stroke-width="1.3" stroke-linejoin="round"/>
                    <path d="M17 14 L22 17" stroke="url(#outroBear)" stroke-width="1.3" stroke-linejoin="round"/>
                    <path d="M17 14 L14 20 L20 21" stroke="url(#outroBear)" stroke-width="1.3" stroke-linejoin="round"/>
                    <circle cx="19.5" cy="12.5" r="1.3" fill="#ffffff"/>
                    <circle cx="28.5" cy="14.8" r="1" fill="#38bdf8"/>
                </svg>
            </div>
            <div>
                <h1 class="text-4xl font-extrabold tracking-tight font-mono bg-gradient-to-r from-sky-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent">
                    Icepol Semantic Copilot
                </h1>
                <p class="text-sm font-mono text-sky-400 tracking-widest uppercase pt-1">
                    Camada Semântica de Crédito Corporativo
                </p>
            </div>
        </div>

        <!-- Features Matrix -->
        <div class="grid grid-cols-3 gap-4 pt-2 text-left">
            <div class="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1">
                <div class="text-sky-400 font-mono text-xs font-semibold">⚡ DuckDB Lakehouse</div>
                <div class="text-slate-300 text-xs font-medium">Execuções analíticas in-memory em menos de 3ms.</div>
            </div>
            <div class="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1">
                <div class="text-purple-400 font-mono text-xs font-semibold">🧊 Apache Iceberg + Polaris</div>
                <div class="text-slate-300 text-xs font-medium">Metadados REST canônicos e storage MinIO S3 imutável.</div>
            </div>
            <div class="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1">
                <div class="text-emerald-400 font-mono text-xs font-semibold">📐 Mermaid + Ollama LLM</div>
                <div class="text-slate-300 text-xs font-medium">Visualização automática de ERD e zero adivinhação de schema.</div>
            </div>
        </div>

        <!-- GitHub & Host Footer -->
        <div class="pt-4 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400 font-mono">
            <span>Repos: <strong class="text-slate-200">github.com/Helfstein-one/icepol-semantic</strong></span>
            <span class="text-sky-400">Trilha Sonora: 80s Electronic Synthwave (Depeche Mode Style)</span>
        </div>
    </div>
</body>
</html>"""

# Write all HTML scenes
scenes = [
    ("video/scene2_home.html", scene2_html, "video/scene2_home.png"),
    ("video/scene3_duckdb.html", scene3_html, "video/scene3_duckdb.png"),
    ("video/scene4_llm.html", scene4_html, "video/scene4_llm.png"),
    ("video/scene5_query.html", scene5_html, "video/scene5_query.png"),
    ("video/scene6_mermaid.html", scene6_html, "video/scene6_mermaid.png"),
    ("video/scene7_outro.html", scene7_html, "video/scene7_outro.png"),
]

for html_file, content, png_file in scenes:
    with open(html_file, "w") as f:
        f.write(content)
    capture_html(html_file, png_file)

print("All scenes generated and captured successfully!")
