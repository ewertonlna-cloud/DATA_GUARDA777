import streamlit as st
import pandas as pd
import numpy as np
import random
import sqlite3
from pathlib import Path

# --- Gera o CSV automaticamente se não existir ---
def gerar_dados():
    random.seed(42)
    np.random.seed(42)
    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor", "Teclado", "Mouse", "Headphone", "Webcam"]
    regioes = ["Norte", "Sul", "Sudeste", "Nordeste", "Centro-Oeste"]
    vendedores = ["Ana", "Bruno", "Carlos", "Diana", "Eduardo"]
    from datetime import date, timedelta
    n = 500
    datas = [date(2024, 1, 1) + timedelta(days=random.randint(0, 364)) for _ in range(n)]
    df = pd.DataFrame({
        "data":       datas,
        "produto":    random.choices(produtos, k=n),
        "regiao":     random.choices(regioes, k=n),
        "vendedor":   random.choices(vendedores, k=n),
        "quantidade": np.random.randint(1, 20, n),
        "preco_unit": np.random.choice([799, 1999, 1499, 999, 199, 149, 299, 249], n),
    })
    df["total"] = df["quantidade"] * df["preco_unit"]
    df["mes"] = pd.to_datetime(df["data"]).dt.month
    df.to_csv("vendas.csv", index=False)

if not Path("vendas.csv").exists():
    gerar_dados()

# --- Funções SQL ---
def query(sql):
    df = pd.read_csv("vendas.csv")
    conn = sqlite3.connect(":memory:")
    df.to_sql("vendas", conn, index=False, if_exists="replace")
    return pd.read_sql_query(sql, conn)

def total_por_produto():
    return query("SELECT produto, SUM(quantidade) AS unidades_vendidas, SUM(total) AS receita_total FROM vendas GROUP BY produto ORDER BY receita_total DESC")

def total_por_regiao():
    return query("SELECT regiao, SUM(total) AS receita_total FROM vendas GROUP BY regiao ORDER BY receita_total DESC")

def vendas_por_mes():
    return query("SELECT mes, COUNT(*) AS num_vendas, SUM(total) AS receita_total FROM vendas GROUP BY mes ORDER BY mes")

def top_vendedores():
    return query("SELECT vendedor, COUNT(*) AS num_vendas, SUM(total) AS receita_total FROM vendas GROUP BY vendedor ORDER BY receita_total DESC")

# --- App ---
st.set_page_config(page_title="Dashboard de Vendas", page_icon="📊", layout="wide")
st.title("📊 Dashboard de Vendas — 2024")
st.caption("Projeto de portfólio | Pandas · SQL · Streamlit")

@st.cache_data
def carregar_dados():
    return pd.read_csv("vendas.csv")

df = carregar_dados()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Vendas", f"{len(df):,}")
col2.metric("Receita Total", f"R$ {df['total'].sum():,.0f}")
col3.metric("Ticket Médio", f"R$ {df['total'].mean():,.0f}")
col4.metric("Produtos", df['produto'].nunique())

st.divider()

st.sidebar.header("🔍 Filtros")
regioes = st.sidebar.multiselect("Região", df["regiao"].unique(), default=list(df["regiao"].unique()))
produtos = st.sidebar.multiselect("Produto", df["produto"].unique(), default=list(df["produto"].unique()))
df_filtrado = df[df["regiao"].isin(regioes) & df["produto"].isin(produtos)]

col_a, col_b = st.columns(2)
with col_a:
    st.subheader("Receita por Produto")
    st.bar_chart(total_por_produto().set_index("produto")["receita_total"])
with col_b:
    st.subheader("Receita por Região")
    st.bar_chart(total_por_regiao().set_index("regiao")["receita_total"])

st.subheader("Evolução Mensal das Vendas")
st.line_chart(vendas_por_mes().set_index("mes")["receita_total"])

st.divider()
st.subheader("🗃️ Consultas SQL em tempo real")
tab1, tab2, tab3 = st.tabs(["Top Vendedores", "Por Produto", "Dados Brutos"])
with tab1:
    st.dataframe(top_vendedores(), use_container_width=True)
with tab2:
    st.dataframe(total_por_produto(), use_container_width=True)
with tab3:
    st.dataframe(df_filtrado.head(100), use_container_width=True)

