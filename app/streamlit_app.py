"""
Dangerous Data: MJ Statistics - Web App Interativo
MBA em Data Science, IA e Analytics (USP/ESALQ)
"""

import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração do caminho raiz para importar módulos de src/
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from src.database import execute_query, DEFAULT_DB_PATH

# Configuração da Página
st.set_page_config(
    page_title="Dangerous Data | MJ Statistics",
    page_icon="🕺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título Principal
st.title("🕺 Dangerous Data: MJ Statistics")
st.markdown("**A Anatomia Estatística da Maior Força Pop da História** | *MBA em Data Science, IA e Analytics — USP/ESALQ*")

# Verificação do Banco de Dados
if not DEFAULT_DB_PATH.exists():
    st.error("⚠️ Banco SQLite `mj_analytics.db` não encontrado. Execute `py src/etl.py` no terminal para compilar os dados.")
    st.stop()

# Barra Lateral
with st.sidebar:
    st.header("⚙️ Sobre o Projeto")
    st.markdown("""
    Este Web App consome dados de um banco relacional **SQLite (Star Schema)** 
    modelado com integridade referencial a partir de dados históricos da carreira solo de Michael Jackson.
    """)
    st.divider()
    st.caption("Autor: **Eric Renato**")
    st.caption("Repositório: [GitHub](https://github.com/EricRenato/dangerous_data_mj_statistics)")

# Abas Principais
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👑 The Commercial Empire",
    "📈 Chart Performance",
    "🎬 The Audiovisual Impact",
    "🏎️ Bar Chart Race",
    "🤖 Text-to-SQL (GenAI)"
])

# -------------------------------------------------------------
# ABA 1: O Império Comercial (Álbuns & Turnês)
# -------------------------------------------------------------
with tab1:
    st.subheader("Vendas Globais de Álbuns & Receita de Turnês")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Álbum Mais Vendido", "Thriller (70M)")
    col2.metric("Semanas #1 Billboard (Thriller)", "37 semanas")
    col3.metric("Maior Turnê (Receita)", "HIStory ($165M)")
    col4.metric("Público Total em Turnês", "12,8M espectadores")
    
    st.markdown("---")
    
    df_albuns = execute_query("""
        SELECT nome_album, ano_lancamento, vendas_mi, grammys, semanas_topo_billboard 
        FROM dim_album 
        ORDER BY ano_lancamento ASC;
    """)
    
    fig_vendas = px.bar(
        df_albuns, 
        x="nome_album", 
        y="vendas_mi",
        color="vendas_mi",
        text="vendas_mi",
        title="Vendas Mundiais Estimadas por Álbum Solo (Milhões de Cópias)",
        labels={"vendas_mi": "Vendas (mi)", "nome_album": "Álbum"},
        color_continuous_scale="Purples"
    )
    fig_vendas.update_traces(texttemplate='%{text}M', textposition="outside")
    st.plotly_chart(fig_vendas, use_container_width=True)
    
    st.subheader("Desempenho Financeiro das Turnês Mundiais")
    df_turnes = execute_query("""
        SELECT nome_turne AS Turnê, 
               ano_inicio || ' - ' || ano_fim AS Período, 
               num_shows AS Shows, 
               publico_total_mi AS 'Público (mi)', 
               receita_total_usd_mi AS 'Receita Total (USD mi)',
               ROUND(receita_total_usd_mi / num_shows, 2) AS 'Receita Média / Show (USD mi)',
               patrocinador AS Patrocinador
        FROM fato_turne 
        ORDER BY ano_inicio ASC;
    """)
    st.dataframe(df_turnes, use_container_width=True)

# -------------------------------------------------------------
# ABA 2: Chart Performance (Billboard Hot 100 vs UK)
# -------------------------------------------------------------
with tab2:
    st.subheader("Performance nas Paradas: Billboard Hot 100 (EUA) vs UK Singles")
    
    df_singles = execute_query("""
        SELECT s.nome_single, a.nome_album, s.ano_lancamento, s.peak_eua, s.peak_uk, s.semanas_chart_eua
        FROM fato_single s
        JOIN dim_album a ON s.id_album = a.id_album
        WHERE s.peak_eua IS NOT NULL AND s.peak_uk IS NOT NULL;
    """)
    
    fig_scatter = px.scatter(
        df_singles,
        x="peak_eua",
        y="peak_uk",
        text="nome_single",
        color="nome_album",
        size="semanas_chart_eua",
        title="Peak EUA vs Peak UK (Tamanho da bolha = Semanas no Chart dos EUA)",
        labels={"peak_eua": "Melhor Posição EUA (1 = topo)", "peak_uk": "Melhor Posição UK (1 = topo)", "nome_album": "Álbum"}
    )
    fig_scatter.update_traces(textposition="top center")
    fig_scatter.update_xaxes(autorange="reversed")
    fig_scatter.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_scatter, use_container_width=True)

# -------------------------------------------------------------
# ABA 3: Impacto Audiovisual (Clipes e Orçamentos)
# -------------------------------------------------------------
with tab3:
    st.subheader("A Revolução dos Curta-Metragens Musicais")
    
    df_clipes = execute_query("""
        SELECT s.nome_single, a.nome_album, d.nome_diretor, c.orcamento_usd_mi, c.duracao_min, c.tipo, c.premiacao
        FROM fato_clipe c
        JOIN fato_single s ON c.id_single = s.id_single
        JOIN dim_album a ON s.id_album = a.id_album
        JOIN dim_diretor d ON c.id_diretor = d.id_diretor
        ORDER BY c.orcamento_usd_mi DESC;
    """)
    
    fig_clipes = px.bar(
        df_clipes.head(10),
        x="nome_single",
        y="orcamento_usd_mi",
        color="nome_diretor",
        text="orcamento_usd_mi",
        title="Top 10 Clipes por Orçamento Estimado de Produção (USD Milhões)",
        labels={"orcamento_usd_mi": "Orçamento (USD mi)", "nome_single": "Single", "nome_diretor": "Diretor"}
    )
    fig_clipes.update_traces(texttemplate='$%{text}M', textposition="outside")
    st.plotly_chart(fig_clipes, use_container_width=True)
    
    st.markdown("#### Detalhes Técnicos das Obras Audiovisuais")
    st.dataframe(df_clipes, use_container_width=True)

# -------------------------------------------------------------
# ABA 4: Bar Chart Race
# -------------------------------------------------------------
with tab4:
    st.subheader("Evolução Acumulada de Vendas (1979 - 2001+)")
    st.info("Aqui será renderizada a animação da corrida de vendas acumuladas entre os álbuns ao longo das décadas.")

# -------------------------------------------------------------
# ABA 5: GenAI (Text-to-SQL)
# -------------------------------------------------------------
with tab5:
    st.subheader("Dangerous Data Q&A — Chatbot com Text-to-SQL")
    st.markdown("Consulte a base de dados relacional fazendo perguntas em português ou inglês.")
    
    pergunta = st.text_input("Digite sua pergunta:", placeholder="Ex: Quais singles alcançaram a primeira posição na Billboard?")
    if st.button("Consultar Base"):
        st.info("Módulo de GenAI pronto para ser integrado com a API de LLM.")