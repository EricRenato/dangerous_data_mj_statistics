"""
Pipeline ETL: Compilação e carga do banco de dados relacional SQLite (mj_analytics.db)
Dangerous Data: MJ Statistics
"""

import sys
from pathlib import Path

# Ajustar path para importar database
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from src.database import get_connection, execute_script, DEFAULT_DB_PATH

def build_database(reset: bool = True):
    """Executa scripts de schema, seeds e views analíticas no SQLite."""
    sql_dir = BASE_DIR / "sql"
    db_file = DEFAULT_DB_PATH

    if reset and db_file.exists():
        print(f"-> Removendo banco existente: {db_file.name}")
        db_file.unlink()

    db_file.parent.mkdir(parents=True, exist_ok=True)
    print(f"Iniciando compilação do banco SQLite em: {db_file}")

    # 1. Procurar o script completo na pasta sql local ou na pasta de backup
    local_sql = sql_dir / "database_complete.sql"
    bkp_sql = BASE_DIR.parent / "BKP_MJ_Dataset" / "SQL" / "MJ_Database_SQL.sql"

    if local_sql.exists():
        script_to_run = local_sql
    elif bkp_sql.exists():
        script_to_run = bkp_sql
    else:
        print("❌ Erro: Nenhum arquivo SQL encontrado em 'sql/' nem em 'BKP_MJ_Dataset/SQL/'")
        return

    print(f"-> Executando DDL e carga de dados de: {script_to_run.name}...")
    execute_script(script_to_run, db_file)

    # 2. Executar views analíticas se o arquivo existir
    views_script = sql_dir / "analytical_views.sql"
    if views_script.exists():
        print("-> Criando Views Analíticas (Data Marts)...")
        execute_script(views_script, db_file)

    # 3. Validação e contagem das tabelas
    with get_connection(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM dim_album;")
        albuns = cursor.fetchone()[0]
        cursor.execute("SELECT count(*) FROM fato_single;")
        singles = cursor.fetchone()[0]
        cursor.execute("SELECT count(*) FROM fato_turne;")
        turnes = cursor.fetchone()[0]

    print("\n✅ Banco compilado com sucesso!")
    print(f"   • Álbuns cadastrados: {albuns}")
    print(f"   • Singles cadastrados: {singles}")
    print(f"   • Turnês cadastradas: {turnes}")

if __name__ == "__main__":
    build_database(reset=True)