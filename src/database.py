"""
Módulo de conexão e execução de queries no SQLite (mj_analytics.db)
Dangerous Data: MJ Statistics
"""

import math
import sqlite3
from pathlib import Path
from typing import Optional
import pandas as pd

# Caminhos padrão do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = BASE_DIR / "data" / "processed" / "mj_analytics.db"

class SQLiteStdDev:
    """Implementação do cálculo de Desvio Padrão amostral para o SQLite."""
    def __init__(self):
        self.M = 0.0
        self.S = 0.0
        self.k = 0

    def step(self, value):
        if value is None:
            return
        t = float(value)
        self.k += 1
        new_M = self.M + (t - self.M) / self.k
        self.S += (t - self.M) * (t - new_M)
        self.M = new_M

    def finalize(self):
        if self.k < 2:
            return 0.0
        return math.sqrt(self.S / (self.k - 1))

def get_connection(db_path: Optional[Path] = None) -> sqlite3.Connection:
    """Retorna uma conexão ativa com o banco SQLite com suporte a STDDEV."""
    target_path = db_path or DEFAULT_DB_PATH
    target_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(target_path)
    conn.row_factory = sqlite3.Row
    # Registra a função agregada STDDEV no SQLite
    conn.create_aggregate("STDDEV", 1, SQLiteStdDev)
    conn.create_aggregate("STDEV", 1, SQLiteStdDev)
    return conn

def execute_query(query: str, params: Optional[tuple] = None, db_path: Optional[Path] = None) -> pd.DataFrame:
    """Executa uma query SELECT e retorna os resultados em um DataFrame do Pandas."""
    with get_connection(db_path) as conn:
        return pd.read_sql_query(query, conn, params=params)

def execute_script(script_path: Path, db_path: Optional[Path] = None) -> None:
    """Executa um arquivo SQL de DDL ou DML no banco SQLite."""
    with open(script_path, "r", encoding="utf-8") as f:
        sql_content = f.read()
    with get_connection(db_path) as conn:
        conn.executescript(sql_content)
        conn.commit()

if __name__ == "__main__":
    print(f"Database path configurado para: {DEFAULT_DB_PATH}")