import os
import re
import duckdb
from typing import Optional, Any, Dict, List

class DuckDBIcebergEngine:
    def __init__(
        self,
        s3_endpoint: str = "localhost:9000",
        s3_access_key: str = "admin",
        s3_secret_key: str = "password123",
        polaris_uri: str = "http://localhost:8181/api/catalog",
        polaris_realm: str = "default-realm",
        use_ssl: bool = False
    ):
        self.s3_endpoint = s3_endpoint
        self.s3_access_key = s3_access_key
        self.s3_secret_key = s3_secret_key
        self.polaris_uri = polaris_uri
        self.polaris_realm = polaris_realm
        self.use_ssl = use_ssl
        self.con = None

    def connect(self) -> duckdb.DuckDBPyConnection:
        """Inicializa DuckDB com extensões Iceberg e HTTPFS e credenciais S3 MinIO."""
        self.con = duckdb.connect(database=":memory:")
        
        # Load extensions
        self.con.sql("INSTALL iceberg; LOAD iceberg;")
        self.con.sql("INSTALL httpfs; LOAD httpfs;")

        # MinIO S3 Credentials & Configuration
        ssl_str = "true" if self.use_ssl else "false"
        self.con.sql(f"""
            SET s3_endpoint='{self.s3_endpoint}';
            SET s3_use_ssl={ssl_str};
            SET s3_url_style='path';
            SET s3_access_key_id='{self.s3_access_key}';
            SET s3_secret_access_key='{self.s3_secret_key}';
        """)

        # Register corporate_credit schema and seed parquet views
        try:
            self.con.sql("CREATE SCHEMA IF NOT EXISTS corporate_credit;")
            seed_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "seed")
            table_files = {
                "counterparts": "counterparts.parquet",
                "facilities": "facilities.parquet",
                "collaterals": "collaterals.parquet",
                "proposals": "proposals.parquet",
                "financial_statements": "financial_statements.parquet",
                "credit_limits": "credit_limits.parquet",
                "covenants": "covenants.parquet"
            }
            dim_aliases = {
                "counterparts": ", ds_cnae_sector AS sector, nm_economic_group AS economic_group, cd_rating_agency AS internal_rating",
                "facilities": ", tp_operation AS operation_type, st_operation AS status",
                "collaterals": ", tp_collateral AS collateral_type, st_collateral AS collateral_status",
                "proposals": ", st_decision AS decision_status, nm_committee AS risk_committee",
                "financial_statements": ", nr_fiscal_year AS fiscal_year, st_audited AS audited_status",
                "credit_limits": ", tp_limit AS limit_type, st_limit AS limit_status",
                "covenants": ", tp_covenant AS covenant_type, st_compliance AS compliance_status"
            }
            for tbl, fname in table_files.items():
                fpath = os.path.join(seed_dir, fname)
                if os.path.exists(fpath):
                    alias_sql = dim_aliases.get(tbl, "")
                    self.con.sql(f"CREATE OR REPLACE VIEW corporate_credit.{tbl} AS SELECT *{alias_sql} FROM read_parquet('{fpath}');")

            # Entity name synonyms (e.g. credit_facility, credit_facilities -> facilities)
            entity_aliases = {
                "credit_facilities": "facilities",
                "credit_facility": "facilities",
                "counterpart": "counterparts",
                "facility": "facilities",
                "collateral": "collaterals",
                "proposal": "proposals",
                "financial_statement": "financial_statements",
                "credit_limit": "credit_limits",
                "covenant": "covenants"
            }
            for alias, target in entity_aliases.items():
                self.con.sql(f"CREATE OR REPLACE VIEW corporate_credit.{alias} AS SELECT * FROM corporate_credit.{target};")
        except Exception as seed_err:
            print(f"[Engine Warning] Error seeding local DuckDB views: {seed_err}")

        # Attach Polaris Iceberg REST Catalog if available
        try:
            self.con.sql(f"""
                CREATE SECRET polaris_secret (
                    TYPE ICEBERG,
                    CLIENT_ID '{self.s3_access_key}',
                    CLIENT_SECRET '{self.s3_secret_key}'
                );
            """)
        except Exception as e:
            print(f"[Engine Warning] Secret creation notice: {e}")

        return self.con

    def execute_query(self, sql_query: str) -> List[Dict[str, Any]]:
        """Executa uma query no DuckDB e retorna resultados como lista de dicionários."""
        if not self.con:
            self.connect()

        try:
            rel = self.con.sql(sql_query)
        except Exception as err:
            err_str = str(err)
            # Auto-healing para SHOW TABLES IN <schema> (DuckDB usa SHOW TABLES FROM <schema>)
            if re.search(r'\bSHOW\s+TABLES\s+IN\b', sql_query, flags=re.IGNORECASE):
                fixed_query = re.sub(
                    r'\bSHOW\s+TABLES\s+IN\b',
                    'SHOW TABLES FROM',
                    sql_query,
                    flags=re.IGNORECASE
                )
                try:
                    rel = self.con.sql(fixed_query)
                except Exception:
                    raise err
            # Auto-healing para SHOW COLUMNS FROM/IN <table> (DuckDB usa DESCRIBE <table>)
            elif re.search(r'^\s*SHOW\s+COLUMNS\s+(?:FROM|IN)\b', sql_query, flags=re.IGNORECASE):
                fixed_query = re.sub(
                    r'^\s*SHOW\s+COLUMNS\s+(?:FROM|IN)\s+([a-zA-Z0-9_\.\"]+)',
                    r'DESCRIBE \1',
                    sql_query,
                    flags=re.IGNORECASE
                )
                try:
                    rel = self.con.sql(fixed_query)
                except Exception:
                    raise err
            # Auto-healing para erros comuns de metadados onde LLMs usam schema_name em vez de table_schema
            elif "schema_name" in err_str or ("schema_name" in sql_query and "information_schema" in sql_query.lower()):
                fixed_query = re.sub(
                    r'\binformation_schema\.tables\b',
                    '(SELECT *, table_schema AS schema_name FROM information_schema.tables)',
                    sql_query,
                    flags=re.IGNORECASE
                )
                fixed_query = re.sub(
                    r'\binformation_schema\.columns\b',
                    '(SELECT *, table_schema AS schema_name FROM information_schema.columns)',
                    fixed_query,
                    flags=re.IGNORECASE
                )
                try:
                    rel = self.con.sql(fixed_query)
                except Exception:
                    raise err
            else:
                raise err

        if rel is None:
            return []
        df = rel.df()
        return df.to_dict(orient="records")

def init_duckdb() -> duckdb.DuckDBPyConnection:
    engine = DuckDBIcebergEngine()
    return engine.connect()

if __name__ == "__main__":
    engine = DuckDBIcebergEngine()
    con = engine.connect()
    print("DuckDB Iceberg Engine initialized successfully.")
