import os
import yaml
from typing import List, Dict, Any, Optional

class SemanticRegistry:
    def __init__(self, ontology_dir: str):
        self.ontology_dir = ontology_dir
        self.entities: List[Dict[str, Any]] = []
        self.metrics: List[Dict[str, Any]] = []
        self.domain: str = "corporate_credit"
        self._load_ontologies()

    def _load_ontologies(self):
        credit_yaml = os.path.join(self.ontology_dir, "corporate_credit.yaml")
        if os.path.exists(credit_yaml):
            with open(credit_yaml, "r", encoding="utf-8") as f:
                spec = yaml.safe_load(f) or {}
                self.domain = spec.get("domain", self.domain)
                self.entities = spec.get("entities", [])
                if "metrics" in spec:
                    self.metrics.extend(spec.get("metrics", []))

        metrics_yaml = os.path.join(self.ontology_dir, "metrics.yaml")
        if os.path.exists(metrics_yaml):
            with open(metrics_yaml, "r", encoding="utf-8") as f:
                spec = yaml.safe_load(f) or {}
                if "metrics" in spec:
                    self.metrics.extend(spec.get("metrics", []))

    def get_prompt_context(self) -> str:
        """Gera o contexto reduzido de métricas/dimensões para injetar no Llama."""
        context = [f"Domain: {self.domain}"]
        context.append("\nEntities & Dimensions:")
        for entity in self.entities:
            dims = [f"{d['name']} ({d['column']})" for d in entity.get("dimensions", [])]
            fks = entity.get("foreign_keys", [])
            fk_info = ""
            if fks:
                fk_parts = []
                for fk in fks:
                    for k, v in fk.items():
                        fk_parts.append(f"{k} -> {v}")
                fk_info = f" | Joins: [{', '.join(fk_parts)}]"
            context.append(f"- Entity: {entity['name']} | Table: {entity['table']} | Dimensions: [{', '.join(dims)}]{fk_info}")

        context.append("\nMetrics:")
        for metric in self.metrics:
            context.append(f"- Metric: {metric['name']} | Entity: {metric.get('entity')} | Logic: {metric['sql']} | Desc: {metric.get('description', '')}")

        return "\n".join(context)

    def compile_query(self, metric_names: List[str], group_by_dims: List[str] = None, entity_name: str = "credit_facility") -> str:
        """Compila métricas e dimensões semânticas em SQL DuckDB."""
        group_by_dims = group_by_dims or []
        entity = next((e for e in self.entities if e["name"] == entity_name), None)
        if not entity:
            table_name = "corporate_credit.facilities"
        else:
            table_name = entity["table"]

        select_exprs = []
        dim_cols = []
        
        # Resolve dimensions to table columns
        if entity:
            dim_map = {d["name"]: d["column"] for d in entity.get("dimensions", [])}
            for dim in group_by_dims:
                col = dim_map.get(dim, dim)
                select_exprs.append(f"{col} AS {dim}")
                dim_cols.append(col)
        else:
            select_exprs.extend(group_by_dims)
            dim_cols.extend(group_by_dims)

        # Resolve metrics
        for m_name in metric_names:
            metric = next((m for m in self.metrics if m["name"] == m_name), None)
            if metric:
                select_exprs.append(f"{metric['sql']} AS {metric['name']}")
            else:
                select_exprs.append(m_name)

        sql = f"SELECT {', '.join(select_exprs)} FROM {table_name}"
        if dim_cols:
            sql += f" GROUP BY {', '.join(dim_cols)}"
        return sql

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    registry = SemanticRegistry(os.path.join(base_dir, "ontologies"))
    print("--- PROMPT CONTEXT ---")
    print(registry.get_prompt_context())
    print("\n--- COMPILED QUERY SAMPLE ---")
    print(registry.compile_query(metric_names=["total_exposure", "overdue_ratio_90d"], group_by_dims=["operation_type"]))
