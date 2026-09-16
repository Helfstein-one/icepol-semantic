import urllib.request, os, subprocess

pwd = os.path.abspath(os.curdir)
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def capture_html(html_path, out_png):
    file_url = f"file://{pwd}/{html_path}"
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--window-size=1440,900",
        f"--screenshot={out_png}",
        file_url
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"Captured: {out_png}")

html = urllib.request.urlopen("http://localhost:8000/").read().decode("utf-8")

mermaid_content = """Abaixo está o modelo conceitual e relacional das entidades corporativas do schema corporate_credit:

```mermaid
erDiagram
    COUNTERPARTS ||--o{ FACILITIES : "possui"
    COUNTERPARTS ||--o{ PROPOSALS : "solicita"
    FACILITIES ||--o{ COLLATERALS : "garantida_por"
    FACILITIES ||--o{ COVENANTS : "regulada_por"

    COUNTERPARTS {
        string counterpart_id PK
        string nm_economic_group
        string ds_cnae_sector
        string cd_rating_agency
    }

    FACILITIES {
        string facility_id PK
        string counterpart_id FK
        string tp_operation
        float vl_contracted
        string st_operation
    }

    COLLATERALS {
        string collateral_id PK
        string facility_id FK
        string tp_collateral
        float vl_appraisal
        string st_collateral
    }

    PROPOSALS {
        string proposal_id PK
        string counterpart_id FK
        float vl_requested
        string st_decision
    }

    COVENANTS {
        string covenant_id PK
        string facility_id FK
        string tp_covenant
        float vl_target
        string st_compliance
    }
```
Diagrama renderizado dinamicamente via Mermaid integrado ao DuckDB Lakehouse.
"""

scene6_script = f"""
<script>
window.addEventListener('DOMContentLoaded', () => {{
    document.getElementById('welcome-view')?.remove();
    const userDiv = document.createElement('div');
    userDiv.className = 'flex justify-end';
    userDiv.innerHTML = '<div class="bg-[#1e1f20] text-sky-300 px-5 py-3 rounded-3xl max-w-2xl border border-sky-600/50 text-sm shadow-xl font-medium">Mostre o diagrama de modelo das entidades (ERD) e relacionamentos de crédito</div>';
    document.getElementById('chat-box').appendChild(userDiv);
    
    appendAssistantNotebookCell({{
        sql: null,
        data: null,
        execution_time_ms: 180.5,
        duckdb_time_ms: 0.0,
        row_count: 0,
        content: {repr(mermaid_content)}
    }}, "llama3.2:3b");
}});
</script>
"""

with open("video/scene6_mermaid.html", "w") as f:
    f.write(html.replace("</body>", scene6_script + "</body>"))
capture_html("video/scene6_mermaid.html", "video/scene6_mermaid.png")
