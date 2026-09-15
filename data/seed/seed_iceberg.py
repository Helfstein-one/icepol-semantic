import os
import duckdb
import pandas as pd

def seed_data():
    """Gera dados sintéticos expandidos de Crédito Corporativo para 7 tabelas físicas."""
    print("Iniciando geração de dados sintéticos para 7 tabelas de Crédito Corporativo...")

    # 1. Counterparts
    counterparts_df = pd.DataFrame([
        {
            "counterpart_id": "CP-001",
            "nm_economic_group": "Grupo Votorantim",
            "ds_cnae_sector": "Indústria Siderúrgica",
            "cd_rating_agency": "AAA"
        },
        {
            "counterpart_id": "CP-002",
            "nm_economic_group": "Grupo JBS",
            "ds_cnae_sector": "Agronegócio e Alimentos",
            "cd_rating_agency": "AA+"
        },
        {
            "counterpart_id": "CP-003",
            "nm_economic_group": "Grupo Suzano",
            "ds_cnae_sector": "Papel e Celulose",
            "cd_rating_agency": "AAA"
        },
        {
            "counterpart_id": "CP-004",
            "nm_economic_group": "Grupo Magalu",
            "ds_cnae_sector": "Varejo",
            "cd_rating_agency": "BBB-"
        }
    ])

    # 2. Facilities
    facilities_df = pd.DataFrame([
        {
            "facility_id": "FAC-1001",
            "counterpart_id": "CP-001",
            "tp_operation": "Capital de Giro",
            "st_operation": "Ativo",
            "vl_outstanding_balance": 15000000.0,
            "vl_provision": 150000.0,
            "vl_collateral_allocated": 18000000.0,
            "nr_days_overdue": 0
        },
        {
            "facility_id": "FAC-1002",
            "counterpart_id": "CP-001",
            "tp_operation": "Debêntures",
            "st_operation": "Ativo",
            "vl_outstanding_balance": 50000000.0,
            "vl_provision": 500000.0,
            "vl_collateral_allocated": 60000000.0,
            "nr_days_overdue": 0
        },
        {
            "facility_id": "FAC-1003",
            "counterpart_id": "CP-002",
            "tp_operation": "CCB",
            "st_operation": "Ativo",
            "vl_outstanding_balance": 25000000.0,
            "vl_provision": 750000.0,
            "vl_collateral_allocated": 30000000.0,
            "nr_days_overdue": 35
        },
        {
            "facility_id": "FAC-1004",
            "counterpart_id": "CP-004",
            "tp_operation": "Capital de Giro",
            "st_operation": "Inadimplente",
            "vl_outstanding_balance": 12000000.0,
            "vl_provision": 12000000.0,
            "vl_collateral_allocated": 8000000.0,
            "nr_days_overdue": 120
        },
        {
            "facility_id": "FAC-1005",
            "counterpart_id": "CP-003",
            "tp_operation": "Financiamento de Exportação",
            "st_operation": "Ativo",
            "vl_outstanding_balance": 40000000.0,
            "vl_provision": 400000.0,
            "vl_collateral_allocated": 50000000.0,
            "nr_days_overdue": 0
        }
    ])

    # 3. Collaterals
    collaterals_df = pd.DataFrame([
        {
            "collateral_id": "COL-501",
            "facility_id": "FAC-1001",
            "counterpart_id": "CP-001",
            "tp_collateral": "Imóveis",
            "st_collateral": "Ativa",
            "vl_appraised_value": 20000000.0
        },
        {
            "collateral_id": "COL-502",
            "facility_id": "FAC-1002",
            "counterpart_id": "CP-001",
            "tp_collateral": "Fiança Bancária",
            "st_collateral": "Ativa",
            "vl_appraised_value": 65000000.0
        },
        {
            "collateral_id": "COL-503",
            "facility_id": "FAC-1003",
            "counterpart_id": "CP-002",
            "tp_collateral": "Recebíveis",
            "st_collateral": "Ativa",
            "vl_appraised_value": 32000000.0
        },
        {
            "collateral_id": "COL-504",
            "facility_id": "FAC-1004",
            "counterpart_id": "CP-004",
            "tp_collateral": "Equipamentos",
            "st_collateral": "Em Liquidação",
            "vl_appraised_value": 9000000.0
        }
    ])

    # 4. Proposals
    proposals_df = pd.DataFrame([
        {
            "proposal_id": "PROP-801",
            "counterpart_id": "CP-001",
            "vl_requested": 30000000.0,
            "st_decision": "Aprovada",
            "nm_committee": "Comitê Executivo"
        },
        {
            "proposal_id": "PROP-802",
            "counterpart_id": "CP-002",
            "vl_requested": 15000000.0,
            "st_decision": "Aprovada",
            "nm_committee": "Comitê Local"
        },
        {
            "proposal_id": "PROP-803",
            "counterpart_id": "CP-004",
            "vl_requested": 20000000.0,
            "st_decision": "Recusada",
            "nm_committee": "Diretoria"
        },
        {
            "proposal_id": "PROP-804",
            "counterpart_id": "CP-003",
            "vl_requested": 50000000.0,
            "st_decision": "Em Análise",
            "nm_committee": "Comitê Executivo"
        }
    ])

    # 5. Financial Statements (Balanços e EBITDA)
    financial_statements_df = pd.DataFrame([
        {
            "statement_id": "ST-2025-01",
            "counterpart_id": "CP-001",
            "nr_fiscal_year": "2025",
            "st_audited": "Auditado",
            "vl_net_debt": 45000000.0,
            "vl_ebitda": 30000000.0
        },
        {
            "statement_id": "ST-2025-02",
            "counterpart_id": "CP-002",
            "nr_fiscal_year": "2025",
            "st_audited": "Auditado",
            "vl_net_debt": 80000000.0,
            "vl_ebitda": 40000000.0
        },
        {
            "statement_id": "ST-2025-03",
            "counterpart_id": "CP-003",
            "nr_fiscal_year": "2025",
            "st_audited": "Auditado",
            "vl_net_debt": 60000000.0,
            "vl_ebitda": 50000000.0
        },
        {
            "statement_id": "ST-2025-04",
            "counterpart_id": "CP-004",
            "nr_fiscal_year": "2025",
            "st_audited": "Não Auditado",
            "vl_net_debt": 35000000.0,
            "vl_ebitda": 7000000.0
        }
    ])

    # 6. Credit Limits (Limites Aprovados vs Utilizados)
    credit_limits_df = pd.DataFrame([
        {
            "limit_id": "LIM-101",
            "counterpart_id": "CP-001",
            "tp_limit": "Guarda-Chuva",
            "st_limit": "Ativo",
            "vl_approved_limit": 100000000.0,
            "vl_used_limit": 65000000.0
        },
        {
            "limit_id": "LIM-102",
            "counterpart_id": "CP-002",
            "tp_limit": "Rotativo",
            "st_limit": "Ativo",
            "vl_approved_limit": 50000000.0,
            "vl_used_limit": 25000000.0
        },
        {
            "limit_id": "LIM-103",
            "counterpart_id": "CP-003",
            "tp_limit": "Específico",
            "st_limit": "Ativo",
            "vl_approved_limit": 60000000.0,
            "vl_used_limit": 40000000.0
        },
        {
            "limit_id": "LIM-104",
            "counterpart_id": "CP-004",
            "tp_limit": "Rotativo",
            "st_limit": "Suspenso",
            "vl_approved_limit": 15000000.0,
            "vl_used_limit": 12000000.0
        }
    ])

    # 7. Covenants (Cláusulas Contratuais)
    covenants_df = pd.DataFrame([
        {
            "covenant_id": "COV-301",
            "facility_id": "FAC-1001",
            "tp_covenant": "Dívida Líquida/EBITDA <= 2.5",
            "st_compliance": "Em Cumpirmento"
        },
        {
            "covenant_id": "COV-302",
            "facility_id": "FAC-1002",
            "tp_covenant": "Cobertura de Juros (ICR) >= 3.0",
            "st_compliance": "Em Cumpirmento"
        },
        {
            "covenant_id": "COV-303",
            "facility_id": "FAC-1003",
            "tp_covenant": "Dívida Líquida/EBITDA <= 3.0",
            "st_compliance": "Em Cumpirmento"
        },
        {
            "covenant_id": "COV-304",
            "facility_id": "FAC-1004",
            "tp_covenant": "Dívida Líquida/EBITDA <= 3.5",
            "st_compliance": "Desenquadrado"
        }
    ])

    # Save to local seed directory as parquet
    data_dir = os.path.dirname(os.path.abspath(__file__))
    tables = {
        "counterparts": counterparts_df,
        "facilities": facilities_df,
        "collaterals": collaterals_df,
        "proposals": proposals_df,
        "financial_statements": financial_statements_df,
        "credit_limits": credit_limits_df,
        "covenants": covenants_df
    }

    con = duckdb.connect()
    con.sql("CREATE SCHEMA IF NOT EXISTS corporate_credit;")

    print("Parquets de seed gerados:")
    for name, df in tables.items():
        path = os.path.join(data_dir, f"{name}.parquet")
        df.to_parquet(path, index=False)
        con.sql(f"CREATE TABLE corporate_credit.{name} AS SELECT * FROM '{path}'")
        print(f"- {path}")

    print("DuckDB schema `corporate_credit` populado com 7 tabelas para testes.")

    # Sincronizar com MinIO S3 se disponível
    try:
        import s3fs
        s3_endpoint = os.getenv("MINIO_ENDPOINT", "localhost:9000")
        endpoint_url = s3_endpoint if s3_endpoint.startswith("http") else f"http://{s3_endpoint}"
        s3_user = os.getenv("MINIO_ACCESS_KEY", "admin")
        s3_pass = os.getenv("MINIO_SECRET_KEY", "password123")
        
        s3 = s3fs.S3FileSystem(
            key=s3_user,
            secret=s3_pass,
            client_kwargs={"endpoint_url": endpoint_url}
        )
        bucket = "warehouse"
        if not s3.exists(bucket):
            s3.mkdir(bucket)
            print(f"Bucket S3 '{bucket}' criado no MinIO.")
        
        for name in tables:
            local_file = os.path.join(data_dir, f"{name}.parquet")
            target_key = f"{bucket}/corporate_credit/{name}.parquet"
            s3.put(local_file, target_key)
            print(f"  -> Upload MinIO: s3://{target_key}")
        print("Sincronização com MinIO S3 concluída com sucesso!")
    except Exception as s3_err:
        print(f"[Aviso] Não foi possível sincronizar com MinIO: {s3_err}")

if __name__ == "__main__":
    seed_data()
