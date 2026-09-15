import os
import json
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
            /* Custom markdown styles */
            .prose pre {
                margin-top: 1rem;
                margin-bottom: 1rem;
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
        </style>
    </head>
    <body class="bg-slate-950 text-slate-100 flex flex-col h-full font-sans antialiased">
        <!-- Minimalist Header -->
        <header class="border-b border-slate-800/80 bg-slate-900/60 backdrop-blur-md px-6 md:px-10 py-4 flex items-center justify-between sticky top-0 z-10">
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

        <!-- Main Chat Stream with Generous Spacing -->
        <main class="flex-1 overflow-y-auto px-4 md:px-8 py-8">
            <div class="max-w-4xl mx-auto space-y-6" id="chat-box">
                <!-- Welcome Card -->
                <div class="bg-slate-900/50 border border-slate-800/80 rounded-2xl p-6 md:p-8 space-y-4 shadow-sm">
                    <div class="space-y-1.5">
                        <h2 class="text-base font-semibold text-white">👋 Bem-vindo ao Icepol Semantic Agent!</h2>
                        <p class="text-sm text-slate-400 leading-relaxed">
                            Faça perguntas analíticas em linguagem natural. A camada semântica mapeará automaticamente as regras de negócio ontológicas, montará a query SQL e a executará no DuckDB.
                        </p>
                    </div>
                    
                    <div class="pt-2 flex flex-wrap gap-2.5">
                        <button onclick="sendPrompt(this.innerText)" class="px-3.5 py-2 bg-slate-800/80 hover:bg-slate-850 hover:border-slate-600 text-slate-300 rounded-xl text-xs font-medium border border-slate-700/80 transition shadow-sm text-left">
                            Qual a exposição total por setor?
                        </button>
                        <button onclick="sendPrompt(this.innerText)" class="px-3.5 py-2 bg-slate-800/80 hover:bg-slate-850 hover:border-slate-600 text-slate-300 rounded-xl text-xs font-medium border border-slate-700/80 transition shadow-sm text-left">
                            Qual a alavancagem média por grupo econômico?
                        </button>
                        <button onclick="sendPrompt(this.innerText)" class="px-3.5 py-2 bg-slate-800/80 hover:bg-slate-850 hover:border-slate-600 text-slate-300 rounded-xl text-xs font-medium border border-slate-700/80 transition shadow-sm text-left">
                            Mostre as propostas de crédito e seus status
                        </button>
                        <button onclick="sendPrompt(this.innerText)" class="px-3.5 py-2 bg-slate-800/80 hover:bg-slate-850 hover:border-slate-600 text-slate-300 rounded-xl text-xs font-medium border border-slate-700/80 transition shadow-sm text-left">
                            Qual o volume de garantias por tipo de colateral?
                        </button>
                    </div>
                </div>
            </div>
        </main>

        <!-- Fixed Footer Input -->
        <footer class="border-t border-slate-800/80 bg-slate-900/60 backdrop-blur-md px-4 md:px-8 py-4">
            <div class="max-w-4xl mx-auto">
                <form id="chat-form" onsubmit="handleSubmit(event)" class="flex gap-3 items-center">
                    <input id="user-input" type="text" placeholder="Pergunte sobre crédito corporativo, garantias, covenants, limites..." 
                        class="flex-1 bg-slate-900/90 border border-slate-700/80 rounded-xl px-5 py-3.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500 text-slate-100 placeholder-slate-500 transition shadow-inner">
                    <button type="submit" id="send-btn" class="bg-blue-600 hover:bg-blue-500 text-white font-medium px-6 py-3.5 rounded-xl text-sm transition shadow-sm shrink-0 flex items-center gap-2">
                        <span>Enviar</span>
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
                        </svg>
                    </button>
                </form>
            </div>
        </footer>

        <script>
            const chatBox = document.getElementById('chat-box');
            const userInput = document.getElementById('user-input');
            const sendBtn = document.getElementById('send-btn');
            const messages = [];

            function appendMessage(role, content) {
                const wrapper = document.createElement('div');
                wrapper.className = role === 'user' 
                    ? 'flex justify-end pt-2' 
                    : 'flex justify-start pt-2';
                
                const bubble = document.createElement('div');
                if (role === 'user') {
                    bubble.className = 'bg-blue-600 text-white rounded-2xl rounded-tr-sm px-5 py-3.5 max-w-xl text-sm shadow-md leading-relaxed';
                    bubble.innerText = content;
                } else {
                    bubble.className = 'bg-slate-900/90 border border-slate-800/90 text-slate-200 rounded-2xl rounded-tl-sm p-6 max-w-3xl text-sm prose prose-invert w-full shadow-md space-y-3';
                    bubble.innerHTML = marked.parse(content);
                    bubble.querySelectorAll('pre code').forEach((block) => {
                        hljs.highlightElement(block);
                    });
                }
                
                wrapper.appendChild(bubble);
                chatBox.appendChild(wrapper);
                chatBox.scrollIntoView({ behavior: 'smooth', block: 'end' });
                window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
            }

            function sendPrompt(text) {
                userInput.value = text;
                handleSubmit(new Event('submit'));
            }

            async function handleSubmit(e) {
                e.preventDefault();
                const q = userInput.value.trim();
                if (!q) return;

                appendMessage('user', q);
                messages.push({role: 'user', content: q});
                userInput.value = '';
                userInput.disabled = true;
                sendBtn.disabled = true;
                sendBtn.innerHTML = '<span>Processando...</span>';

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
                    const reply = data.choices[0].message.content;
                    appendMessage('assistant', reply);
                    messages.push({role: 'assistant', content: reply});
                } catch (err) {
                    appendMessage('assistant', '⚠️ Erro ao consultar o agente: ' + err.message);
                } finally {
                    userInput.disabled = false;
                    sendBtn.disabled = false;
                    sendBtn.innerHTML = '<span>Enviar</span><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>';
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
                    "content": f"[Middleware Fallback - LLM Offline] Contexto Semântico:\n{semantic_context}\n\nErro ao conectar ao LLM: {str(e)}"
                },
                "finish_reason": "stop"
            }]
        }

    assistant_content = llm_result["choices"][0]["message"]["content"]

    # 3. Check if SQL was generated & Execute in DuckDB
    if "```sql" in assistant_content:
        try:
            sql_code = assistant_content.split("```sql")[1].split("```")[0].strip()
            query_results = engine.execute_query(sql_code)
            results_formatted = json.dumps(query_results, indent=2, ensure_ascii=False)
            assistant_content += f"\n\n**Resultados Executados via DuckDB:**\n```json\n{results_formatted}\n```"
        except Exception as query_err:
            assistant_content += f"\n\n**Erro na execução no DuckDB:** {str(query_err)}"

    return {
        "id": llm_result.get("id", "chatcmpl-local"),
        "object": "chat.completion",
        "created": llm_result.get("created", 0),
        "model": req.model,
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": assistant_content
            },
            "finish_reason": "stop"
        }]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
