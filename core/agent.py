import os
import json
import time
import httpx
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
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

class Attachment(BaseModel):
    name: str
    size: Optional[int] = 0
    type: Optional[str] = "application/octet-stream"
    content: Optional[str] = None
    is_image: Optional[bool] = False

class ChatMessage(BaseModel):
    role: str
    content: str
    attachments: Optional[List[Attachment]] = None

class ChatCompletionRequest(BaseModel):
    model: Optional[str] = "llama3.2:3b"
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.2
    stream: Optional[bool] = False
    attachments: Optional[List[Attachment]] = None

@app.get("/", response_class=HTMLResponse)
def index_ui():
    """Interface Web Interativa de Chat para a Camada Semântica."""
    return """
    <!DOCTYPE html>
    <html lang="pt-BR" class="h-full">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Icepol</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
        <script>
            mermaid.initialize({
                startOnLoad: false,
                theme: 'dark',
                securityLevel: 'loose',
                suppressErrorRendering: true,
                themeVariables: {
                    darkMode: true,
                    background: '#020617',
                    primaryColor: '#1e293b',
                    primaryTextColor: '#f8fafc',
                    primaryBorderColor: '#38bdf8',
                    lineColor: '#7dd3fc',
                    secondaryColor: '#0f172a',
                    tertiaryColor: '#1e293b'
                }
            });
        </script>
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
            <div class="flex items-center gap-3 group cursor-pointer" onclick="window.location.reload()" title="Reiniciar chat / Voltar ao início">
                <!-- Polar Bear Vector Logo -->
                <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-sky-500/15 via-slate-800/60 to-slate-900 border border-sky-500/30 flex items-center justify-center shadow-lg shadow-sky-950/40 group-hover:border-sky-400/60 group-hover:shadow-sky-500/20 group-hover:scale-105 transition-all duration-300">
                    <svg width="24" height="24" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" class="transition-transform duration-300 group-hover:scale-105">
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
                        <!-- Bear Silhouette in Clean Line-art -->
                        <!-- Ear -->
                        <path d="M10 6 C10 4 12 3 14 4 C15 4.8 15 6 15 7" stroke="url(#iceBearGrad)" stroke-width="1.6" stroke-linecap="round" fill="rgba(56, 189, 248, 0.25)"/>
                        <!-- Snout & Profile -->
                        <path d="M15 7 L21 11 L28 14 L29 15.5 L26 17 L22 17" stroke="url(#iceBearGrad)" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round" fill="url(#iceBearFill)"/>
                        <!-- Jaw, Neck & Shoulder -->
                        <path d="M22 17 L20 21 L17 26 L12 26 L8 21 L8 14 L10 6" stroke="url(#iceBearGrad)" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round" fill="url(#iceBearFill)"/>
                        <!-- Internal Facets / Ice Polygon Lines -->
                        <path d="M15 7 L17 14 L28 14" stroke="url(#iceBearGrad)" stroke-width="1.2" stroke-linejoin="round" stroke-opacity="0.8"/>
                        <path d="M17 14 L22 17" stroke="url(#iceBearGrad)" stroke-width="1.2" stroke-linejoin="round" stroke-opacity="0.75"/>
                        <path d="M17 14 L14 20 L20 21" stroke="url(#iceBearGrad)" stroke-width="1.2" stroke-linejoin="round" stroke-opacity="0.65"/>
                        <path d="M8 14 L17 14" stroke="url(#iceBearGrad)" stroke-width="1.1" stroke-linejoin="round" stroke-opacity="0.5"/>
                        <path d="M14 20 L12 26" stroke="url(#iceBearGrad)" stroke-width="1.1" stroke-linejoin="round" stroke-opacity="0.5"/>
                        <!-- Eye & Spark -->
                        <circle cx="19.5" cy="12.5" r="1.1" fill="#ffffff"/>
                        <circle cx="28.5" cy="14.8" r="0.8" fill="#7dd3fc"/>
                    </svg>
                </div>
                <span class="text-xl font-bold tracking-tight text-white font-mono group-hover:text-sky-200 transition-colors">Icepol</span>
            </div>
            <div class="flex items-center space-x-2.5 text-xs">
                <!-- Interactive LLM Badge & Popover -->
                <div class="relative">
                    <button type="button" id="header-llm-btn" onclick="toggleHeaderLlmPopover(event)" 
                        class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full font-medium bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/20 hover:border-emerald-500/40 transition cursor-pointer shadow-sm group"
                        title="Configurações e status do Modelo LLM">
                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                        <span>LLM: <strong id="header-llm-label" class="font-semibold text-emerald-300">llama3.2:3b</strong> <span class="opacity-75">(Ollama)</span></span>
                        <svg class="w-3 h-3 text-emerald-400/80 group-hover:translate-y-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                        </svg>
                    </button>

                    <!-- LLM Popover Menu -->
                    <div id="header-llm-popover" class="hidden absolute top-full right-0 mt-2.5 w-72 bg-slate-900/95 border border-slate-700/80 rounded-2xl shadow-2xl p-4 z-50 backdrop-blur-xl space-y-3">
                        <div class="flex items-center justify-between pb-2.5 border-b border-slate-800">
                            <div class="flex items-center gap-2">
                                <div class="w-6 h-6 rounded-lg bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
                                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                                </div>
                                <span class="font-semibold text-white text-xs">Ollama Model Central</span>
                            </div>
                            <span id="popover-llm-status-badge" class="inline-flex items-center gap-1 text-[10px] text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
                                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                                Conectado
                            </span>
                        </div>

                        <!-- Active Model Switcher -->
                        <div class="space-y-1.5">
                            <div class="flex justify-between items-center text-[10px] font-mono text-slate-400 uppercase tracking-wider">
                                <span>Modelos Disponíveis</span>
                                <span class="text-emerald-400">Ollama API</span>
                            </div>
                            <div id="popover-model-list" class="space-y-1 max-h-36 overflow-y-auto">
                                <!-- Populated dynamically -->
                            </div>
                        </div>

                        <!-- Technical Specs -->
                        <div class="bg-slate-950/70 rounded-xl p-2.5 border border-slate-800/80 space-y-1.5 text-[11px]">
                            <div class="flex justify-between text-slate-400">
                                <span>Provedor:</span>
                                <span class="text-slate-200 font-mono">Ollama Local</span>
                            </div>
                            <div class="flex justify-between text-slate-400">
                                <span>Temperatura:</span>
                                <span class="text-slate-200 font-mono">0.2 (SQL Exato)</span>
                            </div>
                            <div class="flex justify-between text-slate-400">
                                <span>Latência do Engine:</span>
                                <span id="popover-llm-latency" class="text-emerald-400 font-mono">Pronto</span>
                            </div>
                        </div>

                        <!-- Ping Test Button -->
                        <button type="button" onclick="testLlmPing()" class="w-full py-2 bg-emerald-500/15 hover:bg-emerald-500/25 text-emerald-300 border border-emerald-500/30 rounded-xl text-xs font-medium transition flex items-center justify-center gap-1.5 cursor-pointer">
                            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
                            <span>Testar Latência do LLM</span>
                        </button>
                    </div>
                </div>

                <!-- Interactive DuckDB Badge & Popover -->
                <div class="relative">
                    <button type="button" id="header-duckdb-btn" onclick="toggleHeaderDuckDbPopover(event)" 
                        class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full font-medium bg-blue-500/10 hover:bg-blue-500/20 text-blue-400 border border-blue-500/20 hover:border-blue-500/40 transition cursor-pointer shadow-sm group"
                        title="Status e Metadados do DuckDB Lakehouse">
                        <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
                        <span>DuckDB Engine: <strong class="font-semibold text-blue-300">Ativo</strong></span>
                        <svg class="w-3 h-3 text-blue-400/80 group-hover:translate-y-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                        </svg>
                    </button>

                    <!-- DuckDB Popover Menu -->
                    <div id="header-duckdb-popover" class="hidden absolute top-full right-0 mt-2.5 w-80 bg-slate-900/95 border border-slate-700/80 rounded-2xl shadow-2xl p-4 z-50 backdrop-blur-xl space-y-3">
                        <div class="flex items-center justify-between pb-2.5 border-b border-slate-800">
                            <div class="flex items-center gap-2">
                                <div class="w-6 h-6 rounded-lg bg-blue-500/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
                                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2 1.5 3 3.5 3h9c2 0 3.5-1 3.5-3V7M4 7c0-2 1.5-3 3.5-3h9c2 0 3.5 1 3.5 3M4 7h16m-16 5h16"/></svg>
                                </div>
                                <span class="font-semibold text-white text-xs">DuckDB Lakehouse</span>
                            </div>
                            <span id="popover-duckdb-status-badge" class="inline-flex items-center gap-1 text-[10px] text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded-full border border-blue-500/20">
                                <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
                                In-Memory Ativo
                            </span>
                        </div>

                        <!-- Architecture Info -->
                        <div class="bg-slate-950/70 rounded-xl p-2.5 border border-slate-800/80 space-y-1.5 text-[11px]">
                            <div class="flex justify-between text-slate-400">
                                <span>Schema Canônico:</span>
                                <span class="text-blue-300 font-mono font-semibold">corporate_credit</span>
                            </div>
                            <div class="flex justify-between text-slate-400">
                                <span>Catálogo Metastore:</span>
                                <span class="text-slate-200">Polaris Iceberg REST</span>
                            </div>
                            <div class="flex justify-between text-slate-400">
                                <span>Armazenamento:</span>
                                <span class="text-slate-200 font-mono">MinIO S3</span>
                            </div>
                            <div class="flex justify-between text-slate-400">
                                <span>Tempo de Execução:</span>
                                <span id="popover-duckdb-latency" class="text-blue-400 font-mono">⚡ 1.2ms</span>
                            </div>
                        </div>

                        <!-- Interactive Tables (Click to Query) -->
                        <div class="space-y-1.5">
                            <div class="flex items-center justify-between">
                                <span class="text-[10px] font-mono font-semibold text-slate-400 uppercase tracking-wider">Tabelas (Clique p/ consultar)</span>
                                <span id="popover-tables-count" class="text-[10px] text-slate-400 font-mono">--</span>
                            </div>
                            <div id="popover-tables-list" class="flex flex-wrap gap-1.5 max-h-32 overflow-y-auto pt-0.5">
                                <span class="text-xs text-slate-500">Carregando tabelas...</span>
                            </div>
                        </div>

                        <!-- Quick Actions -->
                        <div class="grid grid-cols-2 gap-2 pt-1">
                            <button type="button" onclick="testDuckDbPing()" class="py-2 px-2 bg-blue-500/15 hover:bg-blue-500/25 text-blue-300 border border-blue-500/30 rounded-xl text-[11px] font-medium transition flex items-center justify-center gap-1 cursor-pointer">
                                <span>⚡ Testar Engine</span>
                            </button>
                            <button type="button" onclick="sendPrompt('SHOW TABLES FROM corporate_credit;'); closeAllPopovers();" class="py-2 px-2 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-xl text-[11px] font-medium transition flex items-center justify-center gap-1 cursor-pointer">
                                <span>Listar Tabelas →</span>
                            </button>
                        </div>
                    </div>
                </div>
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
                            Como posso ajudar com sua pesquisa hoje?
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
                        <button onclick="sendPrompt('Mostre o diagrama de modelo das entidades (ERD) e relacionamentos de crédito')" 
                            class="px-4 py-2.5 rounded-full bg-[#1e1f20] hover:bg-[#282a2c] text-sky-300 hover:text-white border border-sky-600/50 transition text-xs md:text-sm font-medium shadow-sm flex items-center gap-1.5">
                            <span>📊 Diagrama de Entidades (Mermaid)</span>
                        </button>
                    </div>
                </div>
            </div>
        </main>

        <!-- Gemini Pill Floating Footer Input -->
        <footer class="px-4 md:px-8 py-5 sticky bottom-0 z-20">
            <div class="max-w-4xl mx-auto">
                <!-- Hidden file input for images & documents -->
                <input type="file" id="file-input" multiple accept="image/*,.pdf,.csv,.json,.txt,.parquet,.sql,.xlsx,.doc,.docx" class="hidden" onchange="handleFileSelect(event)">

                <form id="chat-form" onsubmit="handleSubmit(event)" class="relative flex flex-col bg-[#1e1f20] hover:bg-[#26282c] focus-within:bg-[#1e1f20] border border-slate-700/70 focus-within:border-slate-500 rounded-3xl px-3.5 py-2 md:py-2.5 shadow-2xl transition-all duration-200">
                    
                    <!-- Attachment Previews Badge Bar -->
                    <div id="attachments-bar" class="hidden w-full px-2 py-1.5 mb-1.5 border-b border-slate-700/50 flex flex-wrap gap-2 items-center"></div>

                    <div class="flex items-center w-full">
                        <!-- Left + Button (Files / Images / Tools) -->
                        <button type="button" onclick="document.getElementById('file-input').click()" 
                            class="w-9 h-9 rounded-full flex items-center justify-center text-slate-300 hover:text-white hover:bg-white/10 transition shrink-0" 
                            title="Anexar arquivos ou imagens para ajudar na pesquisa">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                            </svg>
                        </button>

                        <!-- Text input with dynamic 'Peça ao <modelo>' placeholder -->
                        <input id="user-input" type="text" placeholder="Peça ao llama3.2:3b" 
                            class="flex-1 bg-transparent border-0 text-white placeholder-slate-400 text-sm md:text-base focus:ring-0 focus:outline-none px-3 font-sans">

                        <!-- Right Items: Model Selector Dropdown, Microphone & Send -->
                        <div class="flex items-center space-x-1.5 shrink-0 pr-1">
                            
                            <!-- Model badge dropdown -->
                            <div class="relative">
                                <button type="button" id="model-dropdown-btn" onclick="toggleModelDropdown(event)" 
                                    class="flex items-center gap-1.5 text-xs text-slate-300 hover:text-white px-3 py-1.5 rounded-full hover:bg-white/10 transition cursor-pointer font-sans" 
                                    title="Selecionar modelo de IA disponível">
                                    <span id="selected-model-label">llama3.2:3b</span>
                                    <svg class="w-3.5 h-3.5 text-slate-400 transition-transform duration-200" id="model-chevron" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                                    </svg>
                                </button>
                                
                                <!-- Floating Dropdown Menu -->
                                <div id="model-dropdown-menu" class="hidden absolute bottom-full mb-2 right-0 w-52 bg-slate-900 border border-slate-700/80 rounded-2xl shadow-2xl py-1.5 z-50 backdrop-blur-md">
                                    <div class="px-3 py-1.5 text-[10px] font-mono font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-800 flex items-center justify-between">
                                        <span>Modelos Ollama</span>
                                        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                                    </div>
                                    <div id="model-list" class="max-h-52 overflow-y-auto py-1">
                                        <!-- Dynamically populated -->
                                    </div>
                                </div>
                            </div>

                            <!-- Microphone Voice Input Button -->
                            <button type="button" id="mic-btn" onclick="toggleSpeechRecognition()" 
                                class="w-9 h-9 rounded-full flex items-center justify-center text-slate-300 hover:text-white hover:bg-white/10 transition shrink-0" 
                                title="Escutar áudio para pesquisa">
                                <svg id="mic-icon" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 02-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/>
                                </svg>
                            </button>

                            <!-- Send button -->
                            <button type="submit" id="send-btn" 
                                class="w-9 h-9 rounded-full bg-white hover:bg-slate-200 text-slate-900 flex items-center justify-center transition shadow shrink-0" 
                                title="Enviar consulta">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 12h14M12 5l7 7-7 7"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </footer>

        <script>
            const chatBox = document.getElementById('chat-box');
            const userInput = document.getElementById('user-input');
            const sendBtn = document.getElementById('send-btn');
            const attachmentsBar = document.getElementById('attachments-bar');
            const selectedModelLabel = document.getElementById('selected-model-label');
            const headerLlmLabel = document.getElementById('header-llm-label');
            const modelDropdownMenu = document.getElementById('model-dropdown-menu');
            const modelListEl = document.getElementById('model-list');
            const micBtn = document.getElementById('mic-btn');

            const messages = [];
            let attachedFiles = [];
            let cellCounter = 0;
            let currentModel = 'llama3.2:3b';
            let availableModels = ['llama3.2:3b', 'llama3.2:1b'];
            let recognition = null;
            let isRecording = false;
            let speechBaseText = '';

            // --- MODEL MANAGEMENT ---
            async function loadAvailableModels() {
                try {
                    const res = await fetch('/api/models');
                    const data = await res.json();
                    if (data.models && data.models.length > 0) {
                        availableModels = data.models;
                        currentModel = data.default || data.models[0];
                        renderModelList(availableModels);
                        updateModelUI(currentModel);
                    }
                } catch (err) {
                    console.warn('Erro ao carregar modelos:', err);
                    renderModelList(availableModels);
                }
            }

            function renderModelList(models) {
                modelListEl.innerHTML = models.map(m => `
                    <button type="button" onclick="selectModel('${m}')" 
                        class="w-full text-left px-3 py-2 text-xs text-slate-300 hover:text-white hover:bg-slate-800/80 rounded-xl transition flex items-center justify-between font-mono">
                        <span class="truncate">${m}</span>
                        ${m === currentModel ? '<span class="text-emerald-400 font-bold ml-2">✓</span>' : ''}
                    </button>
                `).join('');
                renderPopoverModelList(models);
            }

            function toggleModelDropdown(e) {
                e.stopPropagation();
                modelDropdownMenu.classList.toggle('hidden');
                document.getElementById('model-chevron')?.classList.toggle('rotate-180');
            }

            function selectModel(modelName) {
                currentModel = modelName;
                updateModelUI(modelName);
                closeAllPopovers();
                renderModelList(availableModels);
            }

            function updateModelUI(modelName) {
                selectedModelLabel.innerText = modelName;
                if (headerLlmLabel) headerLlmLabel.innerText = modelName;
                userInput.placeholder = `Peça ao ${modelName}`;
            }

            // --- HEADER INTERACTIVE POPOVERS ---
            function toggleHeaderLlmPopover(e) {
                e.stopPropagation();
                const popover = document.getElementById('header-llm-popover');
                const isHidden = popover.classList.contains('hidden');
                closeAllPopovers();
                if (isHidden) {
                    popover.classList.remove('hidden');
                    renderPopoverModelList(availableModels);
                    testLlmPing();
                }
            }

            function toggleHeaderDuckDbPopover(e) {
                e.stopPropagation();
                const popover = document.getElementById('header-duckdb-popover');
                const isHidden = popover.classList.contains('hidden');
                closeAllPopovers();
                if (isHidden) {
                    popover.classList.remove('hidden');
                    loadDuckDbStatus();
                }
            }

            function closeAllPopovers() {
                document.getElementById('header-llm-popover')?.classList.add('hidden');
                document.getElementById('header-duckdb-popover')?.classList.add('hidden');
                document.getElementById('model-dropdown-menu')?.classList.add('hidden');
                document.getElementById('model-chevron')?.classList.remove('rotate-180');
            }

            function renderPopoverModelList(models) {
                const listEl = document.getElementById('popover-model-list');
                if (!listEl) return;
                listEl.innerHTML = models.map(m => `
                    <button type="button" onclick="selectModel('${m}'); closeAllPopovers();" 
                        class="w-full text-left px-2.5 py-1.5 text-xs rounded-xl transition flex items-center justify-between font-mono cursor-pointer ${m === currentModel ? 'bg-emerald-500/20 text-emerald-300 font-semibold border border-emerald-500/30' : 'text-slate-300 hover:text-white hover:bg-slate-800/80'}">
                        <span class="truncate">${m}</span>
                        ${m === currentModel ? '<span class="text-emerald-400 font-bold ml-1.5 text-xs">✓ Ativo</span>' : ''}
                    </button>
                `).join('');
            }

            async function testLlmPing() {
                const latencyEl = document.getElementById('popover-llm-latency');
                const badgeEl = document.getElementById('popover-llm-status-badge');
                if (latencyEl) latencyEl.innerText = 'Medindo...';
                try {
                    const res = await fetch('/api/llm/ping');
                    const data = await res.json();
                    if (data.status === 'online') {
                        if (latencyEl) latencyEl.innerText = `⚡ ${data.latency_ms}ms (OK)`;
                        if (badgeEl) badgeEl.innerHTML = '<span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span> Conectado';
                    } else {
                        if (latencyEl) latencyEl.innerText = 'Offline';
                        if (badgeEl) badgeEl.innerHTML = '<span class="w-1.5 h-1.5 rounded-full bg-red-400"></span> Desconectado';
                    }
                } catch (err) {
                    if (latencyEl) latencyEl.innerText = 'Erro';
                }
            }

            async function loadDuckDbStatus() {
                const latencyEl = document.getElementById('popover-duckdb-latency');
                const countEl = document.getElementById('popover-tables-count');
                const listEl = document.getElementById('popover-tables-list');
                try {
                    const res = await fetch('/api/engine/status');
                    const data = await res.json();
                    if (latencyEl) latencyEl.innerText = `⚡ ${data.ping_ms}ms (OK)`;
                    if (countEl) countEl.innerText = `${data.table_count} tabelas`;
                    if (listEl && data.tables) {
                        listEl.innerHTML = data.tables.map(t => `
                            <button type="button" onclick="insertSampleQuery('${t}')" 
                                title="Clique para consultar a tabela ${t}"
                                class="px-2 py-1 bg-slate-800/80 hover:bg-blue-600/30 text-slate-300 hover:text-blue-200 rounded-lg text-[11px] font-mono border border-slate-700/60 hover:border-blue-400/40 transition cursor-pointer">
                                ${t}
                            </button>
                        `).join('');
                    }
                } catch (err) {
                    console.warn('Erro ao carregar status do DuckDB:', err);
                }
            }

            async function testDuckDbPing() {
                const latencyEl = document.getElementById('popover-duckdb-latency');
                if (latencyEl) latencyEl.innerText = 'Medindo...';
                await loadDuckDbStatus();
            }

            function insertSampleQuery(tableName) {
                userInput.value = `Qual a estrutura e dados da tabela corporate_credit.${tableName}?`;
                closeAllPopovers();
                userInput.focus();
            }

            // Close dropdowns and popovers when clicking outside
            document.addEventListener('click', (e) => {
                if (!document.getElementById('header-llm-popover')?.contains(e.target) && !document.getElementById('header-llm-btn')?.contains(e.target)) {
                    document.getElementById('header-llm-popover')?.classList.add('hidden');
                }
                if (!document.getElementById('header-duckdb-popover')?.contains(e.target) && !document.getElementById('header-duckdb-btn')?.contains(e.target)) {
                    document.getElementById('header-duckdb-popover')?.classList.add('hidden');
                }
                if (!modelDropdownMenu.contains(e.target) && !document.getElementById('model-dropdown-btn')?.contains(e.target)) {
                    modelDropdownMenu.classList.add('hidden');
                    document.getElementById('model-chevron')?.classList.remove('rotate-180');
                }
            });

            // --- FILE & IMAGE ATTACHMENTS VIA /api/upload ---
            function formatSize(bytes) {
                if (!bytes || bytes === 0) return '0 B';
                const k = 1024;
                const sizes = ['B', 'KB', 'MB', 'GB'];
                const i = Math.floor(Math.log(bytes) / Math.log(k));
                return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
            }

            async function handleFileSelect(e) {
                const files = Array.from(e.target.files || []);
                if (!files.length) return;

                for (const file of files) {
                    const isImg = file.type.startsWith('image/');
                    const previewUrl = isImg ? URL.createObjectURL(file) : null;
                    const tempId = 'att-' + Date.now() + '-' + Math.random().toString(36).substr(2, 5);

                    const attItem = {
                        id: tempId,
                        name: file.name,
                        size: file.size,
                        type: file.type || 'application/octet-stream',
                        is_image: isImg,
                        previewUrl: previewUrl,
                        content: null,
                        uploading: true
                    };
                    attachedFiles.push(attItem);
                    renderAttachmentPreviews();

                    const formData = new FormData();
                    formData.append('file', file);

                    try {
                        const res = await fetch('/api/upload', {
                            method: 'POST',
                            body: formData
                        });
                        if (res.ok) {
                            const data = await res.json();
                            const item = attachedFiles.find(a => a.id === tempId);
                            if (item) {
                                item.content = data.content;
                                item.type = data.type || item.type;
                                item.is_image = data.is_image;
                                item.uploading = false;
                                renderAttachmentPreviews();
                            }
                        } else {
                            throw new Error('Upload error: ' + res.status);
                        }
                    } catch (err) {
                        console.warn('Fallback leitura local para arquivo:', file.name, err);
                        const item = attachedFiles.find(a => a.id === tempId);
                        if (item) {
                            item.uploading = false;
                            renderAttachmentPreviews();
                        }
                    }
                }

                e.target.value = ''; // Reset input
            }

            function removeAttachment(index) {
                const removed = attachedFiles.splice(index, 1)[0];
                if (removed && removed.previewUrl && removed.previewUrl.startsWith('blob:')) {
                    URL.revokeObjectURL(removed.previewUrl);
                }
                renderAttachmentPreviews();
            }

            function renderAttachmentPreviews() {
                if (!attachedFiles.length) {
                    attachmentsBar.classList.add('hidden');
                    attachmentsBar.innerHTML = '';
                    return;
                }

                attachmentsBar.classList.remove('hidden');
                attachmentsBar.innerHTML = attachedFiles.map((att, idx) => {
                    const spinner = att.uploading ? `
                        <svg class="w-3.5 h-3.5 animate-spin text-blue-400 shrink-0" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                        </svg>` : '';
                    if (att.is_image) {
                        return `
                            <div class="flex items-center gap-2 bg-slate-800/90 text-slate-200 px-2.5 py-1.5 rounded-xl text-xs border border-slate-700/80 shadow-sm">
                                ${att.previewUrl ? `<img src="${att.previewUrl}" class="w-6 h-6 rounded-md object-cover border border-slate-600">` : ''}
                                ${spinner}
                                <span class="max-w-[130px] truncate font-medium">${att.name}</span>
                                <span class="text-slate-400 text-[10px]">${formatSize(att.size)}</span>
                                <button type="button" onclick="removeAttachment(${idx})" class="text-slate-400 hover:text-rose-400 ml-1 transition" title="Remover">
                                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                                </button>
                            </div>
                        `;
                    } else {
                        return `
                            <div class="flex items-center gap-2 bg-slate-800/90 text-slate-200 px-2.5 py-1.5 rounded-xl text-xs border border-slate-700/80 shadow-sm">
                                <svg class="w-4 h-4 text-blue-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
                                </svg>
                                ${spinner}
                                <span class="max-w-[130px] truncate font-medium">${att.name}</span>
                                <span class="text-slate-400 text-[10px]">${formatSize(att.size)}</span>
                                <button type="button" onclick="removeAttachment(${idx})" class="text-slate-400 hover:text-rose-400 ml-1 transition" title="Remover">
                                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                                </button>
                            </div>
                        `;
                    }
                }).join('');
            }

            // --- SPEECH RECOGNITION (AUDIO / MIC) ---
            function toggleSpeechRecognition() {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!SpeechRecognition) {
                    alert('Reconhecimento de voz não é suportado pelo seu navegador atual. Recomendamos o Google Chrome ou Microsoft Edge.');
                    return;
                }

                if (!recognition) {
                    recognition = new SpeechRecognition();
                    recognition.lang = 'pt-BR';
                    recognition.continuous = true;
                    recognition.interimResults = true;

                    recognition.onstart = () => {
                        isRecording = true;
                        speechBaseText = userInput.value ? userInput.value.trim() + ' ' : '';
                        updateMicUi(true);
                    };

                    recognition.onresult = (event) => {
                        let finalTranscript = '';
                        let interimTranscript = '';
                        for (let i = 0; i < event.results.length; ++i) {
                            if (event.results[i].isFinal) {
                                finalTranscript += event.results[i][0].transcript;
                            } else {
                                interimTranscript += event.results[i][0].transcript;
                            }
                        }
                        const combinedSpeech = (finalTranscript + (interimTranscript ? ' ' + interimTranscript : '')).trim();
                        if (combinedSpeech) {
                            userInput.value = speechBaseText + combinedSpeech;
                        }
                    };

                    recognition.onerror = (event) => {
                        console.warn('Speech recognition status:', event.error);
                        if (event.error === 'not-allowed') {
                            alert('Permissão de microfone negada. Por favor, permita o acesso ao microfone nas configurações do seu navegador.');
                        }
                        if (event.error !== 'no-speech') {
                            isRecording = false;
                            updateMicUi(false);
                        }
                    };

                    recognition.onend = () => {
                        isRecording = false;
                        updateMicUi(false);
                    };
                }

                if (isRecording) {
                    recognition.stop();
                } else {
                    try {
                        speechBaseText = userInput.value ? userInput.value.trim() + ' ' : '';
                        recognition.start();
                    } catch (err) {
                        console.error('Falha ao iniciar reconhecimento de áudio:', err);
                    }
                }
            }

            function updateMicUi(recording) {
                if (recording) {
                    micBtn.className = 'w-9 h-9 rounded-full bg-red-500/20 text-red-400 ring-2 ring-red-500/50 flex items-center justify-center transition shrink-0 animate-pulse';
                    userInput.placeholder = 'Ouvindo áudio... Fale sua pesquisa agora';
                } else {
                    micBtn.className = 'w-9 h-9 rounded-full flex items-center justify-center text-slate-300 hover:text-white hover:bg-white/10 transition shrink-0';
                    userInput.placeholder = `Peça ao ${currentModel}`;
                }
            }

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

            function appendUserMessage(content, sentAttachments = [], modelUsed = null) {
                const wrapper = document.createElement('div');
                wrapper.className = 'flex flex-col items-end pt-2';
                
                if (modelUsed) {
                    const modelTag = document.createElement('div');
                    modelTag.className = 'text-[11px] font-mono text-slate-400 mb-1 mr-2 flex items-center gap-1';
                    modelTag.innerHTML = `<span>Peça ao</span> <span class="text-indigo-300 font-semibold">${modelUsed}</span>`;
                    wrapper.appendChild(modelTag);
                }

                const bubble = document.createElement('div');
                bubble.className = 'bg-blue-600 text-white rounded-3xl rounded-tr-sm px-6 py-4 max-w-2xl text-sm shadow-md leading-relaxed';
                
                let html = `<div>${content}</div>`;
                if (sentAttachments && sentAttachments.length > 0) {
                    html += `<div class="mt-3 pt-2.5 border-t border-blue-500/40 flex flex-wrap gap-2">`;
                    sentAttachments.forEach(att => {
                        if (att.is_image) {
                            html += `
                                <div class="space-y-1">
                                    <img src="${att.previewUrl || att.content}" class="max-h-40 max-w-xs rounded-xl border border-blue-400/40 object-cover shadow-sm">
                                    <span class="text-[10px] text-blue-200 block truncate max-w-[160px]">${att.name}</span>
                                </div>
                            `;
                        } else {
                            html += `
                                <div class="inline-flex items-center gap-1.5 bg-blue-700/70 border border-blue-400/40 px-3 py-1.5 rounded-xl text-xs">
                                    <svg class="w-3.5 h-3.5 text-blue-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"/>
                                    </svg>
                                    <span class="font-medium">${att.name}</span>
                                    <span class="text-blue-200 text-[10px]">(${formatSize(att.size)})</span>
                                </div>
                            `;
                        }
                    });
                    html += `</div>`;
                }

                bubble.innerHTML = html;
                wrapper.appendChild(bubble);
                chatBox.appendChild(wrapper);
                chatBox.scrollIntoView({ behavior: 'smooth', block: 'end' });
            }

            function showProcessingStepper(modelUsed) {
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
                                Pesquisa Analítica [In ${cellCounter + 1}]
                            </span>
                        </div>
                        <span class="text-xs text-slate-400 font-mono" id="stepper-time">0.0s</span>
                    </div>
                    <div class="space-y-2.5 text-xs text-slate-300 font-mono">
                        <div id="step-1" class="flex items-center gap-2.5 text-blue-300">
                            <span class="w-2 h-2 rounded-full bg-blue-400 animate-pulse"></span>
                            <span>Mapeando ontologias & contexto da pesquisa...</span>
                        </div>
                        <div id="step-2" class="flex items-center gap-2.5 text-slate-500">
                            <span class="w-2 h-2 rounded-full bg-slate-700"></span>
                            <span>Compilando consulta analítica via Ollama (${modelUsed})...</span>
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

            function sanitizeMermaidCode(raw) {
                if (!raw) return "";
                const nl = String.fromCharCode(10);
                let code = raw.trim();
                code = code.replace(/^```(?:mermaid)?/i, "").replace(/```$/, "").trim();

                // Check if ER diagram
                if (/erDiagram/i.test(code)) {
                    let lines = code.split(nl);
                    let insideEntity = false;
                    let sanitizedLines = ["erDiagram"];
                    const knownTypes = new Set([
                        "string", "str", "varchar", "text", "int", "integer", "bigint", "float", 
                        "double", "number", "numeric", "decimal", "date", "datetime", "timestamp", 
                        "boolean", "bool", "uuid"
                    ]);

                    for (let i = 0; i < lines.length; i++) {
                        let line = lines[i];
                        let trimmed = line.trim();
                        if (!trimmed) continue;
                        if (/^[\\s]*erDiagram/i.test(trimmed)) continue;

                        // Comments
                        if (trimmed.startsWith("#") || trimmed.startsWith("//")) {
                            sanitizedLines.push("    %% " + trimmed.replace(/^[#/]+[\\s]*/, ""));
                            continue;
                        }

                        // Relationship line check
                        const isRel = /(?:\\|\\|--[o|]\\{|--|->|-->|\\|\\|--\\|\\||\\}\\|--\\|\\{|\\}\\|--o\\{|\\}o--o\\{|\\}o--\\|\\||\\*--\\*|<-->|<--)/.test(trimmed);

                        // Entity start: e.g. counterparts { or entity counterparts { (must not be a relationship)
                        if (!isRel && /\\{[\\s]*$/.test(trimmed)) {
                            insideEntity = true;
                            let entName = trimmed.replace(/PART[\\s]+OF[\\s]+/gi, "").replace(/["'{}]/g, "").trim().split(/[\\s]+/)[0];
                            if (entName) {
                                sanitizedLines.push(`    ${entName} {`);
                            }
                            continue;
                        }

                        // Entity end
                        if (!isRel && (trimmed === "}" || trimmed.endsWith("}"))) {
                            insideEntity = false;
                            sanitizedLines.push("    }");
                            continue;
                        }

                        if (insideEntity) {
                            // Split line if multiple attributes (e.g. separated by commas, semicolons, or multiple '=' assignments)
                            let subAttributes = trimmed.split(/[\\s]+(?=[a-zA-Z0-9_]+[\\s]*=)|[,;]+/);
                            for (let subAttr of subAttributes) {
                                let item = subAttr.trim();
                                if (!item) continue;

                                // Clean quotes and symbols
                                let clean = item.replace(/[=:'"]/g, " ").replace(/[\\s]+/g, " ").trim();
                                let parts = clean.split(" ").filter(p => p.length > 0);
                                if (parts.length === 0) continue;

                                let type = "string";
                                let col = "";
                                let key = "";

                                let filtered = [];
                                for (let p of parts) {
                                    let up = p.toUpperCase();
                                    if (up === "PK" || up === "FK" || up === "UK") {
                                        key = up;
                                    } else {
                                        filtered.push(p);
                                    }
                                }

                                if (filtered.length === 1) {
                                    col = filtered[0].replace(/[^a-zA-Z0-9_]/g, "");
                                } else if (filtered.length >= 2) {
                                    let p0Low = filtered[0].toLowerCase();
                                    let p1Low = filtered[1].toLowerCase();
                                    if (knownTypes.has(p0Low)) {
                                        type = p0Low;
                                        col = filtered[1].replace(/[^a-zA-Z0-9_]/g, "");
                                    } else if (knownTypes.has(p1Low)) {
                                        type = p1Low;
                                        col = filtered[0].replace(/[^a-zA-Z0-9_]/g, "");
                                    } else {
                                        if (p0Low.includes("_") || p0Low.endsWith("id") || p0Low.startsWith("nm_") || p0Low.startsWith("dt_") || p0Low.startsWith("vl_")) {
                                            col = filtered[0].replace(/[^a-zA-Z0-9_]/g, "");
                                            type = (p1Low === "id" || p1Low === "key") ? "string" : (p1Low.length <= 8 ? p1Low : "string");
                                        } else {
                                            type = p0Low.length <= 8 ? p0Low : "string";
                                            col = filtered[1].replace(/[^a-zA-Z0-9_]/g, "");
                                        }
                                    }
                                }

                                if (col) {
                                    sanitizedLines.push(`        ${type} ${col}${key ? " " + key : ""}`);
                                }
                            }
                        } else {
                            // Relationship line outside entity
                            let cleanRel = trimmed.replace(/PART[\\s]+OF[\\s]+/gi, "").replace(/["']/g, "");
                            cleanRel = cleanRel.replaceAll("*--*", "}|--|{")
                                               .replaceAll("<-->", "}|--|{")
                                               .replaceAll("-->", "||--o{")
                                               .replaceAll("<--", "}o--||");

                            if (/(?:\\|\\|--[o|]\\{|--|\\|\\|--\\|\\||\\}\\|--\\|\\{|\\}\\|--o\\{|\\}o--o\\{|\\}o--\\|\\|)/.test(cleanRel)) {
                                if (!cleanRel.includes(":")) {
                                    cleanRel += ' : "relaciona"';
                                } else {
                                    let parts = cleanRel.split(":");
                                    let relPart = parts[0].trim();
                                    let labelPart = parts.slice(1).join(":").trim().replace(/^["']|["']$/g, "");
                                    cleanRel = `${relPart} : "${labelPart || "relaciona"}"`;
                                }
                                sanitizedLines.push("    " + cleanRel);
                            }
                        }
                    }
                    return sanitizedLines.join(nl);
                }

                return code;
            }

            function fallbackToGraph(code) {
                const nl = String.fromCharCode(10);
                const lines = code.split(nl);
                const nodes = new Set();
                const edges = [];
                let inEntity = false;

                for (const l of lines) {
                    const trimmed = l.trim();
                    if (!trimmed) continue;

                    // Match relationships e.g. A ||--o{ B : "label" or A --> B
                    const match = trimmed.match(/^([a-zA-Z0-9_]+)[\\s]*(?:\\|\\|--[o|]\\{|--|->|-->|\\|\\|--\\|\\||\\}\\|--\\|\\{|\\}\\|--o\\{|\\}o--o\\{|\\}o--\\|\\|)[\\s]*([a-zA-Z0-9_]+)(?:[\\s]*:[\\s]*"?([^"]*)"?)?/);
                    if (match) {
                        nodes.add(match[1]);
                        nodes.add(match[2]);
                        const label = match[3] ? `|"${match[3].trim()}"| ` : '';
                        edges.push(`    ${match[1]} --> ${label}${match[2]}`);
                        continue;
                    }

                    if (trimmed.endsWith("{")) {
                        inEntity = true;
                        const entMatch = trimmed.match(/^([a-zA-Z0-9_]+)[\\s]*\\{/);
                        if (entMatch && !["erdiagram", "graph", "flowchart", "classdiagram"].includes(entMatch[1].toLowerCase())) {
                            nodes.add(entMatch[1]);
                        }
                        continue;
                    }

                    if (trimmed === "}") {
                        inEntity = false;
                        continue;
                    }
                }
                if (nodes.size > 0) {
                    return ["graph TD", ...Array.from(nodes).map(n => `    ${n}["${n}"]`), ...(edges.length ? edges : [])].join(nl);
                }
                return null;
            }

            function renderMarkdownWithMermaid(content) {
                if (!content) return '';
                const rawHtml = marked.parse(content);
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = rawHtml;
                
                tempDiv.querySelectorAll('pre code.language-mermaid').forEach((codeBlock) => {
                    const mermaidCode = codeBlock.textContent.trim();
                    const container = document.createElement('div');
                    container.className = 'mermaid-diagram-card my-4 p-4 rounded-2xl bg-[#090d16] border border-slate-700/80 shadow-2xl overflow-x-auto flex flex-col items-center';
                    
                    const header = document.createElement('div');
                    header.className = 'w-full flex items-center justify-between pb-2 mb-3 border-b border-slate-800 text-xs text-slate-400 font-mono';
                    header.innerHTML = `
                        <span class="flex items-center gap-1.5 text-sky-400 font-semibold">
                            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"/></svg>
                            Diagrama Visual Mermaid
                        </span>
                        <span class="text-[10px] text-slate-500 uppercase font-mono tracking-wider">Modelo Conceitual</span>
                    `;
                    
                    const diagramEl = document.createElement('div');
                    diagramEl.className = 'mermaid-diagram-code w-full flex justify-center py-2';
                    diagramEl.setAttribute('data-mermaid-code', encodeURIComponent(mermaidCode));
                    diagramEl.innerHTML = '<span class="text-xs text-slate-500 animate-pulse font-mono">Renderizando diagrama...</span>';
                    
                    container.appendChild(header);
                    container.appendChild(diagramEl);
                    
                    codeBlock.parentElement.replaceWith(container);
                });
                
                return tempDiv.innerHTML;
            }

            function appendAssistantNotebookCell(msgData, modelName = null) {
                cellCounter++;
                const cellId = 'cell-' + cellCounter;
                const sql = msgData.sql || '';
                const data = msgData.data || null;
                const execTime = msgData.execution_time_ms || 0;
                const duckTime = msgData.duckdb_time_ms || 0;
                const rowCount = msgData.row_count || 0;
                const fullContent = msgData.content || '';
                const modelUsed = modelName || msgData.model || currentModel;
                const hasMermaid = fullContent && (fullContent.includes('```mermaid') || fullContent.includes('language-mermaid'));

                const wrapper = document.createElement('div');
                wrapper.className = 'w-full pt-2';

                // Notebook Cell Container
                const cell = document.createElement('div');
                cell.className = 'bg-slate-900/90 border border-slate-800 rounded-3xl overflow-hidden shadow-xl';

                // Cell Header / Notebook Action Bar
                let actionsHtml = `
                    <div class="bg-slate-950/80 border-b border-slate-800 px-5 py-3 flex flex-wrap items-center justify-between gap-3 text-xs">
                        <div class="flex items-center gap-2.5 flex-wrap">
                            <span class="font-mono text-emerald-400 font-bold bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                                [Out ${cellCounter}]
                            </span>
                            <span class="inline-flex items-center gap-1.5 font-mono text-purple-300 bg-purple-500/10 px-2.5 py-0.5 rounded-full border border-purple-500/20 font-medium">
                                <svg class="w-3.5 h-3.5 text-purple-400" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                                </svg>
                                <span>${modelUsed}</span>
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
                                <button onclick="copyToClipboard(window.cellSql_${cellCounter}, this)" class="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs font-medium border border-slate-700 transition flex items-center gap-1">
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
                            <button onclick="copyToClipboard(window.cellContent_${cellCounter}, this)" class="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs font-medium border border-slate-700 transition flex items-center gap-1">
                                <span>Copiar Resposta</span>
                            </button>
                        </div>
                    </div>
                `;

                // Save data and text to window for copy/export actions
                window['cellSql_' + cellCounter] = sql;
                window['cellContent_' + cellCounter] = fullContent;
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
                            ${hasMermaid ? `
                            <button onclick="switchTab('${cellId}', 'diagram')" id="btn-${cellId}-diagram" class="tab-btn px-3 py-1.5 border-b-2 border-transparent text-sky-400 hover:text-sky-200 transition">
                                📐 Diagrama Mermaid
                            </button>` : ''}
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
                            ${renderMarkdownWithMermaid(fullContent)}
                        </div>
                        ${hasMermaid ? `
                        <div id="${cellId}-view-diagram" class="tab-view hidden">
                            ${renderMarkdownWithMermaid(fullContent)}
                        </div>` : ''}
                    `;
                } else {
                    bodyHtml += `<div class="prose prose-invert max-w-none text-sm leading-relaxed">${renderMarkdownWithMermaid(fullContent)}</div>`;
                }

                bodyHtml += `</div>`;

                cell.innerHTML = actionsHtml + tabsHtml + bodyHtml;
                wrapper.appendChild(cell);
                chatBox.appendChild(wrapper);

                // Highlight standard code blocks
                wrapper.querySelectorAll('pre code:not(.language-mermaid)').forEach((block) => {
                    hljs.highlightElement(block);
                });

                // Render all Mermaid diagram elements with auto-healing and fallback
                wrapper.querySelectorAll('.mermaid-diagram-code').forEach(async (el) => {
                    const encoded = el.getAttribute('data-mermaid-code');
                    const rawCode = encoded ? decodeURIComponent(encoded) : el.textContent;
                    const sanitized = sanitizeMermaidCode(rawCode);

                    try {
                        const id = 'mermaid-' + Math.random().toString(36).substring(2, 9);
                        const { svg } = await mermaid.render(id, sanitized);
                        el.innerHTML = svg;
                    } catch (err1) {
                        console.warn('Mermaid primary render failed, attempting fallback to graph:', err1);
                        document.querySelectorAll('[id^="dmermaid"]').forEach(n => n.remove());

                        const fallbackGraph = fallbackToGraph(sanitized);
                        if (fallbackGraph) {
                            try {
                                const idFb = 'mermaid-fb-' + Math.random().toString(36).substring(2, 9);
                                const { svg } = await mermaid.render(idFb, fallbackGraph);
                                el.innerHTML = svg;
                                return;
                            } catch (err2) {
                                console.warn('Mermaid fallback graph failed:', err2);
                                document.querySelectorAll('[id^="dmermaid"]').forEach(n => n.remove());
                            }
                        }
                        el.innerHTML = `
                            <div class="space-y-2 w-full text-left">
                                <div class="text-xs text-amber-300/90 p-3 bg-amber-950/30 border border-amber-800/40 rounded-xl font-mono">
                                    ⚠️ Diagrama renderizado em formato textual (formato não reconhecido pela biblioteca gráfica):
                                </div>
                                <pre class="bg-slate-950 p-3 rounded-xl border border-slate-800 text-xs font-mono text-slate-300 overflow-x-auto"><code>${sanitized}</code></pre>
                            </div>
                        `;
                    }
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
                if (recognition && isRecording) {
                    recognition.stop();
                    isRecording = false;
                    updateMicUi(false);
                }

                const q = userInput.value.trim();
                if (!q && attachedFiles.length === 0) return;

                const welcomeEl = document.getElementById('welcome-view');
                if (welcomeEl) welcomeEl.remove();

                const promptText = q || 'Analise os arquivos anexados.';
                const currentAttachments = [...attachedFiles];
                const requestedModel = currentModel;

                // Append user message with attachments preview and identified model
                appendUserMessage(promptText, currentAttachments, requestedModel);
                messages.push({
                    role: 'user', 
                    content: promptText,
                    attachments: currentAttachments
                });

                // Clear input and attachments
                userInput.value = '';
                attachedFiles = [];
                renderAttachmentPreviews();

                userInput.disabled = true;
                sendBtn.disabled = true;
                sendBtn.innerHTML = '<svg class="w-4 h-4 animate-spin text-slate-900" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path></svg>';

                const stopTimer = showProcessingStepper(requestedModel);

                try {
                    const res = await fetch('/v1/chat/completions', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            model: requestedModel,
                            messages: messages,
                            attachments: currentAttachments
                        })
                    });
                    const data = await res.json();
                    
                    stopTimer();
                    const stepperEl = document.getElementById('gemini-stepper');
                    if (stepperEl) stepperEl.remove();

                    const choiceMsg = data.choices[0].message;
                    const modelUsed = (data && data.model) || (choiceMsg && choiceMsg.model) || requestedModel;
                    appendAssistantNotebookCell(choiceMsg, modelUsed);
                    messages.push({role: 'assistant', content: choiceMsg.content});
                } catch (err) {
                    stopTimer();
                    const stepperEl = document.getElementById('gemini-stepper');
                    if (stepperEl) stepperEl.remove();

                    appendAssistantNotebookCell({
                        content: '⚠️ **Erro ao consultar o agente:** ' + err.message,
                        sql: null,
                        data: null
                    }, requestedModel);
                } finally {
                    userInput.disabled = false;
                    sendBtn.disabled = false;
                    sendBtn.innerHTML = '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 12h14M12 5l7 7-7 7"/></svg>';
                    userInput.focus();
                }
            }

            // Initialize models on load
            loadAvailableModels();
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

@app.get("/api/models")
async def list_models():
    """Retorna os modelos LLM disponíveis via Ollama."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{LLAMA_SERVER_URL}/api/tags")
            if resp.status_code == 200:
                data = resp.json()
                models = [m["name"] for m in data.get("models", [])]
                if models:
                    default_m = LLM_MODEL if LLM_MODEL in models else models[0]
                    return {"models": models, "default": default_m}
    except Exception:
        pass
    return {"models": [LLM_MODEL, "llama3.2:1b"], "default": LLM_MODEL}

