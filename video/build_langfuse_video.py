import os
import subprocess

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUTPUT_DIR = "video"
os.makedirs(OUTPUT_DIR, exist_ok=True)

scenes = [
    ("langfuse_s1.html", """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; }
  body { background: #0b0f19; color: #f1f5f9; width: 1920px; height: 1080px; overflow: hidden; display: flex; flex-direction: column; }
  header { height: 64px; background: #111827; border-bottom: 1px solid #1f2937; display: flex; align-items: center; justify-content: space-between; padding: 0 32px; }
  .brand { display: flex; align-items: center; gap: 14px; }
  .brand svg { width: 30px; height: 30px; fill: #38bdf8; }
  .brand h1 { font-size: 20px; font-weight: 700; color: #f8fafc; letter-spacing: -0.5px; }
  .badge-env { background: #064e3b; color: #34d399; font-size: 11px; padding: 4px 10px; border-radius: 9999px; font-weight: 600; text-transform: uppercase; }
  .project-tag { font-size: 14px; color: #94a3b8; }
  .live-pulse { width: 8px; height: 8px; background: #10b981; border-radius: 50%; box-shadow: 0 0 10px #10b981; }

  .container { flex: 1; padding: 36px 48px; display: flex; flex-direction: column; gap: 28px; }
  .title-bar { display: flex; justify-content: space-between; align-items: flex-end; }
  .title-bar h2 { font-size: 28px; font-weight: 700; color: #ffffff; }
  .title-bar p { color: #64748b; font-size: 15px; margin-top: 4px; }
  .filter-bar { display: flex; gap: 12px; }
  .btn-filter { background: #1e293b; border: 1px solid #334155; color: #e2e8f0; padding: 8px 16px; border-radius: 8px; font-size: 13px; font-weight: 500; }

  .metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }
  .card { background: #111827; border: 1px solid #1e293b; border-radius: 14px; padding: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.25); display: flex; flex-direction: column; justify-content: space-between; }
  .card-header { display: flex; justify-content: space-between; color: #94a3b8; font-size: 14px; font-weight: 500; }
  .card-value { font-size: 34px; font-weight: 800; color: #ffffff; margin: 12px 0 6px; letter-spacing: -0.5px; }
  .card-delta { font-size: 13px; display: flex; align-items: center; gap: 6px; font-weight: 600; }
  .positive { color: #10b981; }
  .highlight-blue { color: #38bdf8; }
  .highlight-purple { color: #c084fc; }
  .highlight-emerald { color: #34d399; }

  .section-box { background: #111827; border: 1px solid #1e293b; border-radius: 14px; flex: 1; padding: 24px; display: flex; flex-direction: column; }
  .section-title { font-size: 18px; font-weight: 700; margin-bottom: 16px; color: #f8fafc; display: flex; align-items: center; justify-content: space-between; }
  table { width: 100%; border-collapse: collapse; text-align: left; font-size: 14px; }
  th { color: #64748b; font-size: 12px; text-transform: uppercase; font-weight: 600; padding: 12px 16px; border-bottom: 1px solid #1e293b; }
  td { padding: 14px 16px; border-bottom: 1px solid #1a2234; color: #cbd5e1; }
  .trace-id { font-family: monospace; color: #38bdf8; font-weight: 600; }
  .status-badge { display: inline-block; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 600; background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
  .model-badge { background: #1e293b; border: 1px solid #334155; padding: 3px 8px; border-radius: 4px; font-size: 12px; color: #93c5fd; }
  .storage-badge { background: #3b0764; color: #d8b4fe; border: 1px solid #6b21a8; padding: 3px 8px; border-radius: 4px; font-size: 12px; }
</style>
</head>
<body>
  <header>
    <div class="brand">
      <svg viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
      <h1>Langfuse LLM Observability & Tracing</h1>
      <span class="badge-env">Production Metastore</span>
    </div>
    <div style="display: flex; align-items: center; gap: 20px;">
      <div style="display: flex; align-items: center; gap: 8px;">
        <div class="live-pulse"></div>
        <span style="font-size: 13px; color: #10b981; font-weight: 600;">Streaming Traces (MinIO & MySQL Connected)</span>
      </div>
      <span class="project-tag">Project: <b>icepol-semantic</b> (v1.2.0)</span>
    </div>
  </header>

  <div class="container">
    <div class="title-bar">
      <div>
        <h2>LLM Execution Analytics & Audit Dashboard</h2>
        <p>Monitor real-time latency, generation token usage, semantic caching, and decision paths for Ollama models.</p>
      </div>
      <div class="filter-bar">
        <button class="btn-filter">Timeframe: Last 24 Hours</button>
        <button class="btn-filter">Filter: deepseek-r1:1.5b</button>
        <button class="btn-filter" style="background:#0284c7; border-color:#0284c7; color:#fff;">+ New Trace Filter</button>
      </div>
    </div>

    <div class="metrics-grid">
      <div class="card">
        <div class="card-header"><span>Total LLM Traces</span><span>⚡ Realtime</span></div>
        <div class="card-value highlight-blue">1,482</div>
        <div class="card-delta positive"><span>↑ 12.4%</span> vs prior session</div>
      </div>
      <div class="card">
        <div class="card-header"><span>Avg Latency (DuckDB + R1)</span><span>⏱ End-to-End</span></div>
        <div class="card-value highlight-purple">1.42s</div>
        <div class="card-delta positive"><span>↓ 380ms</span> cache hit rate 94%</div>
      </div>
      <div class="card">
        <div class="card-header"><span>Total Tokens Processed</span><span>📊 DeepSeek-R1</span></div>
        <div class="card-value highlight-emerald">324.8k</div>
        <div class="card-delta"><span>99.98%</span> valid schema adherence</div>
      </div>
      <div class="card">
        <div class="card-header"><span>Audit Sink Reliability</span><span>💾 MinIO + MySQL 8</span></div>
        <div class="card-value" style="color: #fbbf24;">100%</div>
        <div class="card-delta positive"><span>0</span> dropped metrics / traces</div>
      </div>
    </div>

    <div class="section-box">
      <div class="section-title">
        <span>Recent Agent Traces</span>
        <span style="font-size: 13px; color: #64748b; font-weight: 400;">Showing active executions across local engines</span>
      </div>
      <table>
        <thead>
          <tr>
            <th>Trace ID</th>
            <th>Session / Context</th>
            <th>Model</th>
            <th>Execution Flow</th>
            <th>Sink Backend</th>
            <th>Latency</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="trace-id">tr_icepol_8f492a</td>
            <td>Qual o limite total concedido por setor?</td>
            <td><span class="model-badge">deepseek-r1:1.5b</span></td>
            <td>Semantic Parser &rarr; SQL Synthesizer &rarr; DuckDB</td>
            <td><span class="storage-badge">MinIO S3 + MySQL 8</span></td>
            <td>1.49s</td>
            <td><span class="status-badge">SUCCESS (200)</span></td>
          </tr>
          <tr>
            <td class="trace-id">tr_icepol_7b109e</td>
            <td>Gere o diagrama conceitual completo em Mermaid</td>
            <td><span class="model-badge">llama3.2:3b</span></td>
            <td>Ontology Builder &rarr; Crow's Foot ERD &rarr; SVG</td>
            <td><span class="storage-badge">MinIO S3 + MySQL 8</span></td>
            <td>2.11s</td>
            <td><span class="status-badge">SUCCESS (200)</span></td>
          </tr>
          <tr>
            <td class="trace-id">tr_icepol_61a4f0</td>
            <td>Alavancagem consolidada por grupo econômico</td>
            <td><span class="model-badge">deepseek-r1:1.5b</span></td>
            <td>Iceberg REST &rarr; DuckDB Scan &rarr; Formatter</td>
            <td><span class="storage-badge">MinIO S3 + MySQL 8</span></td>
            <td>0.89s</td>
            <td><span class="status-badge">SUCCESS (200)</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</body>
</html>"""),

    ("langfuse_s2.html", """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; }
  body { background: #0b0f19; color: #f1f5f9; width: 1920px; height: 1080px; overflow: hidden; display: flex; flex-direction: column; }
  header { height: 64px; background: #111827; border-bottom: 1px solid #1f2937; display: flex; align-items: center; justify-content: space-between; padding: 0 32px; }
  .brand { display: flex; align-items: center; gap: 14px; }
  .brand svg { width: 30px; height: 30px; fill: #38bdf8; }
  .brand h1 { font-size: 20px; font-weight: 700; color: #f8fafc; }
  .crumb { font-size: 14px; color: #94a3b8; }

  .content { flex: 1; padding: 32px 48px; display: grid; grid-template-columns: 420px 1fr; gap: 32px; }
  .panel { background: #111827; border: 1px solid #1e293b; border-radius: 14px; padding: 24px; display: flex; flex-direction: column; gap: 20px; }
  .panel-title { font-size: 16px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid #1e293b; padding-bottom: 12px; }
  .meta-item { display: flex; flex-direction: column; gap: 4px; }
  .meta-label { font-size: 12px; color: #64748b; font-weight: 600; text-transform: uppercase; }
  .meta-val { font-size: 14px; color: #f1f5f9; font-weight: 500; font-family: monospace; }

  .waterfall-panel { background: #111827; border: 1px solid #1e293b; border-radius: 14px; padding: 28px; display: flex; flex-direction: column; }
  .wf-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; border-bottom: 1px solid #1e293b; padding-bottom: 16px; }
  .wf-title { font-size: 20px; font-weight: 700; color: #ffffff; }

  .span-item { margin-bottom: 18px; }
  .span-top { display: flex; justify-content: space-between; font-size: 14px; margin-bottom: 6px; font-weight: 600; }
  .span-bar-bg { width: 100%; height: 26px; background: #0f172a; border-radius: 6px; position: relative; overflow: hidden; border: 1px solid #1e293b; }
  .span-bar { height: 100%; border-radius: 5px; position: absolute; display: flex; align-items: center; padding-left: 10px; font-size: 12px; font-weight: 700; color: #ffffff; }
  
  .c1 { background: linear-gradient(90deg, #3b82f6, #60a5fa); left: 0%; width: 100%; }
  .c2 { background: linear-gradient(90deg, #8b5cf6, #a78bfa); left: 5%; width: 22%; }
  .c3 { background: linear-gradient(90deg, #ec4899, #f472b6); left: 28%; width: 52%; }
  .c4 { background: linear-gradient(90deg, #10b981, #34d399); left: 81%; width: 12%; }
  .c5 { background: linear-gradient(90deg, #f59e0b, #fbbf24); left: 93%; width: 7%; }
</style>
</head>
<body>
  <header>
    <div class="brand">
      <svg viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
      <h1>Trace Deep-Dive: <span style="color:#38bdf8;">tr_icepol_8f492a</span></h1>
    </div>
    <div class="crumb">Traces &rarr; icepol_query &rarr; deepseek-r1:1.5b</div>
  </header>

  <div class="content">
    <div class="panel">
      <div class="panel-title">Trace Context & Metadata</div>
      <div class="meta-item">
        <div class="meta-label">User Query Prompt</div>
        <div class="meta-val" style="color:#38bdf8;">"Qual o limite total concedido por setor?"</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Resolved Semantic Intent</div>
        <div class="meta-val">ANALYTICS_AGGREGATION_BY_DIMENSION</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Engine & Model Name</div>
        <div class="meta-val">deepseek-r1:1.5b (Ollama Local)</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Metastore Catalog</div>
        <div class="meta-val">Apache Polaris REST (Iceberg Catalog)</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Execution Engine</div>
        <div class="meta-val">DuckDB v1.1.3 In-Memory Columnar</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Observability Sinks</div>
        <div class="meta-val">MinIO Object Store + MySQL 8.0</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Status & HTTP Return</div>
        <div class="meta-val" style="color:#34d399;">200 OK - Zero Hallucinations</div>
      </div>
    </div>

    <div class="waterfall-panel">
      <div class="wf-header">
        <div class="wf-title">Execution Spans Waterfall (Total Latency: 1.492s)</div>
        <span style="font-size:13px; color:#94a3b8; font-family:monospace;">Wall Time: 1,492.4ms</span>
      </div>

      <div class="span-item">
        <div class="span-top">
          <span style="color:#93c5fd;">ROOT: icepol_query_handler</span>
          <span>1,492.4 ms (100%)</span>
        </div>
        <div class="span-bar-bg"><div class="span-bar c1">Global Request Lifecycle</div></div>
      </div>

      <div class="span-item">
        <div class="span-top">
          <span style="color:#c4b5fd;">SPAN 1: semantic_ontology_parsing</span>
          <span>328.0 ms (22%)</span>
        </div>
        <div class="span-bar-bg"><div class="span-bar c2">YAML Semantic Registry Token Match</div></div>
      </div>

      <div class="span-item">
        <div class="span-top">
          <span style="color:#f472b6;">SPAN 2: deepseek_r1_sql_synthesis</span>
          <span>776.0 ms (52%)</span>
        </div>
        <div class="span-bar-bg"><div class="span-bar c3">LLM Chain-of-Thought Reasoning (342 Tokens)</div></div>
      </div>

      <div class="span-item">
        <div class="span-top">
          <span style="color:#6ee7b7;">SPAN 3: duckdb_columnar_query</span>
          <span>180.0 ms (12%)</span>
        </div>
        <div class="span-bar-bg"><div class="span-bar c4">Aggregated 100,000 Parquet Rows</div></div>
      </div>

      <div class="span-item">
        <div class="span-top">
          <span style="color:#fde047;">SPAN 4: audit_minio_mysql_sink</span>
          <span>108.4 ms (7%)</span>
        </div>
        <div class="span-bar-bg"><div class="span-bar c5">Async Persistence & Telemetry Push</div></div>
      </div>
    </div>
  </div>
</body>
</html>"""),

    ("langfuse_s3.html", """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; }
  body { background: #0b0f19; color: #f1f5f9; width: 1920px; height: 1080px; overflow: hidden; display: flex; flex-direction: column; }
  header { height: 64px; background: #111827; border-bottom: 1px solid #1f2937; display: flex; align-items: center; justify-content: space-between; padding: 0 32px; }
  .brand { display: flex; align-items: center; gap: 14px; }
  .brand svg { width: 30px; height: 30px; fill: #38bdf8; }
  .brand h1 { font-size: 20px; font-weight: 700; color: #f8fafc; }
  
  .container { flex: 1; padding: 36px 48px; display: flex; flex-direction: column; align-items: center; }
  .heading { text-align: center; margin-bottom: 36px; }
  .heading h2 { font-size: 32px; font-weight: 800; color: #ffffff; letter-spacing: -0.5px; }
  .heading p { font-size: 16px; color: #94a3b8; margin-top: 8px; }

  .tree-canvas {
    width: 100%; max-width: 1760px; height: 740px; background: #111827; border: 1px solid #1e293b;
    border-radius: 20px; position: relative; display: flex; justify-content: space-between; align-items: center; padding: 40px 60px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
  }

  .tree-col { display: flex; flex-direction: column; gap: 24px; justify-content: center; height: 100%; z-index: 2; width: 280px; }
  .node-box {
    background: #1e293b; border: 2px solid #334155; border-radius: 12px; padding: 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3); position: relative;
  }
  .node-step { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #38bdf8; margin-bottom: 6px; }
  .node-title { font-size: 16px; font-weight: 700; color: #ffffff; margin-bottom: 8px; }
  .node-desc { font-size: 12px; color: #94a3b8; line-height: 1.4; }
  .node-tag { display: inline-block; margin-top: 10px; font-size: 11px; padding: 3px 8px; border-radius: 4px; font-weight: 600; }

  .active-blue { border-color: #0284c7; background: #0c4a6e22; box-shadow: 0 0 20px rgba(2, 132, 199, 0.4); }
  .active-purple { border-color: #8b5cf6; background: #4c1d9522; box-shadow: 0 0 20px rgba(139, 92, 246, 0.4); }
  .active-pink { border-color: #ec4899; background: #83184322; box-shadow: 0 0 20px rgba(236, 72, 153, 0.4); }
  .active-emerald { border-color: #10b981; background: #064e3b22; box-shadow: 0 0 20px rgba(16, 185, 129, 0.4); }
  .active-amber { border-color: #f59e0b; background: #78350f22; box-shadow: 0 0 20px rgba(245, 158, 11, 0.4); }

  .tag-b { background: #0369a1; color: #e0f2fe; }
  .tag-p { background: #6d28d9; color: #ede9fe; }
  .tag-pk { background: #be185d; color: #fce7f3; }
  .tag-e { background: #047857; color: #d1fae5; }
  .tag-a { background: #b45309; color: #fef3c7; }

  .flow-arrow { display: flex; flex-direction: column; align-items: center; justify-content: center; color: #38bdf8; font-size: 28px; font-weight: bold; }
</style>
</head>
<body>
  <header>
    <div class="brand">
      <svg viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
      <h1>Langfuse Trace Tree: End-to-End Decision Graph (DAG)</h1>
    </div>
    <span style="color:#94a3b8; font-size:14px;">Inference Path: <b>User Query &rarr; DeepSeek-R1 &rarr; DuckDB &rarr; MinIO/MySQL</b></span>
  </header>

  <div class="container">
    <div class="heading">
      <h2>Autonomous Semantic Execution Pipeline</h2>
      <p>Every query follows an audited directed acyclic graph (DAG) tracked with span-level telemetry in Langfuse.</p>
    </div>

    <div class="tree-canvas">
      <div class="tree-col">
        <div class="node-box active-blue">
          <div class="node-step">1. Ingestion Node</div>
          <div class="node-title">Natural Language Prompt</div>
          <div class="node-desc">"Exposição total por setor e alavancagem por grupo econômico"</div>
          <span class="node-tag tag-b">FastAPI Gateway</span>
        </div>
      </div>
      <div class="flow-arrow">&rarr;</div>
      <div class="tree-col">
        <div class="node-box active-purple">
          <div class="node-step">2. Semantic Layer</div>
          <div class="node-title">Ontology & Schema Resolution</div>
          <div class="node-desc">Maps natural terms to verified corporate credit dimensions (CNAE, Facilities, Debt).</div>
          <span class="node-tag tag-p">Zero Hallucination</span>
        </div>
      </div>
      <div class="flow-arrow">&rarr;</div>
      <div class="tree-col">
        <div class="node-box active-pink">
          <div class="node-step">3. Reasoning Engine</div>
          <div class="node-title">DeepSeek-R1 (1.5B)</div>
          <div class="node-desc">Generates deterministic DuckDB SQL with validated Crow foot cardinality.</div>
          <span class="node-tag tag-pk">Ollama Local GPU/CPU</span>
        </div>
      </div>
      <div class="flow-arrow">&rarr;</div>
      <div class="tree-col">
        <div class="node-box active-emerald">
          <div class="node-step">4. OLAP Execution</div>
          <div class="node-title">DuckDB In-Memory</div>
          <div class="node-desc">Scans Iceberg Parquet partitions via Apache Polaris catalog in 180ms.</div>
          <span class="node-tag tag-e">Columnar Vectorized</span>
        </div>
      </div>
      <div class="flow-arrow">&rarr;</div>
      <div class="tree-col">
        <div class="node-box active-amber">
          <div class="node-step">5. Observability Sinks</div>
          <div class="node-title">MinIO S3 & MySQL 8</div>
          <div class="node-desc">Persists raw payload traces to MinIO and queries/latencies to MySQL audit table.</div>
          <span class="node-tag tag-a">Audit & Compliance</span>
        </div>
      </div>
    </div>
  </div>
</body>
</html>"""),

    ("langfuse_s4.html", """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; }
  body { background: #0b0f19; color: #f1f5f9; width: 1920px; height: 1080px; overflow: hidden; display: flex; flex-direction: column; }
  header { height: 64px; background: #111827; border-bottom: 1px solid #1f2937; display: flex; align-items: center; justify-content: space-between; padding: 0 32px; }
  .brand { display: flex; align-items: center; gap: 14px; }
  .brand svg { width: 30px; height: 30px; fill: #38bdf8; }
  .brand h1 { font-size: 20px; font-weight: 700; color: #f8fafc; }

  .content { flex: 1; padding: 32px 48px; display: grid; grid-template-columns: 1fr 1fr; gap: 32px; }
  .box { background: #111827; border: 1px solid #1e293b; border-radius: 14px; padding: 24px; display: flex; flex-direction: column; }
  .box-title { font-size: 16px; font-weight: 700; color: #38bdf8; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; }
  
  pre {
    background: #090d16; border: 1px solid #1f2937; border-radius: 10px; padding: 18px; color: #e2e8f0;
    font-family: 'Fira Code', Menlo, monospace; font-size: 13px; line-height: 1.5; overflow: hidden; flex: 1;
  }
  .kw { color: #f472b6; }
  .str { color: #a5f3fc; }
  .fn { color: #60a5fa; }
  .cm { color: #64748b; }
</style>
</head>
<body>
  <header>
    <div class="brand">
      <svg viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
      <h1>Langfuse Generation Inspector: <span style="color:#f472b6;">deepseek-r1:1.5b</span></h1>
    </div>
    <div style="font-size:13px; color:#94a3b8;">Span ID: <span style="font-family:monospace; color:#38bdf8;">gen_9b2e811c</span> | Latency: 776ms | Tokens: 342</div>
  </header>

  <div class="content">
    <div class="box">
      <div class="box-title">
        <span>Prompt Payload (System Semantic Context)</span>
        <span style="font-size:12px; color:#94a3b8;">Tokens: 218</span>
      </div>
      <pre><code><span class="cm">/* Langfuse Captured Input Payload */</span>
{
  <span class="kw">"model"</span>: <span class="str">"deepseek-r1:1.5b"</span>,
  <span class="kw">"domain"</span>: <span class="str">"corporate_credit"</span>,
  <span class="kw">"entities"</span>: [
    { <span class="kw">"entity"</span>: <span class="str">"counterpart"</span>, <span class="kw">"table"</span>: <span class="str">"corporate_credit.counterparts"</span> },
    { <span class="kw">"entity"</span>: <span class="str">"credit_facility"</span>, <span class="kw">"table"</span>: <span class="str">"corporate_credit.facilities"</span>, <span class="kw">"joins"</span>: [<span class="str">"counterpart_id"</span>] },
    { <span class="kw">"entity"</span>: <span class="str">"collateral"</span>, <span class="kw">"table"</span>: <span class="str">"corporate_credit.collaterals"</span> },
    { <span class="kw">"entity"</span>: <span class="str">"financial_statement"</span>, <span class="kw">"metrics"</span>: [<span class="str">"vl_net_debt"</span>, <span class="str">"vl_ebitda"</span>] }
  ],
  <span class="kw">"prompt"</span>: <span class="str">"Exposição total por setor e alavancagem consolidada por grupo"</span>
}</code></pre>
    </div>

    <div class="box">
      <div class="box-title">
        <span>Model Output & Synthesis (Chain-of-Thought)</span>
        <span style="font-size:12px; color:#94a3b8;">Tokens: 124</span>
      </div>
      <pre><code><span class="cm">/* DeepSeek-R1 Synthesized SQL & Mermaid */</span>
&lt;think&gt;
Resolvendo dimensões solicitadas:
- Setor: counterpart.ds_cnae_sector
- Limite: facilities.vl_credit_limit
- Alavancagem: financial_statement.vl_net_debt / vl_ebitda
Validando Crows foot cardinality entre counterpart e facilities...
&lt;/think&gt;

<span class="kw">SELECT</span> 
    c.ds_cnae_sector <span class="kw">AS</span> setor,
    <span class="fn">SUM</span>(f.vl_credit_limit) <span class="kw">AS</span> total_exposicao,
    <span class="fn">AVG</span>(fs.vl_net_debt / <span class="fn">NULLIF</span>(fs.vl_ebitda, 0)) <span class="kw">AS</span> alavancagem_media
<span class="kw">FROM</span> corporate_credit.counterparts c
<span class="kw">JOIN</span> corporate_credit.facilities f <span class="kw">ON</span> c.counterpart_id = f.counterpart_id
<span class="kw">LEFT JOIN</span> corporate_credit.financial_statements fs <span class="kw">ON</span> c.counterpart_id = fs.counterpart_id
<span class="kw">GROUP BY</span> 1
<span class="kw">ORDER BY</span> total_exposicao <span class="kw">DESC</span>;</code></pre>
    </div>
  </div>
</body>
</html>"""),

    ("langfuse_s5.html", """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; }
  body {
    background: radial-gradient(circle at center, #111827 0%, #030712 100%);
    color: #f1f5f9; width: 1920px; height: 1080px; overflow: hidden;
    display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;
  }
  .badge {
    background: #0284c7; color: #ffffff; font-size: 14px; font-weight: 700;
    padding: 8px 20px; border-radius: 9999px; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 24px;
    box-shadow: 0 0 25px rgba(2, 132, 199, 0.6);
  }
  h1 { font-size: 56px; font-weight: 900; letter-spacing: -1px; margin-bottom: 16px; }
  p { font-size: 22px; color: #94a3b8; max-width: 950px; line-height: 1.5; margin-bottom: 48px; }
  
  .stack-grid { display: flex; gap: 30px; }
  .stack-card {
    background: #0f172a; border: 1px solid #1e293b; border-radius: 16px; padding: 24px 32px;
    display: flex; flex-direction: column; align-items: center; gap: 10px; width: 220px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  }
  .stack-name { font-size: 18px; font-weight: 700; color: #ffffff; }
  .stack-role { font-size: 13px; color: #38bdf8; font-weight: 600; }
  .footer-sub { margin-top: 50px; font-size: 15px; color: #64748b; }
</style>
</head>
<body>
  <div class="badge">Enterprise LLM Observability & Governance</div>
  <h1>Langfuse + MinIO + MySQL 8.0 Integration</h1>
  <p>Continuous telemetry, automated prompt caching, full audit trail, and zero-hallucination semantic query synthesis on Apache Iceberg & DuckDB.</p>

  <div class="stack-grid">
    <div class="stack-card">
      <div style="font-size: 32px;">⚡</div>
      <div class="stack-name">Langfuse v2</div>
      <div class="stack-role">Distributed Tracing</div>
    </div>
    <div class="stack-card">
      <div style="font-size: 32px;">🪣</div>
      <div class="stack-name">MinIO S3</div>
      <div class="stack-role">Object Storage</div>
    </div>
    <div class="stack-card">
      <div style="font-size: 32px;">🐬</div>
      <div class="stack-name">MySQL 8.0</div>
      <div class="stack-role">Query Metrics & Audit</div>
    </div>
    <div class="stack-card">
      <div style="font-size: 32px;">🧠</div>
      <div class="stack-name">DeepSeek-R1</div>
      <div class="stack-role">Reasoning Engine</div>
    </div>
    <div class="stack-card">
      <div style="font-size: 32px;">🦆</div>
      <div class="stack-name">DuckDB</div>
      <div class="stack-role">Vectorized OLAP</div>
    </div>
  </div>

  <div class="footer-sub">Icepol Semantic Layer - Fully Open Source & Self-Hosted Stack</div>
</body>
</html>""")
]

for fname, html_code in scenes:
    fpath = os.path.join(OUTPUT_DIR, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(html_code)
    print(f"Written: {fpath}")

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

clip_durations = [
    ("langfuse_s1.png", 7),
    ("langfuse_s2.png", 7),
    ("langfuse_s3.png", 8),
    ("langfuse_s4.png", 7),
    ("langfuse_s5.png", 7)
]

clip_files = []
for i, (png_name, dur) in enumerate(clip_durations):
    clip_path = os.path.join(OUTPUT_DIR, f"lf_clip_{i}.mp4")
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

concat_path = os.path.join(OUTPUT_DIR, "concat_langfuse.txt")
with open(concat_path, "w") as f:
    for c in clip_files:
        f.write(f"file '{os.path.abspath(c)}'\n")

final_output = os.path.join(OUTPUT_DIR, "langfuse_metrics_decision_tree.mp4")
audio_path = os.path.join(OUTPUT_DIR, "soundtrack_80s.wav")

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
print(f"Generated Video 2: {final_output}")
