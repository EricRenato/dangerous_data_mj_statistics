"""
01_data_wrangling.py
=====================
Etapa 1 do portfólio — Data Wrangling do MJ Dataset Oficial v2.

Objetivo
--------
Transformar os dados BRUTOS exportados do Excel (com imperfeições reais do
mundo: decimais em padrão brasileiro, valores faltantes marcados com "—",
métricas de álbum duplicadas em cada single, etc.) em tabelas TIDY, prontas
para análise estatística.

Princípios de "tidy data" (Wickham, 2014):
    1. Cada variável é uma coluna.
    2. Cada observação é uma linha.
    3. Cada tipo de unidade observacional é uma tabela.

Entrada : data/raw/*.csv
Saída   : data/processed/*.csv  (+ relatório no console)

Uso:
    python analysis/python/01_data_wrangling.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

# Caminhos relativos à raiz do repositório (script roda de qualquer lugar)
ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

# Marcadores de valor faltante usados na fonte original
NA_TOKENS = ["—", "-", "", "NA", "N/A", "nan"]


def br_to_float(series: pd.Series) -> pd.Series:
    """Converte número em padrão brasileiro ('4,98') para float (4.98).

    Também transforma os marcadores de faltante (NA_TOKENS) em NaN.
    """
    cleaned = (
        series.astype("string")
        .str.strip()
        .replace(NA_TOKENS, pd.NA)
        .str.replace(".", "", regex=False)   # separador de milhar, se houver
        .str.replace(",", ".", regex=False)  # vírgula decimal -> ponto
    )
    return pd.to_numeric(cleaned, errors="coerce")


def to_int_nullable(series: pd.Series) -> pd.Series:
    """Inteiro que aceita faltante (tipo Int64 do pandas)."""
    cleaned = series.astype("string").str.strip().replace(NA_TOKENS, pd.NA)
    return pd.to_numeric(cleaned, errors="coerce").astype("Int64")


def yes_no_to_bool(series: pd.Series) -> pd.Series:
    """'Sim'/'Não' -> booleano."""
    return series.astype("string").str.strip().str.lower().map(
        {"sim": True, "não": False, "nao": False}
    )


# ---------------------------------------------------------------------------
# 1) SINGLES — a tabela central
# ---------------------------------------------------------------------------
def wrangle_singles() -> pd.DataFrame:
    df = pd.read_csv(RAW / "mj_singles_raw.csv", dtype="string")

    # 1.1 Tipagem correta de cada coluna
    df["album_id"] = to_int_nullable(df["album_id"])
    df["album_year"] = to_int_nullable(df["album_year"])
    df["single_year"] = to_int_nullable(df["single_year"])
    df["tracks"] = to_int_nullable(df["tracks"])
    df["album_grammys"] = to_int_nullable(df["album_grammys"])
    df["album_weeks_no1_bb200"] = to_int_nullable(df["album_weeks_no1_bb200"])
    df["album_sales_mi"] = br_to_float(df["album_sales_mi"])
    df["duration_min"] = br_to_float(df["duration_min"])
    df["peak_us"] = to_int_nullable(df["peak_us"])
    df["peak_uk"] = to_int_nullable(df["peak_uk"])
    df["weeks_chart_us"] = to_int_nullable(df["weeks_chart_us"])
    df["has_video"] = yes_no_to_bool(df["has_video"])

    # 1.2 Limpeza de texto
    for col in ["album", "single", "genre", "award"]:
        df[col] = df[col].astype("string").str.strip()
    df["award"] = df["award"].replace(NA_TOKENS, pd.NA)

    # 1.3 Variáveis derivadas úteis para a análise
    #     genre_primary = primeiro gênero antes da "/" (reduz a cardinalidade)
    df["genre_primary"] = df["genre"].str.split("/").str[0].str.strip()
    #     reached_no1 = single chegou ao topo da Billboard Hot 100?
    df["reached_no1_us"] = df["peak_us"] == 1
    #     decade do lançamento do single
    df["decade"] = (df["single_year"] // 10 * 10).astype("Int64")

    # 1.4 Chave de identificação corrigida ("atrelar ao ID" — nota do autor):
    #     single_id sequencial e estável, ancorado ao álbum.
    df = df.sort_values(["album_id", "single_year", "single"]).reset_index(drop=True)
    df.insert(0, "single_id", range(1, len(df) + 1))

    # Ordena colunas de forma legível
    cols = [
        "single_id", "album_id", "album", "album_year", "single", "single_year",
        "decade", "genre", "genre_primary", "duration_min", "peak_us", "peak_uk",
        "weeks_chart_us", "reached_no1_us", "has_video", "award",
        # métricas de ÁLBUM (repetidas por single — usar com cuidado!)
        "tracks", "album_sales_mi", "album_grammys", "album_weeks_no1_bb200",
    ]
    return df[cols]


# ---------------------------------------------------------------------------
# 2) ALBUMS — dimensão (1 linha por álbum). Resolve a pseudo-replicação:
#    vendas/Grammys/semanas são do ÁLBUM, não do single.
# ---------------------------------------------------------------------------
def wrangle_albums() -> pd.DataFrame:
    df = pd.read_csv(RAW / "mj_albums_raw.csv", dtype="string")
    df["album_id"] = to_int_nullable(df["album_id"])
    df["album_year"] = to_int_nullable(df["album_year"])
    df["tracks"] = to_int_nullable(df["tracks"])
    df["album_grammys"] = to_int_nullable(df["album_grammys"])
    df["album_weeks_no1_bb200"] = to_int_nullable(df["album_weeks_no1_bb200"])
    df["album_sales_mi"] = br_to_float(df["album_sales_mi"])
    df["album"] = df["album"].astype("string").str.strip()
    return df.sort_values("album_id").reset_index(drop=True)


# ---------------------------------------------------------------------------
# 3) TOURS
# ---------------------------------------------------------------------------
def wrangle_tours() -> pd.DataFrame:
    df = pd.read_csv(RAW / "mj_tours_raw.csv", dtype="string")
    for c in ["year_start", "year_end", "shows", "countries", "cities", "audience_avg_show",
              "revenue_total_usd_mi"]:
        df[c] = to_int_nullable(df[c])
    df["audience_total_mi"] = br_to_float(df["audience_total_mi"])
    df["revenue_avg_show_usd_mi"] = br_to_float(df["revenue_avg_show_usd_mi"])
    for c in ["tour", "tour_id", "sponsor", "note"]:
        df[c] = df[c].astype("string").str.strip().replace(NA_TOKENS, pd.NA)
    # KPI derivado: receita por país
    df["revenue_per_country_usd_mi"] = (
        df["revenue_total_usd_mi"] / df["countries"]
    ).round(2)
    return df.reset_index(drop=True)


# ---------------------------------------------------------------------------
# 4) MILESTONES
# ---------------------------------------------------------------------------
def wrangle_milestones() -> pd.DataFrame:
    df = pd.read_csv(RAW / "mj_milestones_raw.csv", dtype="string")
    df["year"] = to_int_nullable(df["year"])
    for c in ["milestone_id", "milestone", "category", "source", "description", "still_valid"]:
        df[c] = df[c].astype("string").str.strip()
    # Normaliza status: Sim / Não-superado -> categoria limpa
    df["still_valid_flag"] = df["still_valid"].str.lower().str.startswith("sim")
    return df.reset_index(drop=True)


# ---------------------------------------------------------------------------
# 5) SALES TIMELINE — wide -> long (melt). Exemplo clássico de tidy data.
# ---------------------------------------------------------------------------
def wrangle_sales_timeline() -> pd.DataFrame:
    df = pd.read_csv(RAW / "mj_sales_timeline_raw.csv", dtype="string")
    df["year"] = to_int_nullable(df["year"])
    album_cols = [c for c in df.columns if c != "year"]
    for c in album_cols:
        df[c] = br_to_float(df[c])

    long = df.melt(
        id_vars="year", value_vars=album_cols,
        var_name="album", value_name="cumulative_sales_mi",
    )
    # Remove anos anteriores ao lançamento (eram "—" -> NaN)
    long = long.dropna(subset=["cumulative_sales_mi"]).reset_index(drop=True)
    long = long.sort_values(["album", "year"]).reset_index(drop=True)
    return long


# ---------------------------------------------------------------------------
# Relatório de qualidade (data profiling) — o que todo wrangling deve mostrar
# ---------------------------------------------------------------------------
def quality_report(name: str, df: pd.DataFrame) -> None:
    print(f"\n{'='*70}\n{name}  —  {df.shape[0]} linhas x {df.shape[1]} colunas\n{'='*70}")
    nulls = df.isna().sum()
    nulls = nulls[nulls > 0]
    if len(nulls):
        print("Valores faltantes (esperados):")
        for col, n in nulls.items():
            print(f"   - {col}: {n}")
    else:
        print("Sem valores faltantes.")


def main() -> None:
    outputs = {
        "singles": wrangle_singles(),
        "albums": wrangle_albums(),
        "tours": wrangle_tours(),
        "milestones": wrangle_milestones(),
        "sales_timeline": wrangle_sales_timeline(),
    }

    for name, df in outputs.items():
        path = OUT / f"mj_{name}.csv"
        df.to_csv(path, index=False, encoding="utf-8")
        quality_report(name, df)
        print(f"   -> salvo em {path.relative_to(ROOT)}")

    # Verificação de integridade referencial: todo single aponta para um álbum válido
    singles, albums = outputs["singles"], outputs["albums"]
    orfaos = set(singles["album_id"]) - set(albums["album_id"])
    assert not orfaos, f"Singles órfãos (album_id sem álbum): {orfaos}"
    print(f"\n[OK] Integridade referencial: {len(singles)} singles ligados a "
          f"{albums.shape[0]} álbuns. Nenhum órfão.")


if __name__ == "__main__":
    main()
