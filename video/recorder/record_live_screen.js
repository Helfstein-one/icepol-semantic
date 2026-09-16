const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function installVirtualCursor(page) {
  await page.evaluate(() => {
    if (document.getElementById('v-cursor')) return;
    const c = document.createElement('div');
    c.id = 'v-cursor';
    c.style.position = 'fixed';
    c.style.top = '0';
    c.style.left = '0';
    c.style.width = '24px';
    c.style.height = '24px';
    c.style.pointerEvents = 'none';
    c.style.zIndex = '999999999';
    c.style.transition = 'transform 0.18s cubic-bezier(0.2, 0.8, 0.2, 1)';
    c.innerHTML = `
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="filter: drop-shadow(0 3px 6px rgba(0,0,0,0.7));">
        <path d="M5.5 3.21V20.8c0 .45.54.67.85.35l4.86-4.86a.5.5 0 0 1 .35-.15h6.87c.45 0 .67-.54.35-.85L6.35 2.86a.5.5 0 0 0-.85.35z" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
      </svg>
    `;
    document.body.appendChild(c);

    window.moveCursor = (x, y) => {
      c.style.transform = `translate(${x}px, ${y}px)`;
    };

    window.ripple = (x, y) => {
      const r = document.createElement('div');
      r.style.position = 'fixed';
      r.style.left = `${x - 14}px`;
      r.style.top = `${y - 14}px`;
      r.style.width = '28px';
      r.style.height = '28px';
      r.style.borderRadius = '50%';
      r.style.border = '2px solid #38bdf8';
      r.style.background = 'rgba(56, 189, 248, 0.25)';
      r.style.pointerEvents = 'none';
      r.style.zIndex = '999999998';
      r.style.transition = 'all 0.4s ease-out';
      document.body.appendChild(r);
      setTimeout(() => {
        r.style.transform = 'scale(2.2)';
        r.style.opacity = '0';
      }, 10);
      setTimeout(() => r.remove(), 450);
    };
  });
}

async function cursorMoveTo(page, x, y) {
  await page.evaluate(({x, y}) => {
    if (window.moveCursor) window.moveCursor(x, y);
  }, {x, y});
}

async function cursorClick(page, x, y) {
  await cursorMoveTo(page, x, y);
  await page.waitForTimeout(100);
  await page.evaluate(({x, y}) => {
    if (window.ripple) window.ripple(x, y);
  }, {x, y});
  await page.mouse.click(x, y);
}

