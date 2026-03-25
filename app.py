import streamlit as st
import pandas as pd
import database as db

st.set_page_config(page_title="Dashboard de Vendas", page_icon="📊", layout="wide")

st.title("📊 Dashboard de Vendas — 2024")
st.caption("Projeto de portfólio | Pandas · SQL · Streamlit")

# --- Carrega dados brutos ---
@st.cache_data
def carregar_dados():
    return pd.read_csv("vendas.csv")

df = carregar_dados()

# --- KPIs no topo ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Vendas", f"{len(df):,}")
col2.metric("Receita Total", f"R$ {df['total'].sum():,.0f}")
col3.metric("Ticket Médio", f"R$ {df['total'].mean():,.0f}")
col4.metric("Produtos", df['produto'].nunique())

st.divider()

# --- Filtros na sidebar ---
st.sidebar.header("🔍 Filtros")
regioes = st.sidebar.multiselect("Região", df["regiao"].unique(), default=df["regiao"].unique())
produtos = st.sidebar.multiselect("Produto", df["produto"].unique(), default=df["produto"].unique())

df_filtrado = df[df["regiao"].isin(regioes) & df["produto"].isin(produtos)]

# --- Gráficos ---
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Receita por Produto")
    prod = db.total_por_produto()
    st.bar_chart(prod.set_index("produto")["receita_total"])

with col_b:
    st.subheader("Receita por Região")
    reg = db.total_por_regiao()
    st.bar_chart(reg.set_index("regiao")["receita_total"])

st.subheader("Evolução Mensal das Vendas")
mes = db.vendas_por_mes()
st.line_chart(mes.set_index("mes")["receita_total"])

# --- Tabelas SQL ---
st.divider()
st.subheader("🗃️ Consultas SQL em tempo real")

tab1, tab2, tab3 = st.tabs(["Top Vendedores", "Por Produto", "Dados Brutos"])

with tab1:
    st.dataframe(db.top_vendedores(), use_container_width=True)

with tab2:
    st.dataframe(db.total_por_produto(), use_container_width=True)

with tab3:
    st.dataframe(df_filtrado.head(100), use_container_width=True)


---

## 📄 Arquivo 4 — `requirements.txt`

streamlit
pandas
numpy
