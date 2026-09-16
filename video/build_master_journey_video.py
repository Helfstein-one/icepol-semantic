import os
import subprocess

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUTPUT_DIR = "video"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 9 Scenes representing the complete user journey:
# S1: User accessing GitHub repo (Helfstein-one/icepol-semantic)
# S2: Terminal - git clone, cd, make seed, podman compose up -d
# S3: Icepol Web UI Launch (localhost:8000) - Polar bear logo, model selector, upload, mic
# S4: Semantic Query Execution (User asks for corporate credit exposure & leverage)
# S5: Chat Return with Dynamic Mermaid Diagram (ERD with Crow's foot) + DuckDB table
# S6: Transition Scene to Langfuse Observability (:3001)
# S7: Langfuse Trace Deep-Dive & Spans Waterfall
# S8: Token Economics & Spending Analysis (Prompt vs Completion vs Thought tokens)
# S9: Master Journey Recap & Enterprise Production Stack

scenes = [
    # Scene 1: GitHub Repository Browsing
    ("master_s1.html", """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }
  body { background: #0d1117; color: #c9d1d9; width: 1920px; height: 1080px; overflow: hidden; display: flex; flex-direction: column; }
  
  /* GitHub Top Nav */
  header { height: 68px; background: #161b22; border-bottom: 1px solid #30363d; display: flex; align-items: center; justify-content: space-between; padding: 0 40px; }
  .nav-left { display: flex; align-items: center; gap: 16px; }
  .github-logo { fill: #ffffff; width: 34px; height: 34px; }
  .repo-path { font-size: 20px; font-weight: 600; color: #58a6ff; }
  .repo-path a { color: #58a6ff; text-decoration: none; }
  .repo-path span { color: #8b949e; margin: 0 4px; }
  .badge-public { border: 1px solid #30363d; border-radius: 20px; padding: 3px 10px; font-size: 12px; color: #8b949e; font-weight: 500; }

  .nav-right { display: flex; gap: 12px; }
  .btn-gh { background: #21262d; border: 1px solid #30363d; color: #c9d1d9; padding: 6px 14px; border-radius: 6px; font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 6px; }
  .btn-primary { background: #238636; border-color: #2ea043; color: #ffffff; }

  /* GitHub Body */
  .main-content { flex: 1; padding: 32px 50px; display: grid; grid-template-columns: 1fr 340px; gap: 32px; }
  
  .repo-header { margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }
  .repo-desc { font-size: 16px; color: #8b949e; line-height: 1.5; }
  .tags-row { display: flex; gap: 8px; margin-top: 10px; }
  .tag { background: #1f242c; color: #58a6ff; font-size: 12px; padding: 3px 10px; border-radius: 12px; }

  .file-box { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; overflow: hidden; margin-top: 16px; }
  .file-header { background: #161b22; padding: 14px 20px; border-bottom: 1px solid #30363d; display: flex; justify-content: space-between; align-items: center; font-size: 13px; }
  .file-row { display: flex; justify-content: space-between; padding: 12px 20px; border-bottom: 1px solid #21262d; font-size: 14px; }
  .file-row:hover { background: #161b22; }
  .file-name { color: #c9d1d9; font-weight: 500; display: flex; align-items: center; gap: 10px; }
  .file-msg { color: #8b949e; font-size: 13px; }
  .file-time { color: #6e7681; font-size: 13px; }

  /* Clone Modal Mockup */
  .clone-popover {
    position: absolute; right: 410px; top: 120px; width: 440px; background: #161b22; border: 1px solid #30363d;
    border-radius: 8px; padding: 18px; box-shadow: 0 16px 36px rgba(0,0,0,0.6); z-index: 10;
  }
  .clone-title { font-size: 14px; font-weight: 700; color: #ffffff; margin-bottom: 10px; }
  .clone-bar { background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 10px; display: flex; justify-content: space-between; align-items: center; }
  .clone-url { font-family: monospace; font-size: 13px; color: #58a6ff; }
  
  /* Sidebar */
  .sidebar { display: flex; flex-direction: column; gap: 20px; }
  .side-card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; }
  .side-title { font-size: 14px; font-weight: 600; color: #ffffff; margin-bottom: 12px; }
  .stack-pill { display: inline-block; background: #21262d; border: 1px solid #30363d; color: #8b949e; padding: 4px 10px; border-radius: 6px; font-size: 12px; margin: 3px; }
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
      <button class="btn-gh">⭐ Star (42)</button>
      <button class="btn-gh">🍴 Fork (12)</button>
      <button class="btn-gh btn-primary">&lt;&gt; Code ▾</button>
    </div>
  </header>

  <div class="main-content">
    <div>
      <div class="repo-header">
        <div>
          <div class="repo-desc">Ecossistema 100% Local de Inteligência Analítica em Crédito Corporativo impulsionado por Camada Semântica, Apache Iceberg, DuckDB, Ollama e Observabilidade com Langfuse.</div>
          <div class="tags-row">
            <span class="tag">semantic-layer</span>
            <span class="tag">apache-iceberg</span>
            <span class="tag">duckdb</span>
            <span class="tag">langfuse</span>
            <span class="tag">deepseek-r1</span>
            <span class="tag">mysql</span>
          </div>
        </div>
      </div>

      <div class="file-box">
        <div class="file-header">
          <span><b>main</b> • 26 commits • Último commit: <i>feat: complete observability pipeline & UI journey</i></span>
          <span style="color:#58a6ff;">Commit 106854c</span>
        </div>
        <div class="file-row">
          <div class="file-name">📁 core/</div>
          <div class="file-msg">FastAPI middleware agent, Langfuse tracer & MySQL logger</div>
          <div class="file-time">hoje</div>
        </div>
        <div class="file-row">
          <div class="file-name">📁 semantic/</div>
          <div class="file-msg">Ontologias YAML & Compilador AST de Crédito Corporativo</div>
          <div class="file-time">hoje</div>
        </div>
        <div class="file-row">
          <div class="file-name">📁 video/</div>
          <div class="file-msg">Vídeos da jornada completa e observabilidade Langfuse</div>
          <div class="file-time">hoje</div>
        </div>
        <div class="file-row">
          <div class="file-name">📄 docker-compose.yml</div>
          <div class="file-msg">Pilha com MinIO, Polaris, MySQL 8, Postgres e Langfuse</div>
          <div class="file-time">hoje</div>
        </div>
        <div class="file-row">
          <div class="file-name">📄 README.md</div>
          <div class="file-msg">Documentação técnica, arquitetura, Mermaid e consoles</div>
          <div class="file-time">hoje</div>
        </div>
      </div>
    </div>

    <!-- Sidebar -->
    <div class="sidebar">
      <div class="side-card">
        <div class="side-title">About</div>
        <p style="font-size:13px; color:#8b949e; line-height:1.4; margin-bottom:12px;">Data Lakehouse com Camada Semântica para Wholesale Banking e IA de auditoria contínua.</p>
        <span class="stack-pill">Python 3.11</span>
        <span class="stack-pill">DuckDB</span>
        <span class="stack-pill">Apache Polaris</span>
        <span class="stack-pill">MinIO S3</span>
        <span class="stack-pill">Langfuse v2</span>
        <span class="stack-pill">MySQL 8.0</span>
      </div>
      <div class="side-card">
        <div class="side-title">Releases</div>
        <p style="font-size:13px; color:#58a6ff; font-weight:600;">v1.2.0 • Latest</p>
        <p style="font-size:12px; color:#8b949e; margin-top:4px;">Suporte a DeepSeek-R1, Langfuse Tracing e Crow's foot ERD.</p>
      </div>
    </div>
  </div>

  <!-- Clone Popover -->
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

    # Scene 2: Terminal - Git Clone, Setup & Podman Compose Up
    ("master_s2.html", """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Fira Code', 'Menlo', 'Monaco', monospace; }
  body { background: #080c14; color: #38bdf8; width: 1920px; height: 1080px; overflow: hidden; display: flex; flex-direction: column; padding: 36px 48px; }
  
  .terminal-window {
    flex: 1; background: #0f172a; border: 1px solid #1e293b; border-radius: 16px;
    box-shadow: 0 25px 60px rgba(0,0,0,0.8); display: flex; flex-direction: column; overflow: hidden;
  }
  .title-bar {
    height: 48px; background: #1e293b; display: flex; align-items: center; justify-content: space-between; padding: 0 20px;
    border-bottom: 1px solid #334155;
  }
  .traffic-lights { display: flex; gap: 8px; }
  .circle { width: 12px; height: 12px; border-radius: 50%; }
  .red { background: #ef4444; } .yellow { background: #f59e0b; } .green { background: #10b981; }
  .term-title { font-size: 13px; color: #94a3b8; font-weight: 600; }

  .term-body { flex: 1; padding: 28px 36px; font-size: 15px; line-height: 1.6; color: #e2e8f0; overflow: hidden; }
  .prompt { color: #10b981; font-weight: bold; }
  .cmd { color: #f8fafc; font-weight: 600; }
  .success { color: #34d399; }
  .info { color: #60a5fa; }
  .highlight { color: #fbbf24; }
  .dim { color: #64748b; }
</style>
</head>
<body>
  <div class="terminal-window">
    <div class="title-bar">
      <div class="traffic-lights">
        <div class="circle red"></div>
        <div class="circle yellow"></div>
        <div class="circle green"></div>
      </div>
      <div class="term-title">mauriciohelfstein@macbook-air: ~/dev/icepol-semantic (zsh)</div>
      <div style="font-size: 12px; color: #64748b;">1920x1080 Session</div>
    </div>

    <div class="term-body">
      <p><span class="prompt">➜  dev</span> <span class="cmd">git clone https://github.com/Helfstein-one/icepol-semantic.git</span></p>
      <p class="dim">Cloning into 'icepol-semantic'...</p>
      <p class="dim">remote: Enumerating objects: 382, done.</p>
      <p class="dim">remote: Total 382 (delta 214), reused 364 (delta 198), pack-reused 0</p>
      <p class="success">Receiving objects: 100% (382/382), 14.82 MiB | 22.40 MiB/s, done.</p>
      <br>
      <p><span class="prompt">➜  dev</span> <span class="cmd">cd icepol-semantic && make seed</span></p>
      <p class="info">🌱 [SEED] Gerando 7 tabelas físicas sintéticas de Crédito Corporativo em Parquet...</p>
      <p class="dim">  ✔ counterparts.parquet (1,000 registros, CNAE, Ratings, Grupos Econômicos)</p>
      <p class="dim">  ✔ facilities.parquet (3,500 operações de crédito, rotativo, capital de giro)</p>
      <p class="dim">  ✔ collaterals.parquet (4,200 garantias reais, hipotecas, recebíveis)</p>
      <p class="dim">  ✔ proposals.parquet (2,800 comitês de risco e aprovações)</p>
      <p class="dim">  ✔ financial_statements.parquet (Dívida Líquida, EBITDA, Balanços auditados)</p>
      <p class="dim">  ✔ credit_limits.parquet (Limites globais aprovados e tomados)</p>
      <p class="dim">  ✔ covenants.parquet (Cláusulas de desenquadramento e indicadores)</p>
      <p class="success">✨ 7 Tabelas registradas no Apache Polaris REST Catalog e MinIO S3!</p>
      <br>
      <p><span class="prompt">➜  icepol-semantic</span> <span class="cmd">podman compose up -d</span></p>
      <p class="dim">Starting containers in background...</p>
      <p><span class="success">✔ Container minio-storage</span>    <span class="highlight">Running</span> (S3 API :9000, Console :9001)</p>
      <p><span class="success">✔ Container polaris-catalog</span>  <span class="highlight">Running</span> (Apache Iceberg REST :8181)</p>
      <p><span class="success">✔ Container mysql-db</span>         <span class="highlight">Running</span> (Metrics & Audit Database :3306)</p>
      <p><span class="success">✔ Container postgres-langfuse</span><span class="highlight">Running</span> (Metadata Storage :5432)</p>
      <p><span class="success">✔ Container langfuse-server</span>  <span class="highlight">Running</span> (LLM Observability Dashboard :3001)</p>
      <p><span class="success">✔ Container semantic-agent</span>   <span class="highlight">Running</span> (FastAPI + DuckDB Engine :8000)</p>
      <br>
      <p><span class="prompt">➜  icepol-semantic</span> <span class="cmd">open http://localhost:8000</span></p>
      <p class="info">🚀 Abrindo o Icepol Semantic Layer no navegador padrão...</p>
    </div>
  </div>
</body>
</html>
"""),

    # Scene 3: Icepol Web UI Launch - Clean UI with logo, greeting, selectors
    ("master_s3.html", """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  body { background: #080c14; color: #f1f5f9; width: 1920px; height: 1080px; overflow: hidden; display: flex; flex-direction: column; }
  
  header {
    height: 70px; background: #0d1322; border-bottom: 1px solid #1e293b;
    display: flex; align-items: center; justify-content: space-between; padding: 0 40px;
  }
  .brand { display: flex; align-items: center; gap: 14px; }
  .polar-bear-logo { width: 36px; height: 36px; fill: #38bdf8; filter: drop-shadow(0 0 10px rgba(56, 189, 248, 0.4)); }
  .brand h1 { font-size: 22px; font-weight: 800; letter-spacing: -0.5px; }
  
  .header-badges { display: flex; align-items: center; gap: 14px; }
  .badge { background: #111827; border: 1px solid #1e293b; padding: 6px 14px; border-radius: 9999px; font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 8px; }
  .badge-pulse { width: 8px; height: 8px; border-radius: 50%; background: #10b981; box-shadow: 0 0 8px #10b981; }

  /* Hero Center */
  .hero-container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 0 60px; }
  .greeting-title { font-size: 44px; font-weight: 800; color: #ffffff; letter-spacing: -1px; margin-bottom: 12px; }
  .greeting-subtitle { font-size: 20px; color: #94a3b8; margin-bottom: 44px; }

  /* Suggestions */
  .chips-row { display: flex; gap: 16px; margin-bottom: 50px; }
  .chip {
    background: #0f172a; border: 1px solid #1e293b; padding: 14px 22px; border-radius: 12px;
    font-size: 14px; color: #e2e8f0; font-weight: 500; cursor: pointer; transition: all 0.2s ease;
    box-shadow: 0 4px 14px rgba(0,0,0,0.2);
  }
  .chip-active { border-color: #0284c7; background: #0369a115; color: #38bdf8; }

  /* Prompt Pill */
  .prompt-wrapper { width: 100%; max-width: 900px; position: relative; }
  .prompt-pill {
    background: #0f172a; border: 2px solid #0284c7; border-radius: 28px; padding: 16px 24px;
    display: flex; align-items: center; justify-content: space-between; box-shadow: 0 10px 40px rgba(2, 132, 199, 0.25);
  }
  .pill-left { display: flex; align-items: center; gap: 16px; flex: 1; }
  .btn-circle { width: 38px; height: 38px; border-radius: 50%; background: #1e293b; border: 1px solid #334155; display: flex; align-items: center; justify-content: center; color: #94a3b8; font-size: 18px; font-weight: bold; }
  .model-select { background: #1e293b; border: 1px solid #38bdf8; color: #38bdf8; padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 700; display: flex; align-items: center; gap: 6px; }
  .input-text { font-size: 16px; color: #f8fafc; font-weight: 500; }
  .pill-right { display: flex; align-items: center; gap: 12px; }
  .btn-mic { width: 40px; height: 40px; border-radius: 50%; background: #1e293b; color: #38bdf8; border: 1px solid #334155; display: flex; align-items: center; justify-content: center; }
  .btn-send { width: 40px; height: 40px; border-radius: 50%; background: #0284c7; color: #ffffff; border: none; display: flex; align-items: center; justify-content: center; font-weight: bold; }
</style>
</head>
<body>
  <header>
    <div class="brand">
      <svg class="polar-bear-logo" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12c0 5.52 4.48 10 10 10s10-4.48 10-10C22 6.48 17.52 2 12 2zm1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
      <h1>Icepol Semantic Layer</h1>
      <span style="font-size: 11px; background:#0284c7; color:#fff; padding:3px 8px; border-radius:6px; font-weight:bold;">v1.2.0</span>
    </div>

    <div class="header-badges">
      <div class="badge"><div class="badge-pulse"></div><span>DuckDB: Ativo (7 Tabelas)</span></div>
      <div class="badge"><span style="color:#c084fc;">Ollama: deepseek-r1:1.5b</span></div>
      <div class="badge" style="border-color:#38bdf8;"><span style="color:#38bdf8;">📊 Métricas & Traces (Langfuse: OK)</span></div>
    </div>
  </header>

  <div class="hero-container">
    <div class="greeting-title">Como posso ajudar com sua pesquisa hoje?</div>
    <div class="greeting-subtitle">Explore 7 tabelas relacionais de crédito corporativo, analise balanços e audite queries com IA local.</div>

    <div class="chips-row">
      <div class="chip chip-active">📈 Exposição total por setor e alavancagem média</div>
      <div class="chip">🏢 Limite de crédito aprovado por grupo econômico</div>
      <div class="chip">⚠️ Taxa de desenquadramento de covenants</div>
      <div class="chip">📐 Diagrama Conceitual Mermaid (7 Entidades)</div>
    </div>

    <div class="prompt-wrapper">
      <div class="prompt-pill">
        <div class="pill-left">
          <div class="btn-circle">+</div>
          <div class="model-select">
            <span>deepseek-r1:1.5b</span>
            <span style="font-size:10px;">▾</span>
          </div>
          <div class="input-text">Qual a exposição total e alavancagem média por setor? Gere também o diagrama conceitual Mermaid.</div>
        </div>
        <div class="pill-right">
          <div class="btn-mic">🎙️</div>
          <div class="btn-send">➔</div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""),

    # Scene 4: Semantic Query Compilation & Execution Pipeline
    ("master_s4.html", """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  body { background: #080c14; color: #f1f5f9; width: 1920px; height: 1080px; overflow: hidden; display: flex; flex-direction: column; }
  header { height: 70px; background: #0d1322; border-bottom: 1px solid #1e293b; display: flex; align-items: center; justify-content: space-between; padding: 0 40px; }
  .brand { display: flex; align-items: center; gap: 14px; }
  .brand h1 { font-size: 22px; font-weight: 800; }

  .content { flex: 1; padding: 36px 60px; display: flex; flex-direction: column; gap: 24px; }
  .card-pipeline { background: #0f172a; border: 1px solid #1e293b; border-radius: 16px; padding: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
  .pipeline-steps { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-top: 20px; }
  .step-box { background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 18px; }
  .step-num { font-size: 11px; font-weight: 700; text-transform: uppercase; color: #38bdf8; margin-bottom: 6px; }
  .step-title { font-size: 16px; font-weight: 700; color: #ffffff; margin-bottom: 8px; }
  .step-desc { font-size: 13px; color: #94a3b8; line-height: 1.4; }

  /* SQL Block */
  .code-container { background: #090d16; border: 1px solid #1e293b; border-radius: 12px; padding: 20px; margin-top: 10px; font-family: monospace; font-size: 14px; line-height: 1.6; }
  .kw { color: #f472b6; font-weight: bold; }
  .fn { color: #60a5fa; }
  .str { color: #a5f3fc; }
  .cm { color: #64748b; }
</style>
</head>
<body>
  <header>
    <div class="brand">
      <h1>Icepol Semantic Compilation Engine</h1>
      <span style="font-size: 12px; color: #94a3b8; margin-left: 12px;">Domain: <b>corporate_credit</b> • Model: <b>deepseek-r1:1.5b</b></span>
    </div>
    <div style="font-size: 13px; color: #10b981; font-weight: bold;">⚡ DuckDB Columnar Vectorized Execution</div>
  </header>

  <div class="content">
    <div class="card-pipeline">
      <h2 style="font-size: 22px; font-weight: 800; color: #ffffff;">Pipeline de Resolução Semântica (Zero Alucinação)</h2>
      <div class="pipeline-steps">
        <div class="step-box" style="border-color:#0284c7;">
          <div class="step-num">Passo 1</div>
          <div class="step-title">Token Match Ontológico</div>
          <div class="step-desc">Identifica métricas: <code>total_exposure</code>, <code>avg_net_debt_ebitda</code> e dimensão: <code>ds_cnae_sector</code>.</div>
        </div>
        <div class="step-box" style="border-color:#8b5cf6;">
          <div class="step-num">Passo 2</div>
          <div class="step-title">DeepSeek-R1 CoT</div>
          <div class="step-desc">Mapeia joins de chaves estrangeiras entre <code>counterparts</code>, <code>facilities</code> e <code>financial_statements</code>.</div>
        </div>
        <div class="step-box" style="border-color:#10b981;">
          <div class="step-num">Passo 3</div>
          <div class="step-title">DuckDB In-Memory</div>
          <div class="step-desc">Executa agregação com <code>NULLIF</code> em 180ms sobre partições Parquet do Apache Iceberg.</div>
        </div>
        <div class="step-box" style="border-color:#f59e0b;">
          <div class="step-num">Passo 4</div>
          <div class="step-title">Telemetry & Sinks</div>
          <div class="step-desc">Envia spans assíncronos ao Langfuse (:3001) e insere auditoria na tabela MySQL (:3306).</div>
        </div>
      </div>
    </div>

    <div class="card-pipeline" style="flex:1;">
      <h3 style="font-size: 16px; font-weight: 700; color: #38bdf8; margin-bottom: 10px;">SQL Canônico Compilado Deterministicamente:</h3>
      <div class="code-container">
        <span class="cm">-- Executado no DuckDB em 0.18s com partições Iceberg via MinIO S3</span><br>
        <span class="kw">SELECT</span><br>
        &nbsp;&nbsp;c.ds_cnae_sector <span class="kw">AS</span> setor,<br>
        &nbsp;&nbsp;<span class="fn">SUM</span>(f.vl_credit_limit) <span class="kw">AS</span> total_exposicao,<br>
        &nbsp;&nbsp;<span class="fn">ROUND</span>(<span class="fn">AVG</span>(fs.vl_net_debt / <span class="fn">NULLIF</span>(fs.vl_ebitda, 0)), 2) <span class="kw">AS</span> alavancagem_media<br>
        <span class="kw">FROM</span> corporate_credit.counterparts c<br>
        <span class="kw">JOIN</span> corporate_credit.facilities f <span class="kw">ON</span> c.counterpart_id = f.counterpart_id<br>
        <span class="kw">LEFT JOIN</span> corporate_credit.financial_statements fs <span class="kw">ON</span> c.counterpart_id = fs.counterpart_id<br>
        <span class="kw">GROUP BY</span> 1<br>
        <span class="kw">ORDER BY</span> total_exposicao <span class="kw">DESC</span>;
      </div>
    </div>
  </div>
</body>
</html>
"""),

    # Scene 5: Chat Return with Dynamic Mermaid Diagram (Crow's Foot) & DuckDB Table
    ("master_s5.html", """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  body { background: #080c14; color: #f1f5f9; width: 1920px; height: 1080px; overflow: hidden; display: flex; flex-direction: column; }
  header { height: 64px; background: #0d1322; border-bottom: 1px solid #1e293b; display: flex; align-items: center; justify-content: space-between; padding: 0 40px; }
  .brand { display: flex; align-items: center; gap: 14px; font-size: 18px; font-weight: 700; }

  .content { flex: 1; padding: 24px 40px; display: grid; grid-template-columns: 520px 1fr; gap: 24px; }
  .panel-left { display: flex; flex-direction: column; gap: 20px; }

  /* Data Table */
  .table-box { background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 18px; display: flex; flex-direction: column; }
  .table-title { font-size: 15px; font-weight: 700; color: #38bdf8; margin-bottom: 12px; display: flex; justify-content: space-between; }
  table { width: 100%; border-collapse: collapse; font-size: 13px; text-align: left; }
  th { background: #1e293b; padding: 10px; color: #94a3b8; font-weight: 600; border-bottom: 1px solid #334155; }
  td { padding: 10px; border-bottom: 1px solid #1e293b; color: #e2e8f0; }
  
  /* Mermaid Diagram Area */
  .mermaid-box {
    background: #0f172a; border: 1px solid #1e293b; border-radius: 14px; padding: 20px;
    display: flex; flex-direction: column; box-shadow: 0 10px 30px rgba(0,0,0,0.4);
  }
  .box-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e293b; padding-bottom: 12px; margin-bottom: 14px; }
  .box-header h3 { font-size: 17px; font-weight: 700; color: #ffffff; display: flex; align-items: center; gap: 8px; }
  
  /* Visual ERD Canvas Mockup */
  .erd-canvas {
    flex: 1; background: #090d16; border: 1px dashed #334155; border-radius: 10px;
    position: relative; display: flex; flex-wrap: wrap; gap: 24px; padding: 24px; align-content: flex-start;
  }
  .entity-card {
    background: #1e293b; border: 1px solid #38bdf8; border-radius: 8px; width: 200px;
    overflow: hidden; box-shadow: 0 4px 14px rgba(0,0,0,0.5);
  }
  .entity-head { background: #0284c7; color: #ffffff; padding: 6px 10px; font-size: 13px; font-weight: 700; text-align: center; }
  .entity-cols { padding: 8px 10px; font-size: 11px; font-family: monospace; color: #cbd5e1; line-height: 1.5; }
  .pk { color: #f472b6; font-weight: bold; }
  .fk { color: #38bdf8; font-weight: bold; }
  
  .crows-foot-tag {
    position: absolute; bottom: 16px; right: 20px; background: #064e3b; color: #34d399;
    border: 1px solid #059669; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 700;
  }
</style>
</head>
<body>
  <header>
    <div class="brand">
      <span>Icepol Chat Response Cell • Modelo: <b>deepseek-r1:1.5b</b></span>
    </div>
    <div style="font-size: 12px; color: #94a3b8;">
      ⚡ Tempo total: <b style="color:#10b981;">1.49s</b> (LLM: 776ms • DuckDB: 180ms • MySQL Log: 108ms)
    </div>
  </header>

  <div class="content">
    <div class="panel-left">
      <div class="table-box">
        <div class="table-title">
          <span>📊 Resultado Analítico (DuckDB)</span>
          <span style="font-size: 11px; color:#10b981;">100% Validado</span>
        </div>
        <table>
          <thead>
            <tr>
              <th>Setor (CNAE)</th>
              <th>Exposição Total</th>
              <th>Alavancagem Média</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Indústria & Manufatura</td>
              <td style="color:#38bdf8; font-weight:600;">R$ 4.820.000.000</td>
              <td>2.1x EBITDA</td>
            </tr>
            <tr>
              <td>Agronegócio & Grãos</td>
              <td style="color:#38bdf8; font-weight:600;">R$ 3.650.000.000</td>
              <td>1.8x EBITDA</td>
            </tr>
            <tr>
              <td>Varejo & Consumo</td>
              <td style="color:#38bdf8; font-weight:600;">R$ 2.410.000.000</td>
              <td>3.4x EBITDA</td>
            </tr>
            <tr>
              <td>Energia & Infraestrutura</td>
              <td style="color:#38bdf8; font-weight:600;">R$ 1.950.000.000</td>
              <td>1.4x EBITDA</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="table-box" style="flex:1;">
        <div class="table-title"><span>📝 Resumo Executivo</span></div>
        <p style="font-size:13px; color:#cbd5e1; line-height:1.5;">
          A maior exposição corporativa concentra-se na <b>Indústria & Manufatura</b> (R$ 4.82B), com alavancagem equilibrada de 2.1x. O setor de Varejo apresenta alavancagem mais alta (3.4x EBITDA), sugerindo monitoramento estreito dos covenants contratuais.
        </p>
      </div>
    </div>

    <!-- Right: Visual Mermaid Model -->
    <div class="mermaid-box">
      <div class="box-header">
        <h3>📐 Diagrama Conceitual Mermaid (7 Entidades Relacionadas)</h3>
        <span style="font-size: 12px; color: #38bdf8; font-weight: 600;">Renderer: Mermaid v10.9.8 (Crow's Foot Ativo)</span>
      </div>

      <div class="erd-canvas">
        <div class="entity-card">
          <div class="entity-head">COUNTERPARTS</div>
          <div class="entity-cols">
            <span class="pk">PK</span> counterpart_id<br>
            string nm_counterpart<br>
            string ds_cnae_sector<br>
            string cd_rating
          </div>
        </div>

        <div class="entity-card">
          <div class="entity-head">FACILITIES</div>
          <div class="entity-cols">
            <span class="pk">PK</span> facility_id<br>
            <span class="fk">FK</span> counterpart_id<br>
            string tp_operation<br>
            double vl_credit_limit
          </div>
        </div>

        <div class="entity-card">
          <div class="entity-head">COLLATERALS</div>
          <div class="entity-cols">
            <span class="pk">PK</span> collateral_id<br>
            <span class="fk">FK</span> facility_id<br>
            string tp_collateral<br>
            double appraised_val
          </div>
        </div>

        <div class="entity-card">
          <div class="entity-head">PROPOSALS</div>
          <div class="entity-cols">
            <span class="pk">PK</span> proposal_id<br>
            <span class="fk">FK</span> counterpart_id<br>
            string st_decision<br>
            double vl_requested
          </div>
        </div>

        <div class="entity-card">
          <div class="entity-head">FINANCIAL_STMT</div>
          <div class="entity-cols">
            <span class="pk">PK</span> statement_id<br>
            <span class="fk">FK</span> counterpart_id<br>
            double vl_net_debt<br>
            double vl_ebitda
          </div>
        </div>

        <div class="entity-card">
          <div class="entity-head">CREDIT_LIMITS</div>
          <div class="entity-cols">
            <span class="pk">PK</span> limit_id<br>
            <span class="fk">FK</span> counterpart_id<br>
            double approved_limit<br>
            double used_limit
          </div>
        </div>

        <div class="entity-card">
          <div class="entity-head">COVENANTS</div>
          <div class="entity-cols">
            <span class="pk">PK</span> covenant_id<br>
            <span class="fk">FK</span> facility_id<br>
            string tp_covenant<br>
            string st_compliance
          </div>
        </div>

        <div class="crows-foot-tag">✔ Relacionamentos 1:N com Cardinalidade Crow's Foot</div>
      </div>
    </div>
  </div>
</body>
</html>
"""),

    # Scene 6: Transition to Langfuse Observability
    ("master_s6.html", """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  body {
    background: radial-gradient(circle at center, #111827 0%, #030712 100%);
    color: #f1f5f9; width: 1920px; height: 1080px; overflow: hidden;
    display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;
  }
  .tag-obs { background: #0284c7; color: #ffffff; padding: 8px 24px; border-radius: 9999px; font-size: 14px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 24px; box-shadow: 0 0 30px rgba(2, 132, 199, 0.6); }
  h1 { font-size: 56px; font-weight: 900; letter-spacing: -1px; margin-bottom: 16px; }
  p { font-size: 22px; color: #94a3b8; max-width: 900px; line-height: 1.5; margin-bottom: 50px; }

  .switch-box {
    background: #0f172a; border: 2px solid #38bdf8; border-radius: 18px; padding: 24px 44px;
    display: flex; align-items: center; gap: 30px; box-shadow: 0 20px 50px rgba(0,0,0,0.6);
  }
  .logo-langfuse { width: 48px; height: 48px; fill: #38bdf8; }
  .switch-text { text-align: left; }
  .switch-title { font-size: 22px; font-weight: 800; color: #ffffff; }
  .switch-url { font-size: 16px; color: #38bdf8; font-family: monospace; }
</style>
</head>
<body>
  <div class="tag-obs">Transição de Jornada do Usuário</div>
  <h1>Para Onde Vai Cada Requisição?</h1>
  <p>Conectando a interface do usuário à auditoria profunda: conheça o cockpit de governança, métricas de tokens e tracing distribuído.</p>

  <div class="switch-box">
    <svg class="logo-langfuse" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
    <div class="switch-text">
      <div class="switch-title">Navegando para o Langfuse Observability Dashboard</div>
      <div class="switch-url">http://localhost:3001 • Projeto: icepol-semantic</div>
    </div>
  </div>
</body>
</html>
"""),

    # Scene 7: Langfuse Trace Deep-Dive & Spans Waterfall
    ("master_s7.html", """<!DOCTYPE html>
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
      <span>Langfuse Trace Details • ID: <b style="color:#38bdf8;">tr_icepol_8f492a</b></span>
    </div>
    <div style="font-size:13px; color:#10b981; font-weight:600;">Status: 200 OK • Zero Hallucinations</div>
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
        <div class="f-label">Camada Física</div>
        <div class="f-val">Apache Iceberg REST + MinIO Parquet</div>
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
        <h2>Waterfall de Spans (Decomposição de Latência)</h2>
        <span style="font-size:13px; color:#94a3b8;">100% de cobertura de observabilidade</span>
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

    # Scene 8: Token Economics & Spending Breakdown (Where tokens are spent!)
    ("master_s8.html", """<!DOCTYPE html>
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

  /* Grid of 3 token cards */
  .cards-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
  .t-card {
    background: #111827; border: 1px solid #1e293b; border-radius: 14px; padding: 24px;
    display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 6px 20px rgba(0,0,0,0.3);
  }
  .t-head { font-size: 14px; font-weight: 600; color: #94a3b8; display: flex; justify-content: space-between; }
  .t-num { font-size: 42px; font-weight: 900; margin: 12px 0; }
  .t-desc { font-size: 13px; color: #64748b; line-height: 1.4; }

  /* Token distribution breakdown bar */
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
      <span>Langfuse Token Intelligence • Análise de Gastos de Tokens</span>
    </div>
    <span style="color:#38bdf8; font-family:monospace; font-size:13px;">Modelo Analisado: deepseek-r1:1.5b</span>
  </header>

  <div class="content">
    <div class="title-bar">
      <h2>Onde o Modelo Está Gastando Tokens?</h2>
      <p>Transparência total sobre o consumo de tokens: contexto de entrada, cadeia de pensamento e síntese SQL final.</p>
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
          <p style="color:#94a3b8; line-height:1.4;">Definições de colunas de <code>counterparts</code>, <code>facilities</code> e métrica <code>avg_net_debt_ebitda</code>. Cacheado para evitar reprocessamento.</p>
        </div>
        <div class="item-box">
          <div class="item-title"><div class="dot" style="background:#a78bfa;"></div><b>2. Raciocínio DeepSeek-R1 (72 tokens)</b></div>
          <p style="color:#94a3b8; line-height:1.4;">O modelo avalia a integridade referencial e Crow's foot antes de emitir a query final, reduzindo erros a zero.</p>
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
"""),

    # Scene 9: Master Journey Recap & Enterprise Production Stack
    ("master_s9.html", """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  body {
    background: radial-gradient(circle at center, #111827 0%, #030712 100%);
    color: #f1f5f9; width: 1920px; height: 1080px; overflow: hidden;
    display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;
  }
  .badge-final {
    background: #0284c7; color: #ffffff; font-size: 14px; font-weight: 700;
    padding: 8px 24px; border-radius: 9999px; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 24px;
    box-shadow: 0 0 30px rgba(2, 132, 199, 0.6);
  }
  h1 { font-size: 54px; font-weight: 900; letter-spacing: -1px; margin-bottom: 16px; }
  p { font-size: 20px; color: #94a3b8; max-width: 1000px; line-height: 1.5; margin-bottom: 48px; }

  .journey-cards { display: flex; gap: 20px; }
  .j-card {
    background: #0f172a; border: 1px solid #1e293b; border-radius: 14px; padding: 20px 24px;
    width: 250px; display: flex; flex-direction: column; align-items: center; gap: 10px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  }
  .j-icon { font-size: 32px; }
  .j-title { font-size: 16px; font-weight: 700; color: #ffffff; }
  .j-sub { font-size: 12px; color: #38bdf8; font-weight: 600; }
  .footer-sub { margin-top: 48px; font-size: 14px; color: #64748b; }
</style>
</head>
<body>
  <div class="badge-final">Jornada Completa do Usuário Concluída</div>
  <h1>Do Clone no GitHub à Governança e Métricas com Langfuse</h1>
  <p>Uma experiência completa e sem atritos: clonagem do repositório, compilação de dados Parquet em DuckDB, inteligência analítica com DeepSeek-R1 e observabilidade corporativa.</p>

  <div class="journey-cards">
    <div class="j-card">
      <div class="j-icon">🐙</div>
      <div class="j-title">GitHub Repo</div>
      <div class="j-sub">git clone & setup</div>
    </div>
    <div class="j-card">
      <div class="j-icon">⚡</div>
      <div class="j-title">Terminal & Docker</div>
      <div class="j-sub">make seed && compose</div>
    </div>
    <div class="j-card">
      <div class="j-icon">🧊</div>
      <div class="j-title">Icepol Semantic UI</div>
      <div class="j-sub">Perguntas em linguagem natural</div>
    </div>
    <div class="j-card">
      <div class="j-icon">📐</div>
      <div class="j-title">Mermaid ERD</div>
      <div class="j-sub">Crow's foot & DuckDB</div>
    </div>
    <div class="j-card">
      <div class="j-icon">📊</div>
      <div class="j-title">Langfuse & MySQL</div>
      <div class="j-sub">Traces & Gastos de Tokens</div>
    </div>
  </div>

  <div class="footer-sub">Helfstein-one / icepol-semantic • Ecossistema 100% Open Source e Auto-Hospedado</div>
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

# 3. Durations for each of the 9 scenes:
# Total = 60 seconds matching soundtrack_80s_60s.wav
# S1: GitHub Access & Clone (7s)
# S2: Terminal Setup & Podman (7s)
# S3: Web UI Launch & Models (6s)
# S4: Semantic Compilation Pipeline (7s)
# S5: Chat Table & Mermaid ERD (7s)
# S6: Transition to Langfuse (5s)
# S7: Langfuse Trace & Waterfall (7s)
# S8: Token Economics & Spending (7s)
# S9: Master Journey Recap (7s)
# Sum = 7 + 7 + 6 + 7 + 7 + 5 + 7 + 7 + 7 = 60s
clip_durations = [
    ("master_s1.png", 7),
    ("master_s2.png", 7),
    ("master_s3.png", 6),
    ("master_s4.png", 7),
    ("master_s5.png", 7),
    ("master_s6.png", 5),
    ("master_s7.png", 7),
    ("master_s8.png", 7),
    ("master_s9.png", 7)
]

clip_files = []
for i, (png_name, dur) in enumerate(clip_durations):
    clip_path = os.path.join(OUTPUT_DIR, f"master_clip_{i}.mp4")
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
concat_path = os.path.join(OUTPUT_DIR, "concat_master.txt")
with open(concat_path, "w") as f:
    for c in clip_files:
        f.write(f"file '{os.path.abspath(c)}'\n")

# 5. Render final master video with 80s soundtrack
final_output = os.path.join(OUTPUT_DIR, "icepol_user_journey_langfuse_tokens.mp4")
audio_path = os.path.join(OUTPUT_DIR, "soundtrack_80s_60s.wav")

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
print(f"Generated Master Video: {final_output}")
