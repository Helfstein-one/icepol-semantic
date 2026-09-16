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
                    LLM: <span id="header-llm-label">llama3.2:3b</span> (Ollama)
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
            }

            function toggleModelDropdown(e) {
                e.stopPropagation();
                modelDropdownMenu.classList.toggle('hidden');
                document.getElementById('model-chevron')?.classList.toggle('rotate-180');
            }

            function selectModel(modelName) {
                currentModel = modelName;
                updateModelUI(modelName);
                modelDropdownMenu.classList.add('hidden');
                document.getElementById('model-chevron')?.classList.remove('rotate-180');
                renderModelList(availableModels);
            }

            function updateModelUI(modelName) {
                selectedModelLabel.innerText = modelName;
                if (headerLlmLabel) headerLlmLabel.innerText = modelName;
                userInput.placeholder = `Peça ao ${modelName}`;
            }

            // Close dropdown when clicking outside
            document.addEventListener('click', (e) => {
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
        "3. Ao combinar métricas de uma entidade com dimensões de outra, utilize JOIN explícito usando as relações indicadas em 'Joins' (ex: `JOIN corporate_credit.counterparts c ON f.counterpart_id = c.counterpart_id`).\n"
        "4. Se o usuário anexou arquivos (como CSVs ou relatórios), correlacione os dados fornecidos com o modelo analítico.\n"
        "5. Para listar tabelas ou consultar metadados no DuckDB, utilize `SHOW TABLES IN corporate_credit;` ou `SELECT table_name, table_schema FROM information_schema.tables WHERE table_schema = 'corporate_credit';` (a coluna padrão SQL de schema é `table_schema`, não `schema_name`).\n"
        "6. Se for apenas conversa genérica, pesquisa conceitual ou saudação, responda normalmente em português.\n"
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
        async with httpx.AsyncClient(timeout=60.0) as client:
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
                    "content": f"[Middleware Fallback - LLM Offline] Contexto Semântico:\n{semantic_context}\n\nErro ao conectar ao LLM ({target_model}): {str(e)}",
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

