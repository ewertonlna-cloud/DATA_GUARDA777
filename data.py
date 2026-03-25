import pandas as pd
import numpy as np
import random
from datetime import date, timedelta

random.seed(42)
np.random.seed(42)

produtos = ["Notebook", "Smartphone", "Tablet", "Monitor", "Teclado", "Mouse", "Headphone", "Webcam"]
regioes = ["Norte", "Sul", "Sudeste", "Nordeste", "Centro-Oeste"]
vendedores = ["Ana", "Bruno", "Carlos", "Diana", "Eduardo"]

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
print("✅ vendas.csv gerado com sucesso!")
