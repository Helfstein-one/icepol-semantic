import os
import json
import httpx
import asyncio
from mcp.server.fastmcp import FastMCP

from semantic.parser import SemanticRegistry
from core.engine import DuckDBIcebergEngine

# Initialize FastMCP Server
mcp = FastMCP("icepol-semantic-mcp")

# Environment & Core Registries
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

@mcp.tool()
async def get_semantic_ontologies() -> str:
    """Retorna as entidades, dimensões e métricas registradas na camada semântica de Crédito Corporativo."""
    return registry.get_prompt_context()

@mcp.tool()
async def query_llama(prompt: str, system_prompt: str = "") -> str:
    """Envia um prompt para o servidor local de inferência llama.cpp e retorna a resposta gerada."""
    if not system_prompt:
        system_prompt = (
            "Você é um assistente especialista em Crédito Corporativo e Engenharia de Dados.\n"
            f"=== CONTEXTO SEMÂNTICO ===\n{registry.get_prompt_context()}\n==========================="
        )

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                f"{LLAMA_SERVER_URL}/v1/chat/completions",
                json={
                    "model": LLM_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.2
                }
            )
            if resp.status_code == 200:
                result = resp.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"[Erro Llama.cpp - Status {resp.status_code}]: {resp.text}"
    except Exception as e:
        return f"[Llama.cpp Indisponível/Offline]: {str(e)}"

@mcp.tool()
async def execute_semantic_sql(metric_names: list[str], group_by_dims: list[str] = None, entity_name: str = "credit_facility") -> str:
    """Compila métricas e dimensões semânticas em SQL DuckDB e executa a consulta na engine de dados.
    
    Args:
        metric_names: Lista de métricas semânticas (ex: ['total_exposure', 'overdue_ratio_90d'])
        group_by_dims: Lista de dimensões para agrupamento (ex: ['operation_type'])
        entity_name: Nome da entidade alvo (padrão: 'credit_facility')
    """
    sql_query = registry.compile_query(metric_names=metric_names, group_by_dims=group_by_dims, entity_name=entity_name)
    try:
        results = engine.execute_query(sql_query)
        return json.dumps({
            "compiled_sql": sql_query,
            "results": results
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({
            "compiled_sql": sql_query,
            "error": str(e)
        }, indent=2)

if __name__ == "__main__":
    mcp.run()