@app.get("/api/engine/status")
def engine_status():
    """Retorna o status do DuckDB, metadados do schema e tabelas conectadas."""
    start = time.perf_counter()
    tables = []
    try:
        if not engine.con:
            engine.connect()
        rel = engine.con.sql("SHOW TABLES FROM corporate_credit")
        tables = [row[0] for row in rel.fetchall()]
    except Exception:
        try:
            tables = [t.name for t in registry.entities.values()]
        except Exception:
            tables = ["counterparts", "facilities", "collaterals", "proposals", "financial_statements", "credit_limits", "covenants"]
    ping_ms = round((time.perf_counter() - start) * 1000, 2)
    return {
        "status": "active",
        "engine": "DuckDB In-Memory",
        "schema": "corporate_credit",
        "tables": tables,
        "table_count": len(tables),
        "catalog": "Polaris Iceberg REST",
        "storage": "MinIO S3 (s3://iceberg-warehouse/)",
        "ping_ms": ping_ms
    }

@app.get("/api/llm/ping")
async def ping_llm():
    """Mede o tempo de resposta e status do servidor Ollama."""
    start = time.perf_counter()
    try:
        async with httpx.AsyncClient(timeout=4.0) as client:
            resp = await client.get(f"{LLAMA_SERVER_URL}/api/version")
            elapsed_ms = round((time.perf_counter() - start) * 1000, 1)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "status": "online",
                    "latency_ms": elapsed_ms,
                    "version": data.get("version", "latest"),
                    "server": "Ollama Local"
                }
    except Exception:
        pass
    return {"status": "offline", "latency_ms": 0, "server": "Ollama Local"}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Recebe e processa arquivos/imagens para enriquecer o contexto da pesquisa."""
    content = await file.read()
    filename = file.filename or "uploaded_file"
    content_type = file.content_type or "application/octet-stream"
    size_bytes = len(content)
    is_image = content_type.startswith("image/")
    
    text_preview = None
    if is_image:
        text_preview = f"[Imagem anexada: {filename} ({round(size_bytes / 1024, 1)} KB)]"
    else:
        # Check if parquet file
        if filename.lower().endswith(".parquet") or content.startswith(b"PAR1"):
            try:
                import tempfile
                import duckdb
                with tempfile.NamedTemporaryFile(suffix=".parquet", delete=True) as tmp:
                    tmp.write(content)
                    tmp.flush()
                    con = duckdb.connect()
                    df_summary = con.execute(f"DESCRIBE SELECT * FROM '{tmp.name}'").fetchdf()
                    cols = ", ".join([f"{row['column_name']} ({row['column_type']})" for _, row in df_summary.iterrows()])
                    row_count = con.execute(f"SELECT COUNT(*) FROM '{tmp.name}'").fetchone()[0]
                    text_preview = f"Arquivo Parquet: {filename} | Total de linhas: {row_count}\nColunas e tipos: {cols}"
            except Exception:
                text_preview = f"Arquivo Parquet: {filename} ({round(size_bytes / 1024, 1)} KB)"
        elif filename.lower().endswith((".csv", ".tsv", ".txt", ".json", ".sql", ".yaml", ".yml", ".md", ".xml", ".log")):
            try:
                text_str = content.decode("utf-8", errors="replace")
                text_preview = text_str[:4000]
            except Exception:
                pass
        else:
            # Check for null bytes to avoid dumping binary gibberish
            if b"\x00" in content[:1024]:
                text_preview = f"[Arquivo binário anexado: {filename} ({round(size_bytes / 1024, 1)} KB)]"
            else:
                try:
                    text_str = content.decode("utf-8", errors="replace")
                    text_preview = text_str[:4000]
                except Exception:
                    text_preview = f"[Arquivo anexado: {filename} ({round(size_bytes / 1024, 1)} KB)]"

    return {
        "name": filename,
        "size": size_bytes,
        "type": content_type,
        "is_image": is_image,
        "content": text_preview
    }

@app.post("/v1/chat/completions")
async def chat_completions(req: ChatCompletionRequest):
    """Middleware compatível com OpenAI API para Open WebUI e interface Web."""
    target_model = req.model if req.model and req.model not in ("local-model", "") else LLM_MODEL
    
    # 1. Collect Attachments Context
    all_attachments: List[Attachment] = []
    if req.attachments:
        all_attachments.extend(req.attachments)
    for msg in req.messages:
        if msg.attachments:
            all_attachments.extend(msg.attachments)

    attachments_context = ""
    if all_attachments:
        attachments_context = "\n=== ARQUIVOS E ANEXOS DA PESQUISA ===\n"
        for att in all_attachments:
            att_info = f"- Arquivo: {att.name} (tipo: {att.type or 'desconhecido'}, tamanho: {round(att.size / 1024, 1) if att.size else 0} KB)"
            if att.content and not att.is_image:
                preview = att.content[:3000]
                att_info += f"\n  Conteúdo:\n```\n{preview}\n```"
            elif att.is_image:
                att_info += " [Imagem anexada pelo usuário para contexto visual/análise]"
            attachments_context += att_info + "\n"
        attachments_context += "======================================\n"

    # 2. Inject Semantic Context and Attachments into System Prompt
    semantic_context = registry.get_prompt_context()
    system_prompt = (
        "Você é um assistente analítico especializado em Pesquisa, Crédito Corporativo e Camada Semântica.\n"
        "Com base no Modelo Semântico e em quaisquer arquivos anexados, converta a pergunta do usuário em uma consulta SQL válida para DuckDB.\n\n"
        f"=== CONTEXTO SEMÂNTICO ===\n{semantic_context}\n===========================\n"
        f"{attachments_context}\n"
        "Regras fundamentais:\n"
        "1. Responda com a query SQL dentro de um bloco ```sql ... ``` se a solicitação puder ser convertida em consulta analítica.\n"
        "2. Sempre use as tabelas qualificadas com o schema (ex: `corporate_credit.facilities`, `corporate_credit.counterparts`).\n"
        "3. Ao combinar métricas de uma entidade com dimensões de outra, utilize JOIN explícito usando as relações indicadas em 'Joins' (ex: `JOIN corporate_credit.counterparts c ON f.counterpart_id = c.counterpart_id`). QUALIFIQUE SEMPRE todas as colunas com o alias da tabela (ex: `c.counterpart_id`, `c.sector`, `f.vl_outstanding_balance`) para evitar colunas ambíguas no DuckDB.\n"
        "4. Se o usuário anexou arquivos (como CSVs ou relatórios), correlacione os dados fornecidos com o modelo analítico.\n"
        "5. Para listar tabelas ou consultar metadados no DuckDB, utilize `SHOW TABLES FROM corporate_credit;` (atenção: DuckDB utiliza FROM, não utilize IN) ou `SELECT table_name, table_schema FROM information_schema.tables WHERE table_schema = 'corporate_credit';` (a coluna padrão SQL de schema é `table_schema`, não `schema_name`).\n"
        "6. Se for apenas conversa genérica, pesquisa conceitual ou saudação, responda normalmente em português.\n"
        "7. Quando o usuário solicitar modelo de dados, relações entre entidades (ERD), arquitetura, linhagem ou diagramas de fluxo, você DEVE gerar um diagrama Mermaid válido dentro de um bloco ```mermaid ... ```.\n"
        "   ATENÇÃO CRÍTICA À SINTAXE DO MERMAID ERDIAGRAM:\n"
        "   - Dentro de cada entidade { }, os atributos devem ser estritamente: `tipo nome_coluna [PK/FK]` (ex: `string counterpart_id PK`).\n"
        "   - NUNCA use sinal de igual `=` ou aspas dentro da entidade (ex: NUNCA escreva `id = \"string\"` ou `col = \"id\"`).\n"
        "   - Toda relação entre entidades DEVE ter um rótulo com dois pontos e aspas (ex: `counterparts ||--o{ facilities : \"possui\"`).\n"
        "   - NUNCA use `PART OF`. Use diretamente o nome da entidade (ex: `counterparts`, `facilities`, `collaterals`, `proposals`).\n"
        "   Exemplo canônico de erDiagram:\n"
        "   ```mermaid\n"
        "   erDiagram\n"
        "       counterparts ||--o{ facilities : \"possui\"\n"
        "       facilities ||--o{ collaterals : \"garantido_por\"\n"
        "       counterparts {\n"
        "           string counterpart_id PK\n"
        "           string nm_counterpart\n"
        "           string sector\n"
        "       }\n"
        "       facilities {\n"
        "           string facility_id PK\n"
        "           string counterpart_id FK\n"
        "           float limit_amount\n"
        "       }\n"
        "   ```\n"
    )

    llm_messages = [{"role": "system", "content": system_prompt}]
    for msg in req.messages:
        llm_messages.append({"role": msg.role, "content": msg.content})

    start_time = time.perf_counter()
    duckdb_time_ms = 0.0
    sql_code = None
    query_results = None

    # 3. Query Ollama / llama.cpp server
    try:
        timeout_config = httpx.Timeout(180.0, connect=15.0)
        async with httpx.AsyncClient(timeout=timeout_config) as client:
            resp = await client.post(
                f"{LLAMA_SERVER_URL}/v1/chat/completions",
                json={
                    "model": target_model,
                    "messages": llm_messages,
                    "temperature": req.temperature,
                    "stream": False
                }
            )
            # Fallback to default LLM_MODEL if target_model failed
            if resp.status_code != 200 and target_model != LLM_MODEL:
                print(f"[LLM Retry] Falha no modelo {target_model} (HTTP {resp.status_code}), tentando {LLM_MODEL}...", flush=True)
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
                raise HTTPException(status_code=resp.status_code, detail=f"Ollama retornou HTTP {resp.status_code}: {resp.text}")
            llm_result = resp.json()
    except Exception as e:
        total_time_ms = round((time.perf_counter() - start_time) * 1000, 1)
        err_msg = str(e).strip() or f"{type(e).__name__} (tempo limite de processamento excedido pelo modelo local)"
        print(f"[LLM Fallback] Erro ao consultar {target_model}: {err_msg}", flush=True)
        # Fallback se LLM não estiver acessível
        return {
            "id": "chatcmpl-fallback",
            "object": "chat.completion",
            "created": 0,
            "model": target_model,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "model": target_model,
                    "content": f"⚠️ **Aviso de Conexão com o Modelo ({target_model}):** {err_msg}\n\nO modelo local demorou mais que o esperado ou esteve temporariamente ocupado. Tente novamente ou selecione um modelo mais rápido como `qwen2.5:1.5b` ou `llama3.2:1b` no seletor.",
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

    # 4. Check if SQL was generated & Execute in DuckDB
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
        "model": target_model,
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "model": target_model,
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

