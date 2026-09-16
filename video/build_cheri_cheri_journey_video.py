import os
import subprocess

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUTPUT_DIR = "video"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 10 Detailed Scenes for the complete User Journey:
# S1: GitHub Repo Top (Browsing header, repo description, releases, tags)
# S2: GitHub Repo Scrolling (Viewing files: core/, semantic/, docker-compose, README)
# S3: Terminal 1 - Git clone & cd icepol-semantic
# S4: Terminal 2 - make seed (populating 7 synthetic parquets) & podman compose up -d (containers running)
# S5: Chat UI Welcome (Prompt pill, deepseek-r1:1.5b selector, polar bear logo, mic, file upload)
# S6: Chat UI Asking Question (Typing corporate credit query)
# S7: Chat UI Response & DuckDB Table (Vectorized execution in 180ms, risk metrics)
# S8: Chat UI Mermaid ERD Relational Modeling (Full 7 entities with Crow's foot cardinality)
# S9: Langfuse Observability & Tracing Deep-Dive (Trace tree, spans waterfall: 328ms parsing, 776ms R1, 180ms DuckDB)
# S10: Token Analytics & Cost Breakdown (Highlighting where tokens are spent: 63.7% ontology, 21% CoT reasoning, 15.3% SQL output)

scenes = [
    # Scene 1: GitHub Repo Top View
    ("cheri_s1.html", """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }
  body { background: #0d1117; color: #c9d1d9; width: 1920px; height: 1080px; overflow: hidden; display: flex; flex-direction: column; }
  header { height: 68px; background: #161b22; border-bottom: 1px solid #30363d; display: flex; align-items: center; justify-content: space-between; padding: 0 40px; }
  .nav-left { display: flex; align-items: center; gap: 16px; }
  .github-logo { fill: #ffffff; width: 34px; height: 34px; }
  .repo-path { font-size: 20px; font-weight: 600; color: #58a6ff; }
  .repo-path span { color: #8b949e; margin: 0 4px; }
  .badge-public { border: 1px solid #30363d; border-radius: 20px; padding: 3px 10px; font-size: 12px; color: #8b949e; }
  .nav-right { display: flex; gap: 12px; }
  .btn-gh { background: #21262d; border: 1px solid #30363d; color: #c9d1d9; padding: 6px 14px; border-radius: 6px; font-size: 13px; font-weight: 600; }
  .btn-primary { background: #238636; border-color: #2ea043; color: #ffffff; }

  .main-content { flex: 1; padding: 32px 50px; display: grid; grid-template-columns: 1fr 340px; gap: 32px; }
  .repo-header { margin-bottom: 20px; }
  .repo-desc { font-size: 17px; color: #c9d1d9; line-height: 1.5; font-weight: 400; }
  .tags-row { display: flex; gap: 8px; margin-top: 12px; }
  .tag { background: #1f242c; color: #58a6ff; font-size: 12px; padding: 4px 12px; border-radius: 12px; }

  .file-box { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; overflow: hidden; margin-top: 16px; }
  .file-header { background: #161b22; padding: 14px 20px; border-bottom: 1px solid #30363d; display: flex; justify-content: space-between; align-items: center; font-size: 13px; }
  .file-row { display: flex; justify-content: space-between; padding: 12px 20px; border-bottom: 1px solid #21262d; font-size: 14px; }
  .file-name { color: #c9d1d9; font-weight: 500; }

  .clone-popover {
    position: absolute; right: 410px; top: 120px; width: 440px; background: #161b22; border: 1px solid #30363d;
    border-radius: 8px; padding: 18px; box-shadow: 0 16px 36px rgba(0,0,0,0.6); z-index: 10;
  }
  .clone-title { font-size: 14px; font-weight: 700; color: #ffffff; margin-bottom: 10px; }
  .clone-bar { background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 10px; display: flex; justify-content: space-between; align-items: center; }
  .clone-url { font-family: monospace; font-size: 13px; color: #58a6ff; }
  
  .side-card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
  .side-title { font-size: 14px; font-weight: 600; color: #ffffff; margin-bottom: 12px; }
</style>
</head>
<body>
  <header>
    <div class="nav-left">
      <svg class="github-logo" viewBox="0 0 16 16"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
      <div class="repo-path">Helfstein-one <span>/</span> <b>icepol-semantic</b></div>
      <span class="badge-public">Public</span>
    </div>
    <div class="nav-right">
      <button class="btn-gh">⭐ Star (54)</button>
      <button class="btn-gh">🍴 Fork (15)</button>
      <button class="btn-gh btn-primary">&lt;&gt; Code ▾</button>
    </div>
  </header>

  <div class="main-content">
    <div>
      <div class="repo-header">
        <div class="repo-desc">Ecossistema Local de Inteligência Analítica em Crédito Corporativo (Wholesale Banking) com Camada Semântica, DuckDB, Apache Iceberg, Langfuse Tracing e MySQL 8.</div>
        <div class="tags-row">
          <span class="tag">semantic-layer</span>
          <span class="tag">apache-iceberg</span>
          <span class="tag">duckdb</span>
          <span class="tag">langfuse</span>
          <span class="tag">deepseek-r1</span>
          <span class="tag">mysql-audit</span>
        </div>
      </div>

      <div class="file-box">
        <div class="file-header">
          <span><b>main</b> • 28 commits • Último commit: <i>feat: tracing waterfall & token spend analysis</i></span>
          <span style="color:#58a6ff;">Commit 2dd6962</span>
        </div>
        <div class="file-row">
          <div class="file-name">📁 core/</div>
          <div style="color:#8b949e;">FastAPI agent, DuckDB engine, Langfuse tracer & MySQL logger</div>
          <div style="color:#6e7681;">hoje</div>
        </div>
        <div class="file-row">
          <div class="file-name">📁 semantic/</div>
          <div style="color:#8b949e;">Ontologias YAML de Crédito Corporativo e compilador AST</div>
          <div style="color:#6e7681;">hoje</div>
        </div>
        <div class="file-row">
          <div class="file-name">📁 video/</div>
          <div style="color:#8b949e;">Vídeos de demonstração da jornada completa</div>
          <div style="color:#6e7681;">hoje</div>
        </div>
        <div class="file-row">
          <div class="file-name">📄 docker-compose.yml</div>
          <div style="color:#8b949e;">Pilha completa: MinIO, Polaris, MySQL 8, Postgres e Langfuse</div>
          <div style="color:#6e7681;">hoje</div>
        </div>
        <div class="file-row">
          <div class="file-name">📄 README.md</div>
          <div style="color:#8b949e;">Documentação completa com diagramas de tracing e tokens</div>
          <div style="color:#6e7681;">hoje</div>
        </div>
      </div>
    </div>

    <div>
      <div class="side-card">
        <div class="side-title">About</div>
        <p style="font-size:13px; color:#8b949e; line-height:1.4;">Data Lakehouse com Camada Semântica para Wholesale Banking e IA com auditoria regulatória contínua.</p>
      </div>
      <div class="side-card">
        <div class="side-title">Releases</div>
        <p style="font-size:13px; color:#58a6ff; font-weight:600;">v1.2.0 • Latest</p>
        <p style="font-size:12px; color:#8b949e; margin-top:4px;">Suporte a DeepSeek-R1, Langfuse Tracing e Crow's foot ERD.</p>
      </div>
    </div>
  </div>

  <div class="clone-popover">
    <div class="clone-title">Clone com HTTPS</div>
    <div class="clone-bar">
      <span class="clone-url">git clone https://github.com/Helfstein-one/icepol-semantic.git</span>
      <span style="font-size:12px; background:#238636; color:#fff; padding:4px 8px; border-radius:4px; font-weight:bold;">COPY</span>
    </div>
  </div>
</body>
</html>
"""),

    # Scene 2: GitHub Repo Scrolling (Exploring README & Tracing Diagrams)
    ("cheri_s2.html", """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }
  body { background: #0d1117; color: #c9d1d9; width: 1920px; height: 1080px; overflow: hidden; display: flex; flex-direction: column; }
  header { height: 68px; background: #161b22; border-bottom: 1px solid #30363d; display: flex; align-items: center; justify-content: space-between; padding: 0 40px; }
  .repo-path { font-size: 20px; font-weight: 600; color: #58a6ff; }
  .repo-path span { color: #8b949e; margin: 0 4px; }

  /* Scrolled View into README */
  .readme-scroll { flex: 1; padding: 40px 180px; overflow: hidden; display: flex; flex-direction: column; gap: 24px; }
  .readme-box { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 36px 48px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
  h2 { font-size: 24px; font-weight: 700; color: #ffffff; border-bottom: 1px solid #21262d; padding-bottom: 12px; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }
  p { font-size: 15px; color: #8b949e; line-height: 1.6; margin-bottom: 20px; }
  
  .diagram-mock { background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 24px; display: flex; justify-content: space-between; align-items: center; }
  .node { background: #1f242c; border: 1px solid #38bdf8; color: #f1f5f9; padding: 14px 20px; border-radius: 8px; font-size: 13px; font-weight: 600; text-align: center; }
  .arrow { color: #38bdf8; font-size: 20px; font-weight: bold; }
</style>
</head>
<body>
  <header>
    <div class="repo-path">Helfstein-one <span>/</span> <b>icepol-semantic</b> • README.md (Visualização da Arquitetura)</div>
    <div style="font-size: 13px; color: #10b981; font-weight: bold;">✔ Camada Semântica & Observabilidade</div>
  </header>

  <div class="readme-scroll">
    <div class="readme-box">
      <h2>🔍 Observabilidade Corporativa (Langfuse, MinIO S3 & MySQL 8.0)</h2>
      <p>O Icepol integra uma pilha corporativa completa para auditoria regulatória, rastreabilidade de ponta a ponta e mitigação de alucinações em produção:</p>
      
      <div class="diagram-mock">
        <div class="node">🗣️ Usuário / Prompt<br><span style="font-size:11px; color:#94a3b8;">Linguagem Natural</span></div>
        <div class="arrow">➔</div>
        <div class="node" style="border-color:#a78bfa;">📜 Camada Semântica<br><span style="font-size:11px; color:#94a3b8;">YAML & AST Compiler</span></div>
        <div class="arrow">➔</div>
        <div class="node" style="border-color:#f472b6;">🧠 DeepSeek-R1 (1.5B)<br><span style="font-size:11px; color:#94a3b8;">CoT &lt;think&gt; Raciocínio</span></div>
        <div class="arrow">➔</div>
        <div class="node" style="border-color:#34d399;">🦆 DuckDB In-Memory<br><span style="font-size:11px; color:#94a3b8;">Iceberg Parquet S3</span></div>
        <div class="arrow">➔</div>
        <div class="node" style="border-color:#fbbf24;">⚡ Langfuse & MySQL<br><span style="font-size:11px; color:#94a3b8;">Spans & Auditoria 100%</span></div>
      </div>

      <div style="margin-top: 24px; padding: 16px; background: #161b22; border-left: 4px solid #38bdf8; border-radius: 4px; font-size: 14px; color: #cbd5e1;">
        <b>Zero Alucinação de Schema:</b> O modelo nunca acessa nomes de tabelas brutas diretamente; todas as métricas são regradas no dicionário semântico canônico.
      </div>
    </div>
  </div>
</body>
</html>
"""),

    # Scene 3: Terminal 1 - Git Clone
    ("cheri_s3.html", """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Fira Code', Menlo, monospace; }
  body { background: #080c14; color: #38bdf8; width: 1920px; height: 1080px; overflow: hidden; display: flex; flex-direction: column; padding: 40px 60px; }
  .term-window { flex: 1; background: #0f172a; border: 1px solid #1e293b; border-radius: 16px; box-shadow: 0 25px 60px rgba(0,0,0,0.8); display: flex; flex-direction: column; overflow: hidden; }
  .title-bar { height: 48px; background: #1e293b; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; border-bottom: 1px solid #334155; }
  .traffic-lights { display: flex; gap: 8px; }
  .circle { width: 12px; height: 12px; border-radius: 50%; }
  .red { background: #ef4444; } .yellow { background: #f59e0b; } .green { background: #10b981; }
  .term-body { flex: 1; padding: 36px 44px; font-size: 16px; line-height: 1.8; color: #e2e8f0; }
  .prompt { color: #10b981; font-weight: bold; }
  .cmd { color: #f8fafc; font-weight: 600; }
  .dim { color: #64748b; }
  .success { color: #34d399; font-weight: 600; }
</style>
</head>
<body>
  <div class="term-window">
    <div class="title-bar">
      <div class="traffic-lights"><div class="circle red"></div><div class="circle yellow"></div><div class="circle green"></div></div>
      <div style="font-size:13px; color:#94a3b8; font-weight:600;">terminal: ~/dev (zsh) — Clonando o Repositório</div>
      <div style="font-size:12px; color:#64748b;">1920x1080</div>
    </div>
    <div class="term-body">
      <p><span class="prompt">➜  dev</span> <span class="cmd">git clone https://github.com/Helfstein-one/icepol-semantic.git</span></p>
      <p class="dim">Cloning into 'icepol-semantic'...</p>
      <p class="dim">remote: Enumerating objects: 412, done.</p>
      <p class="dim">remote: Counting objects: 100% (412/412), done.</p>
      <p class="dim">remote: Compressing objects: 100% (238/238), done.</p>
      <p class="success">remote: Total 412 (delta 234), reused 390 (delta 218), pack-reused 0</p>
      <p class="success">Receiving objects: 100% (412/412), 16.40 MiB | 24.12 MiB/s, done.</p>
      <p class="success">Resolving deltas: 100% (234/234), done.</p>
      <br>
      <p><span class="prompt">➜  dev</span> <span class="cmd">cd icepol-semantic</span></p>
      <p><span class="prompt">➜  icepol-semantic (main)</span> <span class="cmd">ls -la</span></p>
      <p class="dim">total 128</p>
      <p class="dim">drwxr-xr-x   core/          (FastAPI Agent & DuckDB Engine)</p>
      <p class="dim">drwxr-xr-x   semantic/      (Ontologias YAML de Crédito)</p>
      <p class="dim">-rw-r--r--   docker-compose.yml</p>
      <p class="dim">-rw-r--r--   requirements.txt</p>
      <p class="dim">-rw-r--r--   Makefile</p>
    </div>
  </div>
</body>
</html>
"""),

    # Scene 4: Terminal 2 - Make Seed & Podman Compose Up
    ("cheri_s4.html", """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Fira Code', Menlo, monospace; }
  body { background: #080c14; color: #38bdf8; width: 1920px; height: 1080px; overflow: hidden; display: flex; flex-direction: column; padding: 40px 60px; }
  .term-window { flex: 1; background: #0f172a; border: 1px solid #1e293b; border-radius: 16px; box-shadow: 0 25px 60px rgba(0,0,0,0.8); display: flex; flex-direction: column; overflow: hidden; }
  .title-bar { height: 48px; background: #1e293b; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; border-bottom: 1px solid #334155; }
  .traffic-lights { display: flex; gap: 8px; }
  .circle { width: 12px; height: 12px; border-radius: 50%; }
  .red { background: #ef4444; } .yellow { background: #f59e0b; } .green { background: #10b981; }
  .term-body { flex: 1; padding: 36px 44px; font-size: 15px; line-height: 1.7; color: #e2e8f0; }
  .prompt { color: #10b981; font-weight: bold; }
  .cmd { color: #f8fafc; font-weight: 600; }
  .dim { color: #64748b; }
  .success { color: #34d399; }
  .highlight { color: #fbbf24; }
  .info { color: #38bdf8; }
</style>
</head>
<body>
  <div class="term-window">
    <div class="title-bar">
      <div class="traffic-lights"><div class="circle red"></div><div class="circle yellow"></div><div class="circle green"></div></div>
      <div style="font-size:13px; color:#94a3b8; font-weight:600;">terminal: ~/dev/icepol-semantic (zsh) — Setup & Containers</div>
      <div style="font-size:12px; color:#64748b;">1920x1080</div>
    </div>
    <div class="term-body">
      <p><span class="prompt">➜  icepol-semantic</span> <span class="cmd">make seed</span></p>
      <p class="info">🌱 [SEED] Gerando 7 tabelas físicas sintéticas de Crédito Corporativo no Iceberg...</p>
      <p class="dim">  ✔ counterparts.parquet (1,000 tomadores de crédito, CNAE, Ratings)</p>
      <p class="dim">  ✔ facilities.parquet (3,500 operações ativas de crédito)</p>
      <p class="dim">  ✔ collaterals.parquet (4,200 garantias reais e recebíveis)</p>
      <p class="dim">  ✔ proposals.parquet (2,800 deliberações de comitês de risco)</p>
      <p class="dim">  ✔ financial_statements.parquet (Dívida Líquida, EBITDA, Balanços auditados)</p>
      <p class="dim">  ✔ credit_limits.parquet (Limites globais aprovados e tomados)</p>
      <p class="dim">  ✔ covenants.parquet (Cláusulas de desenquadramento financeiro)</p>
      <p class="success">✨ 7 Tabelas registradas no Apache Polaris REST Catalog e MinIO S3!</p>
      <br>
      <p><span class="prompt">➜  icepol-semantic</span> <span class="cmd">podman compose up -d</span></p>
      <p><span class="success">✔ Container minio-storage</span>     <span class="highlight">Running</span> (S3 API :9000, Console :9001)</p>
      <p><span class="success">✔ Container polaris-catalog</span>   <span class="highlight">Running</span> (Apache Iceberg REST :8181)</p>
      <p><span class="success">✔ Container mysql-db</span>          <span class="highlight">Running</span> (Auditoria & Métricas :3306)</p>
      <p><span class="success">✔ Container postgres-langfuse</span> <span class="highlight">Running</span> (Metadata Storage :5432)</p>
      <p><span class="success">✔ Container langfuse-server</span>   <span class="highlight">Running</span> (LLM Observability Dashboard :3001)</p>
      <p><span class="success">✔ Container semantic-agent</span>    <span class="highlight">Running</span> (FastAPI Web Chat :8000)</p>
      <br>
      <p><span class="prompt">➜  icepol-semantic</span> <span class="cmd">open http://localhost:8000</span></p>
    </div>
  </div>
</body>
</html>
"""),

    # Scene 5: Chat UI Welcome Screen
    ("cheri_s5.html", """<!DOCTYPE html>
<html lang="pt-BR" class="h-full bg-slate-950">
<head>
  <meta charset="utf-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <style> body { width: 1920px; height: 1080px; overflow: hidden; } </style>
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

    <!-- Prompt Pill -->
    <div class="w-full max-w-3xl">
      <div class="relative bg-slate-900/90 border border-slate-700/80 rounded-3xl p-3 shadow-2xl backdrop-blur-xl flex items-center gap-3">
        <button class="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center text-slate-300 text-lg font-bold border border-slate-700">+</button>
        <div class="px-3 py-1.5 rounded-full bg-slate-800 border border-sky-500/40 text-xs font-semibold text-sky-400 flex items-center gap-1.5">
          <span>deepseek-r1:1.5b</span>
          <span class="text-[10px]">▾</span>
        </div>
        <input type="text" placeholder="Peça ao deepseek-r1:1.5b..." class="bg-transparent text-sm text-slate-200 placeholder-slate-500 focus:outline-none flex-1" />
        <button class="w-10 h-10 rounded-full bg-slate-800 text-slate-400 flex items-center justify-center text-base">🎙️</button>
        <button class="w-10 h-10 rounded-full bg-sky-600 text-white flex items-center justify-center text-sm font-bold shadow-md shadow-sky-600/30">➔</button>
      </div>
    </div>
  </main>
</body>
</html>
"""),

    # Scene 6: User Asking Question
    ("cheri_s6.html", """<!DOCTYPE html>
<html lang="pt-BR" class="h-full bg-slate-950">
<head>
  <meta charset="utf-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <style> body { width: 1920px; height: 1080px; overflow: hidden; } </style>
</head>
<body class="bg-slate-950 text-slate-100 flex flex-col h-full font-sans antialiased">
  <header class="border-b border-slate-800/80 bg-slate-900/70 backdrop-blur-md px-10 py-4 flex items-center justify-between sticky top-0 z-20">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-sky-500/20 via-slate-800 to-slate-900 border border-sky-500/30 flex items-center justify-center">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><path d="M12 2C6.48 2 2 6.48 2 12c0 5.52 4.48 10 10 10s10-4.48 10-10C22 6.48 17.52 2 12 2zm1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
      </div>
      <div>
        <h1 class="text-xl font-bold tracking-tight text-white">Icepol Semantic Layer</h1>
        <p class="text-xs text-slate-400">Inteligência Analítica em Crédito Corporativo • Apache Iceberg & DuckDB</p>
      </div>
    </div>
    
    <div class="flex items-center gap-3">
      <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
        <span>LLM: <strong class="text-emerald-300">deepseek-r1:1.5b</strong></span>
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

    <!-- Active Typing -->
    <div class="w-full max-w-3xl">
      <div class="relative bg-slate-900/95 border-2 border-sky-500 rounded-3xl p-3.5 shadow-2xl shadow-sky-950/60 flex items-center gap-3">
        <button class="w-10 h-10 rounded-full bg-slate-800 text-slate-300 text-lg font-bold border border-slate-700">+</button>
        <div class="px-3.5 py-1.5 rounded-full bg-sky-950/80 border border-sky-500/60 text-xs font-bold text-sky-300">deepseek-r1:1.5b</div>
        <div class="text-sm font-medium text-slate-100 flex-1">
          Qual a exposição total e alavancagem média por setor? Gere também o modelo relacional Mermaid.
        </div>
        <button class="w-10 h-10 rounded-full bg-slate-800 text-slate-400 flex items-center justify-center text-base">🎙️</button>
        <button class="w-10 h-10 rounded-full bg-sky-500 text-white flex items-center justify-center text-sm font-bold shadow-lg shadow-sky-500/40">➔</button>
      </div>
    </div>
  </main>
</body>
</html>
"""),

    # Scene 7: Chat UI Response with DuckDB Table
    ("cheri_s7.html", """<!DOCTYPE html>
<html lang="pt-BR" class="h-full bg-slate-950">
<head>
  <meta charset="utf-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <style> body { width: 1920px; height: 1080px; overflow: hidden; } </style>
</head>
<body class="bg-slate-950 text-slate-100 flex flex-col h-full font-sans antialiased">
  <header class="border-b border-slate-800/80 bg-slate-900/70 backdrop-blur-md px-10 py-4 flex items-center justify-between sticky top-0 z-20">
    <div class="flex items-center gap-3">
      <h1 class="text-xl font-bold text-white">Icepol Semantic Layer</h1>
      <span class="text-xs text-slate-400">• Execução Analítica DuckDB (180ms)</span>
    </div>
    <div class="flex items-center gap-3 text-xs">
      <span class="px-3 py-1.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-semibold">deepseek-r1:1.5b</span>
      <span class="px-3 py-1.5 rounded-full bg-purple-500/10 text-purple-400 border border-purple-500/20 font-semibold">⚡ 1.49s Total</span>
    </div>
  </header>

  <main class="flex-1 p-10 max-w-5xl mx-auto w-full space-y-6">
    <div class="flex justify-end">
      <div class="bg-sky-600 text-white rounded-2xl rounded-tr-none px-5 py-3 max-w-xl text-sm font-medium">
        Qual a exposição total e alavancagem média por setor? Gere também o modelo relacional Mermaid.
      </div>
    </div>

    <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-5">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3 text-xs text-slate-400">
        <span><b>deepseek-r1:1.5b</b> • DuckDB Engine • Zero Alucinação</span>
        <span class="font-mono text-sky-400">Trace: tr_icepol_8f492a</span>
      </div>

      <div class="overflow-hidden border border-slate-800 rounded-xl bg-slate-950/60">
        <table class="w-full text-left text-sm">
          <thead class="bg-slate-900/80 text-xs text-slate-400 border-b border-slate-800 font-semibold">
            <tr>
              <th class="p-3">Setor Econômico (CNAE)</th>
              <th class="p-3">Exposição Total (total_exposure)</th>
              <th class="p-3">Alavancagem Média (Dívida/EBITDA)</th>
              <th class="p-3">Status de Risco</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800/60 text-slate-300">
            <tr>
              <td class="p-3 font-medium text-white">Indústria & Manufatura</td>
              <td class="p-3 font-mono text-sky-400 font-bold">R$ 4.820.000.000</td>
              <td class="p-3 font-mono">2.1x</td>
              <td class="p-3"><span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400">Baixo</span></td>
            </tr>
            <tr>
              <td class="p-3 font-medium text-white">Agronegócio & Grãos</td>
              <td class="p-3 font-mono text-sky-400 font-bold">R$ 3.650.000.000</td>
              <td class="p-3 font-mono">1.8x</td>
              <td class="p-3"><span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400">Baixo</span></td>
            </tr>
            <tr>
              <td class="p-3 font-medium text-white">Varejo & Consumo</td>
              <td class="p-3 font-mono text-sky-400 font-bold">R$ 2.410.000.000</td>
              <td class="p-3 font-mono text-amber-400 font-bold">3.4x</td>
              <td class="p-3"><span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400">Atenção</span></td>
            </tr>
            <tr>
              <td class="p-3 font-medium text-white">Energia & Infraestrutura</td>
              <td class="p-3 font-mono text-sky-400 font-bold">R$ 1.950.000.000</td>
              <td class="p-3 font-mono">1.4x</td>
              <td class="p-3"><span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400">Ótimo</span></td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="flex items-center gap-3">
        <span class="px-3.5 py-1.5 rounded-lg bg-sky-600/20 text-sky-300 border border-sky-500/40 text-xs font-bold">📐 Aba Mermaid Ativa ➔</span>
        <span class="text-xs text-slate-400">Renderização em SVG com Crow's foot cardinality</span>
      </div>
    </div>
  </main>
</body>
</html>
"""),

    # Scene 8: Chat UI Mermaid Relational Modeling (7 Entities Crow's Foot)
    ("cheri_s8.html", """<!DOCTYPE html>
<html lang="pt-BR" class="h-full bg-slate-950">
<head>
  <meta charset="utf-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <style> body { width: 1920px; height: 1080px; overflow: hidden; } </style>
</head>
<body class="bg-slate-950 text-slate-100 flex flex-col h-full font-sans antialiased">
  <header class="border-b border-slate-800/80 bg-slate-900/70 backdrop-blur-md px-10 py-4 flex items-center justify-between sticky top-0 z-20">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-xl bg-sky-500/20 border border-sky-500/40 flex items-center justify-center">📐</div>
      <div>
        <h1 class="text-xl font-bold tracking-tight text-white">Modelo Conceitual de Crédito Corporativo (Mermaid ERD)</h1>
        <p class="text-xs text-slate-400">7 Entidades com Notação Crow's foot (1:N e N:M) • Zero Erros de Renderização</p>
      </div>
    </div>
    <div class="px-3 py-1.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-bold">
      ✔ Sanitização Estrita & Crow's Foot Ativo
    </div>
  </header>

  <main class="flex-1 p-10 flex items-center justify-center">
    <div class="w-full max-w-6xl bg-slate-900/90 border border-slate-800 rounded-3xl p-8 shadow-2xl">
      <div class="grid grid-cols-4 gap-6 mb-8">
        <div class="bg-slate-950 border border-sky-500/40 rounded-xl overflow-hidden shadow-lg">
          <div class="bg-sky-600 text-white text-xs font-bold text-center py-2">COUNTERPARTS</div>
          <div class="p-3 text-[11px] font-mono space-y-1 text-slate-300">
            <div class="text-pink-400 font-bold">PK counterpart_id</div>
            <div>string nm_counterpart</div>
            <div>string ds_cnae_sector</div>
            <div>string cd_rating</div>
          </div>
        </div>

        <div class="bg-slate-950 border border-sky-500/40 rounded-xl overflow-hidden shadow-lg">
          <div class="bg-sky-600 text-white text-xs font-bold text-center py-2">FACILITIES</div>
          <div class="p-3 text-[11px] font-mono space-y-1 text-slate-300">
            <div class="text-pink-400 font-bold">PK facility_id</div>
            <div class="text-sky-400 font-semibold">FK counterpart_id</div>
            <div>string tp_operation</div>
            <div>double vl_credit_limit</div>
          </div>
        </div>

        <div class="bg-slate-950 border border-sky-500/40 rounded-xl overflow-hidden shadow-lg">
          <div class="bg-sky-600 text-white text-xs font-bold text-center py-2">COLLATERALS</div>
          <div class="p-3 text-[11px] font-mono space-y-1 text-slate-300">
            <div class="text-pink-400 font-bold">PK collateral_id</div>
            <div class="text-sky-400 font-semibold">FK facility_id</div>
            <div>string tp_collateral</div>
            <div>double vl_appraised</div>
          </div>
        </div>

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
        <div class="bg-slate-950 border border-purple-500/40 rounded-xl overflow-hidden shadow-lg">
          <div class="bg-purple-600 text-white text-xs font-bold text-center py-2">FINANCIAL_STATEMENTS</div>
          <div class="p-3 text-[11px] font-mono space-y-1 text-slate-300">
            <div class="text-pink-400 font-bold">PK statement_id</div>
            <div class="text-sky-400 font-semibold">FK counterpart_id</div>
            <div>double vl_net_debt</div>
            <div>double vl_ebitda</div>
          </div>
        </div>

        <div class="bg-slate-950 border border-purple-500/40 rounded-xl overflow-hidden shadow-lg">
          <div class="bg-purple-600 text-white text-xs font-bold text-center py-2">CREDIT_LIMITS</div>
          <div class="p-3 text-[11px] font-mono space-y-1 text-slate-300">
            <div class="text-pink-400 font-bold">PK limit_id</div>
            <div class="text-sky-400 font-semibold">FK counterpart_id</div>
            <div>double approved_limit</div>
            <div>double used_limit</div>
          </div>
        </div>

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
        <div>Relacionamentos: <b>||--o{</b> (1 para N) e <b>}|--|{</b> (N para N)</div>
        <div class="text-sky-400 font-mono">Próxima Parada: Langfuse Observability & Tracing ➔</div>
      </div>
    </div>
  </main>
</body>
</html>
"""),

    # Scene 9: Langfuse Observability & Tracing Spans Waterfall
    ("cheri_s9.html", """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; }
  body { background: #0b0f19; color: #f1f5f9; width: 1920px; height: 1080px; overflow: hidden; display: flex; flex-direction: column; }
  header { height: 64px; background: #111827; border-bottom: 1px solid #1f2937; display: flex; align-items: center; justify-content: space-between; padding: 0 40px; }
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
    <div style="font-size:13px; color:#10b981; font-weight:600;">Trace ID: tr_icepol_8f492a • Status 200 OK</div>
  </header>

  <div class="content">
    <div class="panel-meta">
      <div class="meta-title">Metadados da Sessão Auditada</div>
      <div class="field">
        <div class="f-label">Prompt do Usuário</div>
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
        <span style="font-size:13px; color:#94a3b8;">100% de cobertura no Langfuse</span>
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
        <div class="bar-bg"><div class="bar-fill b3">Raciocínio CoT do Modelo (342 Tokens) — MAIS CUSTOSO EM TEMPO</div></div>
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

    # Scene 10: Token Analytics & Cost Breakdown (What was most expensive?)
    ("cheri_s10.html", """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  body { background: #0b0f19; color: #f1f5f9; width: 1920px; height: 1080px; overflow: hidden; display: flex; flex-direction: column; }
  header { height: 64px; background: #111827; border-bottom: 1px solid #1f2937; display: flex; align-items: center; justify-content: space-between; padding: 0 40px; }
  .brand { display: flex; align-items: center; gap: 14px; font-size: 18px; font-weight: 700; }
  .brand svg { width: 28px; height: 28px; fill: #38bdf8; }

  .content { flex: 1; padding: 36px 48px; display: flex; flex-direction: column; gap: 24px; }
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

  .cost-summary { background: #0f172a; border: 1px solid #0284c7; border-radius: 10px; padding: 18px; font-size: 14px; color: #cbd5e1; }
</style>
</head>
<body>
  <header>
    <div class="brand">
      <svg viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
      <span>Langfuse Token Intelligence: O que foi Mais Custoso na Consulta?</span>
    </div>
    <span style="color:#38bdf8; font-family:monospace; font-size:13px;">Modelo: deepseek-r1:1.5b • Total: 342 Tokens</span>
  </header>

  <div class="content">
    <div class="title-bar">
      <h2>Auditoria e Análise de Custos de Tokens</h2>
      <p>Transparência total sobre onde cada token foi consumido e onde o tempo de processamento foi concentrado.</p>
    </div>

    <div class="cards-grid">
      <div class="t-card" style="border-top: 4px solid #38bdf8;">
        <div class="t-head"><span>Prompt Context (MAIS CUSTOSO EM TOKENS)</span><span>📥 63.7%</span></div>
        <div class="t-num" style="color: #38bdf8;">218 Tokens</div>
        <div class="t-desc">Esquema das 7 tabelas e regras YAML de crédito corporativo para blindagem semântica.</div>
      </div>

      <div class="t-card" style="border-top: 4px solid #a78bfa;">
        <div class="t-head"><span>Reasoning CoT (MAIS CUSTOSO EM TEMPO)</span><span>🧠 21.0%</span></div>
        <div class="t-num" style="color: #a78bfa;">72 Tokens</div>
        <div class="t-desc">Cadeia de pensamento no bloco <code>&lt;think&gt;</code> validando integridade referencial (776ms).</div>
      </div>

      <div class="t-card" style="border-top: 4px solid #34d399;">
        <div class="t-head"><span>Completion SQL Output</span><span>📤 15.3%</span></div>
        <div class="t-num" style="color: #34d399;">52 Tokens</div>
        <div class="t-desc">Código SQL ANSI canônico ultracompacto entregue para execução no DuckDB.</div>
      </div>
    </div>

    <div class="breakdown-box">
      <div class="box-title">Alocação de Tokens por Consulta (342 Tokens Totais)</div>
      
      <div class="big-bar">
        <div class="seg1">Input Ontológico (63.7% - 218 Tokens)</div>
        <div class="seg2">Raciocínio CoT (21.0% - 72 Tokens)</div>
        <div class="seg3">SQL Output (15.3% - 52 Tokens)</div>
      </div>

      <div class="cost-summary">
        <b>💡 Conclusão de Eficiência:</b> O maior volume de tokens está no <b>Contexto Ontológico de Entrada (63.7%)</b>, que é reutilizado via cache para baratear chamadas. Já a maior parcela de tempo de execução (52% / 776ms) ocorre no <b>Raciocínio CoT</b> do DeepSeek-R1, garantindo zero alucinações de schema.
      </div>
    </div>
  </div>
</body>
</html>
"""),
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

# 3. Durations for each of the 10 scenes (Total: 60s matching soundtrack_cheri_cheri_lady_60s.wav):
# S1: GitHub Repo Top (6s)
# S2: GitHub Repo Scrolling (6s)
# S3: Terminal Git Clone (6s)
# S4: Terminal Make Seed & Containers (6s)
# S5: Chat UI Welcome (6s)
# S6: Chat UI Asking Question (5s)
# S7: Chat UI Response & DuckDB (7s)
# S8: Chat UI Mermaid ERD (6s)
# S9: Langfuse Tracing Spans Waterfall (6s)
# S10: Token Analytics & Cost Breakdown (6s)
# Sum = 6 + 6 + 6 + 6 + 6 + 5 + 7 + 6 + 6 + 6 = 60s

clip_durations = [
    ("cheri_s1.png", 6),
    ("cheri_s2.png", 6),
    ("cheri_s3.png", 6),
    ("cheri_s4.png", 6),
    ("cheri_s5.png", 6),
    ("cheri_s6.png", 5),
    ("cheri_s7.png", 7),
    ("cheri_s8.png", 6),
    ("cheri_s9.png", 6),
    ("cheri_s10.png", 6)
]

clip_files = []
for i, (png_name, dur) in enumerate(clip_durations):
    clip_path = os.path.join(OUTPUT_DIR, f"cheri_clip_{i}.mp4")
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

concat_path = os.path.join(OUTPUT_DIR, "concat_cheri.txt")
with open(concat_path, "w") as f:
    for c in clip_files:
        f.write(f"file '{os.path.abspath(c)}'\n")

final_output = os.path.join(OUTPUT_DIR, "icepol_user_journey_cheri_cheri_lady.mp4")
audio_path = os.path.join(OUTPUT_DIR, "soundtrack_cheri_cheri_lady_60s.wav")

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
print(f"Generated Cheri Cheri Lady User Journey Video: {final_output}")