(async () => {
  const recDir = path.resolve(__dirname, 'raw_recordings');
  if (fs.existsSync(recDir)) {
    fs.rmSync(recDir, { recursive: true, force: true });
  }
  fs.mkdirSync(recDir, { recursive: true });

  console.log("Launching Chromium for Real Screen Recording (1920x1080)...");
  const browser = await chromium.launch({
    executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    headless: true,
    args: [
      "--window-size=1920,1080",
      "--no-sandbox",
      "--disable-dev-shm-usage",
      "--hide-scrollbars",
      "--font-render-hinting=none"
    ]
  });

  const context = await browser.newContext({
    recordVideo: {
      dir: recDir,
      size: { width: 1920, height: 1080 }
    },
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1
  });

  const page = await context.newPage();

  // =========================================================================
  // SCENE 1: Real GitHub Navigation - All the way to the End (0s - 22s)
  // =========================================================================
  console.log("Scene 1: Loading Real GitHub Repository Page...");
  await page.goto("https://github.com/Helfstein-one/icepol-semantic", { waitUntil: "domcontentloaded", timeout: 25000 });
  await installVirtualCursor(page);
  await cursorMoveTo(page, 960, 400);
  await page.waitForTimeout(1500);

  // Click <> Code button to reveal repo URL
  try {
    const codeBtn = await page.$('button:has-text("Code")');
    if (codeBtn) {
      const box = await codeBtn.boundingBox();
      if (box) {
        await cursorClick(page, box.x + box.width / 2, box.y + box.height / 2);
        await page.waitForTimeout(1800);
        // Click again to close dropdown cleanly
        await cursorClick(page, box.x + box.width / 2, box.y + box.height / 2);
        await page.waitForTimeout(600);
      }
    }
  } catch (e) {
    console.log("Code button note:", e.message);
  }

  // Smooth progressive scroll through all sections all the way down to the footer!
  console.log("Scrolling smoothly through the entire GitHub README to the end...");
  const scrollSteps = 12;
  for (let s = 0; s < scrollSteps; s++) {
    await page.evaluate(() => window.scrollBy({ top: 580, behavior: 'smooth' }));
    await cursorMoveTo(page, 650 + (s % 3) * 180, 450 + (s % 2) * 120);
    await page.waitForTimeout(1100);
  }

  // Final scroll to ensure very bottom footer (License, GitHub footer links)
  await page.evaluate(() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }));
  await cursorMoveTo(page, 960, 850);
  await page.waitForTimeout(2000);

  // =========================================================================
  // SCENE 2: Real Animated Terminal - Full Install & Seed (22s - 40s)
  // =========================================================================
  console.log("Scene 2: Loading Terminal (git clone, pip install, make seed, podman compose)...");
  const termUrl = "file://" + path.resolve(__dirname, 'live_terminal.html');
  await page.goto(termUrl, { waitUntil: "load" });
  await installVirtualCursor(page);
  await cursorMoveTo(page, 800, 600);

  // Trigger typing in terminal
  await page.evaluate(() => window.startTerminal && window.startTerminal());
  // Wait for all steps to complete typing and outputting (~17.5s)
  await page.waitForTimeout(17500);

  // =========================================================================
  // SCENE 3: Live Icepol Semantic Chat UI - Journey with Model & Mermaid (40s - 63s)
  // =========================================================================
  console.log("Scene 3: Loading Live Icepol Chat UI (http://localhost:8000)...");

  // Intercept completion endpoint to return structured analytical response with DuckDB data and Mermaid ERD
  await page.route('**/v1/chat/completions', async (route) => {
    const postData = route.request().postDataJSON() || {};
    const reqModel = postData.model || 'deepseek-r1:1.5b';
    
    // Simulate realistic 1.8s thinking/execution latency
    await new Promise(r => setTimeout(r, 1800));

    const responseBody = {
      id: "chatcmpl-icepol-demo",
      object: "chat.completion",
      created: Math.floor(Date.now() / 1000),
      model: reqModel,
      choices: [
        {
          index: 0,
          message: {
            role: "assistant",
            content: "### Análise Executiva de Crédito Corporativo\n\n- **Exposição Consolidada**: R$ 14,80 bilhões distribuídos em 4 setores estratégicos.\n- **Alavancagem Média**: O setor Agroindustrial apresenta a maior alavancagem média (**3,42x Dívida Líq/EBITDA**), enquanto Energia & Infraestrutura opera em patamar prudencial de **1,85x**.\n- **Garantias**: Cobertura média de alienação fiduciária e recebíveis de 142% sobre o saldo devedor ativo.\n\n```mermaid\nerDiagram\n    COUNTERPARTS ||--o{ FACILITIES : \"toma_emprestimo\"\n    COUNTERPARTS ||--o{ FINANCIAL_STATEMENTS : \"reporta_balanco\"\n    FACILITIES ||--o{ COLLATERALS : \"garantido_por\"\n    FACILITIES ||--o{ COVENANTS : \"monitorado_por\"\n    COUNTERPARTS {\n        string counterpart_id PK\n        string legal_name\n        string sector\n        string rating_internal\n    }\n    FACILITIES {\n        string facility_id PK\n        string counterpart_id FK\n        decimal outstanding_balance\n        decimal interest_rate\n        string status\n    }\n    FINANCIAL_STATEMENTS {\n        string statement_id PK\n        string counterpart_id FK\n        decimal net_debt\n        decimal ebitda\n        decimal leverage_ratio\n    }\n    COLLATERALS {\n        string collateral_id PK\n        string facility_id FK\n        decimal pledged_value\n    }\n```",
            sql: "SELECT \n  c.sector AS setor,\n  COUNT(DISTINCT c.counterpart_id) AS total_tomadores,\n  ROUND(SUM(f.outstanding_balance) / 1e6, 2) AS exposicao_total_mm,\n  ROUND(AVG(fs.net_debt / NULLIF(fs.ebitda, 0)), 2) AS alavancagem_media_x,\n  ROUND(AVG(f.interest_rate) * 100, 2) AS taxa_media_aa\nFROM counterparts c\nJOIN facilities f ON c.counterpart_id = f.counterpart_id\nJOIN financial_statements fs ON c.counterpart_id = fs.counterpart_id\nWHERE f.status = 'ACTIVE'\nGROUP BY c.sector\nORDER BY exposicao_total_mm DESC;",
            data: [
              { "setor": "Agroindustrial", "total_tomadores": 312, "exposicao_total_mm": 5420.50, "alavancagem_media_x": 3.42, "taxa_media_aa": 13.85 },
              { "setor": "Energia & Infra", "total_tomadores": 184, "exposicao_total_mm": 4180.20, "alavancagem_media_x": 1.85, "taxa_media_aa": 12.10 },
              { "setor": "Indústria Manufatura", "total_tomadores": 275, "exposicao_total_mm": 3250.80, "alavancagem_media_x": 2.65, "taxa_media_aa": 14.20 },
              { "setor": "Varejo & Serviços", "total_tomadores": 229, "exposicao_total_mm": 1950.40, "alavancagem_media_x": 2.90, "taxa_media_aa": 15.10 }
            ],
            metrics: {
              tokens_estimated: 342,
              llm_latency_ms: 776.0,
              duckdb_latency_ms: 180.0,
              total_latency_ms: 1492.4,
              postgres_logged: true
            }
          },
          finish_reason: "stop"
        }
      ],
      usage: {
        prompt_tokens: 218,
        completion_tokens: 124,
        total_tokens: 342
      }
    };

    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(responseBody)
    });
  });

  await page.goto("http://localhost:8000", { waitUntil: "domcontentloaded", timeout: 15000 });
  await installVirtualCursor(page);
  await cursorMoveTo(page, 960, 500);
  await page.waitForTimeout(1000);

  // 1. Select Model: Click model dropdown button
  console.log("Interacting with model selector dropdown...");
  const modelBtn = await page.$('#model-dropdown-btn');
  if (modelBtn) {
    const mbBox = await modelBtn.boundingBox();
    if (mbBox) {
      await cursorClick(page, mbBox.x + mbBox.width / 2, mbBox.y + mbBox.height / 2);
      await page.waitForTimeout(1200);

      // Select deepseek-r1:1.5b from dropdown list
      const deepseekOption = await page.$('#model-list button:has-text("deepseek-r1:1.5b")');
      if (deepseekOption) {
        const dsBox = await deepseekOption.boundingBox();
        if (dsBox) {
          await cursorClick(page, dsBox.x + dsBox.width / 2, dsBox.y + dsBox.height / 2);
          await page.waitForTimeout(1000);
        }
      } else {
        // Direct trigger if not in list
        await page.evaluate(() => window.selectModel && window.selectModel('deepseek-r1:1.5b'));
        await page.waitForTimeout(800);
      }
    }
  }

  // 2. Click prompt input
  const inputEl = await page.$('#user-input');
  if (inputEl) {
    const box = await inputEl.boundingBox();
    if (box) {
      await cursorClick(page, box.x + 50, box.y + box.height / 2);
    }
  }

  // 3. Type question with human cadence
  const queryText = "Qual a exposição total e alavancagem média por setor? Gere também o modelo relacional Mermaid";
  console.log("Typing user question into Chat UI...");
  await page.type('#user-input', queryText, { delay: 35 });
  await page.waitForTimeout(400);

  // 4. Click Send button
  const sendBtn = await page.$('#send-btn');
  if (sendBtn) {
    const sBox = await sendBtn.boundingBox();
    if (sBox) {
      await cursorClick(page, sBox.x + sBox.width / 2, sBox.y + sBox.height / 2);
    }
  } else {
    await page.keyboard.press('Enter');
  }

  // 5. Wait for response to render
  console.log("Waiting for DuckDB and LLM response notebook cell...");
  await page.waitForTimeout(3000);

  // 6. Click 'Diagrama Mermaid' tab to reveal ERD
  console.log("Clicking Diagrama Mermaid tab...");
  const mermaidTab = await page.$('button:has-text("Diagrama Mermaid"), button:has-text("Mermaid")');
  if (mermaidTab) {
    const mBox = await mermaidTab.boundingBox();
    if (mBox) {
      await cursorClick(page, mBox.x + mBox.width / 2, mBox.y + mBox.height / 2);
      await page.waitForTimeout(2800);
      // Hover over diagram
      await cursorMoveTo(page, 960, 560);
      await page.waitForTimeout(1200);
    }
  }

  // 7. Click top header 'Métricas & Traces' popover button
  console.log("Opening Métricas & Traces popover...");
  const obsBtn = await page.$('#header-obs-btn');
  if (obsBtn) {
    const oBox = await obsBtn.boundingBox();
    if (oBox) {
      await cursorClick(page, oBox.x + oBox.width / 2, oBox.y + oBox.height / 2);
      await page.waitForTimeout(2400);
    }
  }

  // =========================================================================
  // SCENE 4: Langfuse Login & Decision Tree / Observability (63s - 85s)
  // =========================================================================
  console.log("Scene 4: Loading Langfuse Tracing & Decision Tree Cockpit...");
  const lfUrl = "file://" + path.resolve(__dirname, 'live_langfuse.html');
  await page.goto(lfUrl, { waitUntil: "load" });
  await installVirtualCursor(page);
  await cursorMoveTo(page, 960, 500);
  await page.waitForTimeout(1200);

  // 1. Move to Login Button and click
  console.log("Clicking Sign in to Project button in Langfuse Login overlay...");
  await cursorClick(page, 960, 610);
  // Wait for login animation to fade overlay out
  await page.waitForTimeout(1600);

  // 2. Highlight Decision Tree / DAG nodes
  console.log("Tracing across Decision Tree DAG nodes...");
  await cursorMoveTo(page, 720, 150); // Node 1: Ingestion
  await page.waitForTimeout(1200);
  await cursorMoveTo(page, 920, 150); // Node 2: Semantic Parser
  await page.waitForTimeout(1200);
  await cursorMoveTo(page, 1140, 150); // Node 3: DeepSeek-R1 (CoT)
  await page.waitForTimeout(1800);
  await cursorMoveTo(page, 1360, 150); // Node 4: DuckDB Columnar
  await page.waitForTimeout(1200);
  await cursorMoveTo(page, 1560, 150); // Node 5: PostgreSQL 15 Audit
  await page.waitForTimeout(1400);

  // 3. Move cursor to Spans Waterfall
  console.log("Inspecting Spans Waterfall...");
  await cursorMoveTo(page, 850, 370); // DeepSeek-R1 (Highlighting 776ms CoT)
  await page.waitForTimeout(2000);
  await cursorMoveTo(page, 900, 430); // DuckDB 180ms
  await page.waitForTimeout(1200);

  // 4. Move cursor to Token Cost cards
  console.log("Inspecting Token Cost Cards...");
  await cursorMoveTo(page, 720, 560); // Input Onto (218 Tokens - Most costly in tokens)
  await page.waitForTimeout(2000);
  await cursorMoveTo(page, 1000, 560); // CoT (776ms - Most costly in wall time)
  await page.waitForTimeout(2200);
  await cursorMoveTo(page, 1300, 560); // SQL output
  await page.waitForTimeout(2000);

  console.log("Finishing recording session...");
  await context.close();
  await browser.close();
  console.log("Browser closed. Raw video written to:", recDir);
})();
