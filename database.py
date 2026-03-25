import pandas as pd
import sqlite3

def get_connection(csv_path="vendas.csv"):
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(":memory:")
    df.to_sql("vendas", conn, index=False, if_exists="replace")
    return conn

def query(sql, csv_path="vendas.csv"):
    conn = get_connection(csv_path)
    return pd.read_sql_query(sql, conn)

# --- Queries prontas ---

def total_por_produto():
    return query("""
        SELECT produto,
               SUM(quantidade) AS unidades_vendidas,
               SUM(total)      AS receita_total
        FROM vendas
        GROUP BY produto
        ORDER BY receita_total DESC
    """)

def total_por_regiao():
    return query("""
        SELECT regiao,
               SUM(total) AS receita_total
        FROM vendas
        GROUP BY regiao
        ORDER BY receita_total DESC
    """)

def vendas_por_mes():
    return query("""
        SELECT mes,
               COUNT(*)   AS num_vendas,
               SUM(total) AS receita_total
        FROM vendas
        GROUP BY mes
        ORDER BY mes
    """)

def top_vendedores():
    return query("""
        SELECT vendedor,
               COUNT(*)   AS num_vendas,
               SUM(total) AS receita_total
        FROM vendas
        GROUP BY vendedor
        ORDER BY receita_total DESC
    """)
