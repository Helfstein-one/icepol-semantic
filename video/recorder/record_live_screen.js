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

  // ==========================================
  // SCENE 1: Real GitHub Navigation (0s - 13s)
  // ==========================================
  console.log("Scene 1: Loading Real GitHub Repository Page...");
  await page.goto("https://github.com/Helfstein-one/icepol-semantic", { waitUntil: "domcontentloaded", timeout: 20000 });
  await installVirtualCursor(page);
  await cursorMoveTo(page, 960, 400);
  await page.waitForTimeout(1200);

  // Look for the <> Code button or click position
  try {
    const codeBtn = await page.$('button:has-text("Code")');
    if (codeBtn) {
      const box = await codeBtn.boundingBox();
      if (box) {
        await cursorClick(page, box.x + box.width / 2, box.y + box.height / 2);
        await page.waitForTimeout(1500);
      }
    }
  } catch (e) {
    console.log("Code button note:", e.message);
  }

  // Smooth scroll through README
  console.log("Scrolling through GitHub README & Architecture...");
  for (let s = 0; s < 7; s++) {
    await page.evaluate(() => window.scrollBy({ top: 380, behavior: 'smooth' }));
    await cursorMoveTo(page, 600 + (s % 3) * 200, 400 + (s % 2) * 150);
    await page.waitForTimeout(1200);
  }

  // ==========================================
  // SCENE 2: Real Animated Terminal (13s - 23s)
  // ==========================================
  console.log("Scene 2: Loading Terminal (git clone, make seed, podman compose)...");
  const termUrl = "file://" + path.resolve(__dirname, 'live_terminal.html');
  await page.goto(termUrl, { waitUntil: "load" });
  await installVirtualCursor(page);
  await cursorMoveTo(page, 800, 600);

  // Trigger typing in terminal
  await page.evaluate(() => window.startTerminal && window.startTerminal());
  await page.waitForTimeout(9500);

  // ==========================================
  // SCENE 3: Live Icepol Semantic Chat UI (23s - 45s)
  // ==========================================
  console.log("Scene 3: Loading Live Icepol Chat UI (http://localhost:8000)...");
  await page.goto("http://localhost:8000", { waitUntil: "domcontentloaded", timeout: 15000 });
  await installVirtualCursor(page);
  await cursorMoveTo(page, 960, 500);
  await page.waitForTimeout(1500);

  // Move cursor to prompt pill
  const inputEl = await page.$('#user-input');
  if (inputEl) {
    const box = await inputEl.boundingBox();
    if (box) {
      await cursorClick(page, box.x + 50, box.y + box.height / 2);
    }
  }

  // Type question with human cadence
  const queryText = "Qual a exposição total e alavancagem média por setor? Gere também o modelo relacional Mermaid";
  console.log("Typing user question into Chat UI...");
  await page.type('#user-input', queryText, { delay: 45 });
  await page.waitForTimeout(600);

  // Click submit button
  const sendBtn = await page.$('#send-btn');
  if (sendBtn) {
    const sBox = await sendBtn.boundingBox();
    if (sBox) {
      await cursorClick(page, sBox.x + sBox.width / 2, sBox.y + sBox.height / 2);
    }
  } else {
    await page.keyboard.press('Enter');
  }

  // Wait for response or render analytical content
  console.log("Waiting for DuckDB and LLM response...");
  await page.waitForTimeout(4000);

  // If response cell rendered, click Mermaid tab or show Mermaid
  const mermaidTab = await page.$('button:has-text("Diagrama Mermaid"), button:has-text("Mermaid")');
  if (mermaidTab) {
    const mBox = await mermaidTab.boundingBox();
    if (mBox) {
      await cursorClick(page, mBox.x + mBox.width / 2, mBox.y + mBox.height / 2);
      await page.waitForTimeout(3000);
    }
  } else {
    await page.waitForTimeout(2000);
  }

  // Click top header 'Métricas & Traces' popover button
  const obsBtn = await page.$('#header-obs-btn');
  if (obsBtn) {
    const oBox = await obsBtn.boundingBox();
    if (oBox) {
      await cursorClick(page, oBox.x + oBox.width / 2, oBox.y + oBox.height / 2);
      await page.waitForTimeout(2500);
    }
  }

  // ==========================================
  // SCENE 4: Langfuse Tracing & Token Cost Analysis (45s - 60s)
  // ==========================================
  console.log("Scene 4: Loading Langfuse Tracing & Token Spend Cockpit...");
  const lfUrl = "file://" + path.resolve(__dirname, 'live_langfuse.html');
  await page.goto(lfUrl, { waitUntil: "load" });
  await installVirtualCursor(page);

  // Move cursor across spans
  await cursorMoveTo(page, 750, 240); // ROOT
  await page.waitForTimeout(1400);
  await cursorMoveTo(page, 800, 310); // Semantic Parsing
  await page.waitForTimeout(1400);
  await cursorMoveTo(page, 850, 370); // DeepSeek-R1 (Highlighting 776ms CoT)
  await page.waitForTimeout(2500);
  await cursorMoveTo(page, 900, 430); // DuckDB 180ms
  await page.waitForTimeout(1200);

  // Move cursor to Token Cost cards
  await cursorMoveTo(page, 720, 560); // Input Onto (218 Tokens - Most costly in tokens)
  await page.waitForTimeout(2400);
  await cursorMoveTo(page, 1000, 560); // CoT (776ms - Most costly in wall time)
  await page.waitForTimeout(2400);
  await cursorMoveTo(page, 1300, 560); // SQL output
  await page.waitForTimeout(2000);

  console.log("Finishing recording session...");
  await context.close();
  await browser.close();
  console.log("Browser closed. Raw video written to:", recDir);
})();
