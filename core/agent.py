import os
import json
import time
import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from semantic.parser import SemanticRegistry
from core.engine import DuckDBIcebergEngine

app = FastAPI(title="Icepol Semantic Middleware Agent", version="1.0.0")

# Paths and Config
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ONTOLOGY_DIR = os.getenv("ONTOLOGY_DIR", os.path.join(BASE_DIR, "semantic", "ontologies"))
LLAMA_SERVER_URL = os.getenv("LLAMA_SERVER_URL", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2:3b")

registry = SemanticRegistry(ONTOLOGY_DIR)
engine = DuckDBIcebergEngine(
    s3_endpoint=os.getenv("MINIO_ENDPOINT", "localhost:9000"),
    s3_access_key=os.getenv("MINIO_ACCESS_KEY", "admin"),
    s3_secret_key=os.getenv("MINIO_SECRET_KEY", "password123")
)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str = "local-model"
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.2
    stream: Optional[bool] = False

@app.get("/", response_class=HTMLResponse)
def index_ui():
    """Interface Web Interativa de Chat para a Camada Semântica."""
    return """
    <!DOCTYPE html>
    <html lang="pt-BR" class="h-full">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>icepol-semantic</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
        <style>
            .prose pre {
                margin-top: 0.75rem;
                margin-bottom: 0.75rem;
                border-radius: 0.75rem;
                background-color: #020617 !important;
                border: 1px solid #1e293b;
                padding: 1rem;
            }
            .prose code {
                font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
                font-size: 0.8125rem;
            }
            .prose p {
                margin-bottom: 0.75rem;
                line-height: 1.625;
            }
            .prose strong {
                color: #93c5fd;
            }
            @keyframes pulse-subtle {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.4; }
            }
            .animate-pulse-subtle {
                animation: pulse-subtle 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
            }
        </style>
    </head>
    <body class="bg-slate-950 text-slate-100 flex flex-col h-full font-sans antialiased selection:bg-blue-500 selection:text-white">
        <!-- Minimalist Header -->
        <header class="border-b border-slate-800/80 bg-slate-900/70 backdrop-blur-md px-6 md:px-10 py-4 flex items-center justify-between sticky top-0 z-20">
            <div class="flex items-center">
                <span class="text-xl font-bold tracking-tight text-white font-mono">icepol-semantic</span>
            </div>
            <div class="flex items-center space-x-3 text-xs">
                <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                    LLM: llama3.2:3b (Ollama)
                </span>
                <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full font-medium bg-blue-500/10 text-blue-400 border border-blue-500/20">
                    <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
                    DuckDB Engine: Ativo
                </span>
            </div>
        </header>

        <!-- Main Chat Stream -->
        <main class="flex-1 overflow-y-auto px-4 md:px-8 py-8" id="chat-container">
            <div class="max-w-5xl mx-auto space-y-6" id="chat-box">
                <!-- Minimalist Gemini Centered Welcome View -->
                <div id="welcome-view" class="py-14 md:py-20 flex flex-col items-center justify-center text-center space-y-6">
                    <div class="space-y-2">
                        <h1 class="text-4xl md:text-5xl font-medium tracking-tight bg-gradient-to-r from-blue-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent">
                            Olá, Mauricio
                        </h1>
                        <p class="text-xl md:text-2xl text-slate-400 font-normal">
                            Como posso ajudar com crédito corporativo hoje?
                        </p>
                    </div>

                    <!-- Clean Minimalist Gemini Prompt Chips -->
                    <div class="flex flex-wrap items-center justify-center gap-2.5 max-w-2xl pt-2">
                        <button onclick="sendPrompt('Qual a exposição total (total_exposure) por setor (sector)?')" 
                            class="px-4 py-2.5 rounded-full bg-[#1e1f20] hover:bg-[#282a2c] text-slate-300 hover:text-white border border-slate-700/60 transition text-xs md:text-sm font-medium shadow-sm">
                            Exposição total por setor
                        </button>
                        <button onclick="sendPrompt('Qual a alavancagem média (avg_net_debt_ebitda) por grupo econômico?')" 
                            class="px-4 py-2.5 rounded-full bg-[#1e1f20] hover:bg-[#282a2c] text-slate-300 hover:text-white border border-slate-700/60 transition text-xs md:text-sm font-medium shadow-sm">
                            Alavancagem por grupo econômico
                        </button>
                        <button onclick="sendPrompt('Qual o volume de garantias por tipo de colateral e status?')" 
                            class="px-4 py-2.5 rounded-full bg-[#1e1f20] hover:bg-[#282a2c] text-slate-300 hover:text-white border border-slate-700/60 transition text-xs md:text-sm font-medium shadow-sm">
                            Garantias por colateral
                        </button>
                        <button onclick="sendPrompt('Quais contratos possuem descumprimento de covenants?')" 
                            class="px-4 py-2.5 rounded-full bg-[#1e1f20] hover:bg-[#282a2c] text-slate-300 hover:text-white border border-slate-700/60 transition text-xs md:text-sm font-medium shadow-sm">
                            Descumprimento de covenants
                        </button>
                    </div>
                </div>
            </div>
        </main>

        <!-- Gemini Pill Floating Footer Input (Exact Perspective) -->
        <footer class="px-4 md:px-8 py-5 sticky bottom-0 z-20">
            <div class="max-w-4xl mx-auto">
                <form id="chat-form" onsubmit="handleSubmit(event)" class="relative flex items-center bg-[#1e1f20] hover:bg-[#26282c] focus-within:bg-[#1e1f20] border border-slate-700/70 focus-within:border-slate-500 rounded-full px-3.5 py-2.5 md:py-3 shadow-2xl transition-all duration-200">
                    
                    <!-- Left + Button (Actions / Tools) -->
                    <button type="button" class="w-9 h-9 rounded-full flex items-center justify-center text-slate-300 hover:text-white hover:bg-white/10 transition shrink-0" title="Ações e ferramentas">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                        </svg>
                    </button>

                    <!-- Text input with 'Peça ao Gemini' placeholder -->
                    <input id="user-input" type="text" placeholder="Peça ao Gemini" 
                        class="flex-1 bg-transparent border-0 text-white placeholder-slate-400 text-sm md:text-base focus:ring-0 focus:outline-none px-3 font-sans">

                    <!-- Right Items: Flash Model Dropdown & Microphone -->
                    <div class="flex items-center space-x-1.5 shrink-0 pr-1">
                        <!-- Model badge dropdown (Flash) -->
                        <div class="flex items-center gap-1.5 text-xs text-slate-300 hover:text-white px-3 py-1.5 rounded-full hover:bg-white/10 transition cursor-pointer font-sans" title="Modelo selecionado">
                            <span>Flash</span>
                            <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                            </svg>
                        </div>

                        <!-- Microphone button -->
                        <button type="button" class="w-9 h-9 rounded-full flex items-center justify-center text-slate-300 hover:text-white hover:bg-white/10 transition" title="Entrada por voz">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 02-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/>
                            </svg>
                        </button>

                        <!-- Send button -->
                        <button type="submit" id="send-btn" class="w-9 h-9 rounded-full bg-white hover:bg-slate-200 text-slate-900 flex items-center justify-center transition shadow shrink-0" title="Enviar">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 12h14M12 5l7 7-7 7"/>
                            </svg>
                        </button>
                    </div>
                </form>
            </div>
        </footer>

        <script>
            const chatBox = document.getElementById('chat-box');
            const userInput = document.getElementById('user-input');
            const sendBtn = document.getElementById('send-btn');
            const messages = [];
            let cellCounter = 0;

            function sendPrompt(text) {
                userInput.value = text;
                handleSubmit(new Event('submit'));
            }

            function copyToClipboard(text, btnElement) {
                navigator.clipboard.writeText(text).then(() => {
                    const originalHtml = btnElement.innerHTML;
                    btnElement.innerHTML = '<span class="text-emerald-400">✓ Copiado!</span>';
                    setTimeout(() => {
                        btnElement.innerHTML = originalHtml;
                    }, 2000);
                });
            }

            function downloadCsv(data, filename) {
                if (!data || !data.length) return;
                const headers = Object.keys(data[0]);
                const csvRows = [headers.join(',')];
                data.forEach(row => {
                    const values = headers.map(h => {
                        const val = ('' + (row[h] ?? '')).replace(/"/g, '""');
                        return `"${val}"`;
                    });
                    csvRows.push(values.join(','));
                });
                const blob = new Blob([csvRows.join('\\n')], { type: 'text/csv;charset=utf-8;' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = filename || 'icepol_query_results.csv';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            }

            function renderTableHtml(data) {
                if (!data || !Array.isArray(data) || data.length === 0) return '<p class="text-xs text-slate-500 italic p-3">Nenhum registro retornado.</p>';
                const headers = Object.keys(data[0]);
                let html = '<div class="overflow-x-auto rounded-xl border border-slate-800 bg-slate-950/70">';
                html += '<table class="min-w-full divide-y divide-slate-800 text-xs">';
                html += '<thead class="bg-slate-900/90 font-mono text-slate-300 uppercase tracking-wider">';
                html += '<tr>';
                headers.forEach(h => {
                    html += `<th class="px-4 py-3 text-left font-semibold">${h}</th>`;
                });
                html += '</tr></thead>';
                html += '<tbody class="divide-y divide-slate-800/60 font-sans text-slate-200">';
                data.forEach((row, idx) => {
                    const bg = idx % 2 === 0 ? 'bg-slate-900/20' : 'bg-slate-900/50';
                    html += `<tr class="${bg} hover:bg-blue-950/30 transition">`;
                    headers.forEach(h => {
                        let val = row[h];
                        if (typeof val === 'number') {
                            val = val.toLocaleString('pt-BR');
                        }
                        html += `<td class="px-4 py-2.5 whitespace-nowrap">${val !== null && val !== undefined ? val : '-'}</td>`;
                    });
                    html += '</tr>';
                });
                html += '</tbody></table></div>';
                return html;
            }

            function appendUserMessage(content) {
                const wrapper = document.createElement('div');
                wrapper.className = 'flex justify-end pt-2';
                
                const bubble = document.createElement('div');
                bubble.className = 'bg-blue-600 text-white rounded-3xl rounded-tr-sm px-6 py-4 max-w-2xl text-sm shadow-md leading-relaxed';
                bubble.innerText = content;
                
                wrapper.appendChild(bubble);
                chatBox.appendChild(wrapper);
                chatBox.scrollIntoView({ behavior: 'smooth', block: 'end' });
            }

            function showProcessingStepper() {
                const stepper = document.createElement('div');
                stepper.id = 'gemini-stepper';
                stepper.className = 'border border-blue-500/30 bg-slate-900/80 rounded-3xl p-6 shadow-xl space-y-4';
                
                stepper.innerHTML = `
                    <div class="flex items-center justify-between border-b border-slate-800/80 pb-3">
                        <div class="flex items-center gap-3">
                            <span class="relative flex h-3 w-3">
                                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                                <span class="relative inline-flex rounded-full h-3 w-3 bg-blue-500"></span>
                            </span>
                            <span class="text-xs font-mono font-semibold uppercase tracking-wider text-blue-400">
                                Gemini Processing Cell [In ${cellCounter + 1}]
                            </span>
                        </div>
                        <span class="text-xs text-slate-400 font-mono" id="stepper-time">0.0s</span>
                    </div>
                    <div class="space-y-2.5 text-xs text-slate-300 font-mono">
                        <div id="step-1" class="flex items-center gap-2.5 text-blue-300">
                            <span class="w-2 h-2 rounded-full bg-blue-400 animate-pulse"></span>
                            <span>Mapeando ontologias & contratos de crédito corporativo...</span>
                        </div>
                        <div id="step-2" class="flex items-center gap-2.5 text-slate-500">
                            <span class="w-2 h-2 rounded-full bg-slate-700"></span>
                            <span>Compilando AST SQL canônico via Ollama (llama3.2:3b)...</span>
                        </div>
                        <div id="step-3" class="flex items-center gap-2.5 text-slate-500">
                            <span class="w-2 h-2 rounded-full bg-slate-700"></span>
                            <span>Executando consulta federada no DuckDB Lakehouse...</span>
                        </div>
                    </div>
                `;

                chatBox.appendChild(stepper);
                chatBox.scrollIntoView({ behavior: 'smooth', block: 'end' });

                let elapsed = 0.0;
                const timerInterval = setInterval(() => {
                    elapsed += 0.2;
                    const timerEl = document.getElementById('stepper-time');
                    if (timerEl) timerEl.innerText = elapsed.toFixed(1) + 's';

                    if (elapsed >= 1.0) {
                        const s2 = document.getElementById('step-2');
                        if (s2) {
                            s2.className = 'flex items-center gap-2.5 text-blue-300';
                            s2.querySelector('span').className = 'w-2 h-2 rounded-full bg-blue-400 animate-pulse';
                        }
                    }
                    if (elapsed >= 2.5) {
                        const s3 = document.getElementById('step-3');
                        if (s3) {
                            s3.className = 'flex items-center gap-2.5 text-blue-300';
                            s3.querySelector('span').className = 'w-2 h-2 rounded-full bg-blue-400 animate-pulse';
                        }
                    }
                }, 200);

                return () => clearInterval(timerInterval);
            }

            function appendAssistantNotebookCell(msgData) {
                cellCounter++;
                const cellId = 'cell-' + cellCounter;
                const sql = msgData.sql || '';
                const data = msgData.data || null;
                const execTime = msgData.execution_time_ms || 0;
                const duckTime = msgData.duckdb_time_ms || 0;
                const rowCount = msgData.row_count || 0;
                const fullContent = msgData.content || '';

                const wrapper = document.createElement('div');
                wrapper.className = 'w-full pt-2';

                // Notebook Cell Container
                const cell = document.createElement('div');
                cell.className = 'bg-slate-900/90 border border-slate-800 rounded-3xl overflow-hidden shadow-xl';

                // Cell Header / Notebook Action Bar
                let actionsHtml = `
                    <div class="bg-slate-950/80 border-b border-slate-800 px-5 py-3 flex flex-wrap items-center justify-between gap-3 text-xs">
                        <div class="flex items-center gap-3">
                            <span class="font-mono text-emerald-400 font-bold bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                                [Out ${cellCounter}]
                            </span>
                            <span class="text-slate-400 font-mono">
                                DuckDB Engine
                            </span>
                            <span class="text-slate-600">•</span>
                            <span class="text-slate-400 font-mono">⚡ ${execTime}ms ${duckTime > 0 ? `(DuckDB: ${duckTime}ms)` : ''}</span>
                            ${rowCount > 0 ? `<span class="text-slate-600">•</span><span class="text-slate-400 font-mono">📊 ${rowCount} registros</span>` : ''}
                        </div>
                        <div class="flex items-center gap-2">
                            ${sql ? `
                                <button onclick="copyToClipboard(\`${sql.replace(/`/g, '\\\\`')}\`, this)" class="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs font-medium border border-slate-700 transition flex items-center gap-1">
                                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
                                    <span>Copiar SQL</span>
                                </button>
                            ` : ''}
                            ${data && data.length ? `
                                <button onclick="downloadCsv(window.cellData_${cellCounter}, 'icepol_export_${cellCounter}.csv')" class="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs font-medium border border-slate-700 transition flex items-center gap-1">
                                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                                    <span>Exportar CSV</span>
                                </button>
                            ` : ''}
                            <button onclick="copyToClipboard(\`${fullContent.replace(/`/g, '\\\\`')}\`, this)" class="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs font-medium border border-slate-700 transition flex items-center gap-1">
                                <span>Copiar Resposta</span>
                            </button>
                        </div>
                    </div>
                `;

                // If tabular data exists, save to window for CSV export
                if (data) {
                    window['cellData_' + cellCounter] = data;
                }

                // Interactive View Tabs (if tabular data / SQL exists)
                let tabsHtml = '';
                if (data && data.length) {
                    tabsHtml = `
                        <div class="flex items-center gap-2 border-b border-slate-800 px-6 pt-3 bg-slate-900/40 text-xs font-mono">
                            <button onclick="switchTab('${cellId}', 'table')" id="btn-${cellId}-table" class="tab-btn px-3 py-1.5 border-b-2 border-blue-500 text-blue-400 font-semibold transition">
                                📊 Tabela de Resultados
                            </button>
                            ${sql ? `
                            <button onclick="switchTab('${cellId}', 'sql')" id="btn-${cellId}-sql" class="tab-btn px-3 py-1.5 border-b-2 border-transparent text-slate-400 hover:text-slate-200 transition">
                                📄 Código SQL
                            </button>` : ''}
                            <button onclick="switchTab('${cellId}', 'json')" id="btn-${cellId}-json" class="tab-btn px-3 py-1.5 border-b-2 border-transparent text-slate-400 hover:text-slate-200 transition">
                                💾 JSON Bruto
                            </button>
                            <button onclick="switchTab('${cellId}', 'raw')" id="btn-${cellId}-raw" class="tab-btn px-3 py-1.5 border-b-2 border-transparent text-slate-400 hover:text-slate-200 transition">
                                📝 Markdown Completo
                            </button>
                        </div>
                    `;
                }

                // Content Views Container
                let bodyHtml = `<div class="p-6 text-sm text-slate-200 space-y-4">`;

                if (data && data.length) {
                    bodyHtml += `
                        <div id="${cellId}-view-table" class="tab-view block">
                            ${renderTableHtml(data)}
                        </div>
                        ${sql ? `
                        <div id="${cellId}-view-sql" class="tab-view hidden">
                            <pre class="bg-slate-950 p-4 rounded-xl border border-slate-800 text-xs font-mono text-blue-300 overflow-x-auto"><code class="language-sql">${sql}</code></pre>
                        </div>` : ''}
                        <div id="${cellId}-view-json" class="tab-view hidden">
                            <pre class="bg-slate-950 p-4 rounded-xl border border-slate-800 text-xs font-mono text-emerald-300 overflow-x-auto"><code>${JSON.stringify(data, null, 2)}</code></pre>
                        </div>
                        <div id="${cellId}-view-raw" class="tab-view hidden prose prose-invert max-w-none text-xs leading-relaxed">
                            ${marked.parse(fullContent)}
                        </div>
                    `;
                } else {
                    bodyHtml += `<div class="prose prose-invert max-w-none text-sm leading-relaxed">${marked.parse(fullContent)}</div>`;
                }

                bodyHtml += `</div>`;

                cell.innerHTML = actionsHtml + tabsHtml + bodyHtml;
                wrapper.appendChild(cell);
                chatBox.appendChild(wrapper);

                // Highlight code blocks
                wrapper.querySelectorAll('pre code').forEach((block) => {
                    hljs.highlightElement(block);
                });

                chatBox.scrollIntoView({ behavior: 'smooth', block: 'end' });
            }

            function switchTab(cellId, tabName) {
                const cell = document.getElementById(cellId + '-view-table')?.parentElement;
                if (!cell) return;

                // Hide all tab views
                cell.querySelectorAll('.tab-view').forEach(el => el.classList.add('hidden'));
                cell.querySelectorAll('.tab-view').forEach(el => el.classList.remove('block'));

                // Show target tab view
                const targetView = document.getElementById(`${cellId}-view-${tabName}`);
                if (targetView) {
                    targetView.classList.remove('hidden');
                    targetView.classList.add('block');
                }

                // Update tab buttons
                const header = cell.previousElementSibling;
                if (header) {
                    header.querySelectorAll('.tab-btn').forEach(b => {
                        b.classList.remove('border-blue-500', 'text-blue-400', 'font-semibold');
                        b.classList.add('border-transparent', 'text-slate-400');
                    });
                    const activeBtn = document.getElementById(`btn-${cellId}-${tabName}`);
                    if (activeBtn) {
                        activeBtn.classList.remove('border-transparent', 'text-slate-400');
                        activeBtn.classList.add('border-blue-500', 'text-blue-400', 'font-semibold');
                    }
                }
            }

            async function handleSubmit(e) {
                e.preventDefault();
                const q = userInput.value.trim();
                if (!q) return;

                const welcomeEl = document.getElementById('welcome-view');
                if (welcomeEl) welcomeEl.remove();

                appendUserMessage(q);
                messages.push({role: 'user', content: q});
                userInput.value = '';
                userInput.disabled = true;
                sendBtn.disabled = true;
                sendBtn.innerHTML = '<svg class="w-4 h-4 animate-spin text-slate-900" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path></svg>';

                const stopTimer = showProcessingStepper();

                try {
                    const res = await fetch('/v1/chat/completions', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            model: 'llama3.2:3b',
                            messages: messages
                        })
                    });
                    const data = await res.json();
                    
                    // Remove stepper
                    stopTimer();
                    const stepperEl = document.getElementById('gemini-stepper');
                    if (stepperEl) stepperEl.remove();

                    const choiceMsg = data.choices[0].message;
                    appendAssistantNotebookCell(choiceMsg);
                    messages.push({role: 'assistant', content: choiceMsg.content});
                } catch (err) {
                    stopTimer();
                    const stepperEl = document.getElementById('gemini-stepper');
                    if (stepperEl) stepperEl.remove();

                    appendAssistantNotebookCell({
                        content: '⚠️ **Erro ao consultar o agente:** ' + err.message,
                        sql: null,
                        data: null
                    });
                } finally {
                    userInput.disabled = false;
                    sendBtn.disabled = false;
                    sendBtn.innerHTML = '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 12h14M12 5l7 7-7 7"/></svg>';
                    userInput.focus();
                }
            }
        </script>
    </body>
    </html>
    """

@app.get("/health")
def health_check():
    return {"status": "ok", "domain": registry.domain}

@app.get("/semantic/context")
def get_semantic_context():
    return {"context": registry.get_prompt_context()}

@app.post("/v1/chat/completions")
async def chat_completions(req: ChatCompletionRequest):
    """Middleware compatível com OpenAI API para Open WebUI."""
    user_message = req.messages[-1].content if req.messages else ""
    
    # 1. Inject Semantic Context into System Prompt
    semantic_context = registry.get_prompt_context()
    system_prompt = (
        "Você é um assistente analítico especializado em Crédito Corporativo e Camada Semântica.\n"
        "Com base no Modelo Semântico abaixo, converta a pergunta do usuário em uma consulta SQL válida para DuckDB.\n\n"
        f"=== CONTEXTO SEMÂNTICO ===\n{semantic_context}\n===========================\n\n"
        "Regras fundamentais:\n"
        "1. Responda com a query SQL dentro de um bloco ```sql ... ``` se a solicitação puder ser convertida em consulta analítica.\n"
        "2. Sempre use as tabelas qualificadas com o schema (ex: `corporate_credit.facilities`, `corporate_credit.counterparts`).\n"
        "3. Ao combinar métricas de uma entidade com dimensões de outra, utilize JOIN explícito usando as relações indicadas em 'Joins' (ex: `JOIN corporate_credit.counterparts c ON f.counterpart_id = c.counterpart_id`).\n"
        "4. Se for apenas conversa genérica ou saudação, responda normalmente em português.\n"
    )

    llm_messages = [{"role": "system", "content": system_prompt}]
    for msg in req.messages:
        llm_messages.append({"role": msg.role, "content": msg.content})

    start_time = time.perf_counter()
    duckdb_time_ms = 0.0
    sql_code = None
    query_results = None

    # 2. Query llama.cpp server
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                f"{LLAMA_SERVER_URL}/v1/chat/completions",
                json={
                    "model": LLM_MODEL,
                    "messages": llm_messages,
                    "temperature": req.temperature,
                    "stream": False
                }
            )
            if resp.status_code != 200:
                raise HTTPException(status_code=resp.status_code, detail=resp.text)
            llm_result = resp.json()
    except Exception as e:
        total_time_ms = round((time.perf_counter() - start_time) * 1000, 1)
        # Fallback se llama-server não estiver acessível
        return {
            "id": "chatcmpl-fallback",
            "object": "chat.completion",
            "created": 0,
            "model": req.model,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": f"[Middleware Fallback - LLM Offline] Contexto Semântico:\n{semantic_context}\n\nErro ao conectar ao LLM: {str(e)}",
                    "sql": None,
                    "data": None,
                    "execution_time_ms": total_time_ms,
                    "duckdb_time_ms": 0.0,
                    "row_count": 0
                },
                "finish_reason": "stop"
            }]
        }

    assistant_content = llm_result["choices"][0]["message"]["content"]

    # 3. Check if SQL was generated & Execute in DuckDB
    if "```sql" in assistant_content:
        try:
            sql_code = assistant_content.split("```sql")[1].split("```")[0].strip()
            t_duck = time.perf_counter()
            query_results = engine.execute_query(sql_code)
            duckdb_time_ms = round((time.perf_counter() - t_duck) * 1000, 1)
            results_formatted = json.dumps(query_results, indent=2, ensure_ascii=False)
            assistant_content += f"\n\n**Resultados Executados via DuckDB:**\n```json\n{results_formatted}\n```"
        except Exception as query_err:
            assistant_content += f"\n\n**Erro na execução no DuckDB:** {str(query_err)}"

    total_time_ms = round((time.perf_counter() - start_time) * 1000, 1)

    return {
        "id": llm_result.get("id", "chatcmpl-local"),
        "object": "chat.completion",
        "created": llm_result.get("created", 0),
        "model": req.model,
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": assistant_content,
                "sql": sql_code,
                "data": query_results,
                "execution_time_ms": total_time_ms,
                "duckdb_time_ms": duckdb_time_ms,
                "row_count": len(query_results) if query_results else 0
            },
            "finish_reason": "stop"
        }]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
