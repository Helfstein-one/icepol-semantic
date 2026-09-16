import os, subprocess

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

scene7_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Icepol - 80s Outro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .neon-glow {
            filter: drop-shadow(0 0 20px rgba(56, 189, 248, 0.7)) drop-shadow(0 0 45px rgba(168, 85, 247, 0.5));
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
    <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-600/20 rounded-full blur-[140px]"></div>
    <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-sky-500/20 rounded-full blur-[140px]"></div>

    <div class="w-full max-w-4xl bg-slate-950/85 border border-slate-700/80 rounded-3xl p-10 shadow-2xl backdrop-blur-2xl text-center space-y-8 neon-glow relative z-10">
        <div class="flex flex-col items-center space-y-4">
            <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-sky-400/20 via-slate-800/80 to-purple-500/20 border border-sky-400/50 flex items-center justify-center shadow-2xl">
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
                <p class="text-xs font-mono text-sky-400 tracking-widest uppercase pt-1">
                    Camada Semântica de Crédito Corporativo • Lakehouse In-Memory
                </p>
            </div>
        </div>

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

        <div class="pt-4 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400 font-mono">
            <span>GitHub: <strong class="text-slate-200">github.com/Helfstein-one/icepol-semantic</strong></span>
            <span class="text-sky-400 font-semibold">🎵 80s Electronic Punk / Depeche Mode Soundtrack</span>
        </div>
    </div>
</body>
</html>"""

with open("video/scene7_outro.html", "w") as f:
    f.write(scene7_html)
capture_html("video/scene7_outro.html", "video/scene7_outro.png")
