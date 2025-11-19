import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import os

caminho_csv = r"C:\Projetos\projetoBigData\projetoBigData1\empregos_ti_texto.csv"

df = pd.read_csv(caminho_csv, sep=';', encoding='latin1')
print("✅ Arquivo carregado com sucesso!\n")

print("=== Colunas disponíveis ===")
print(df.columns, "\n")

print("=== Primeiras linhas ===")
print(df.head(), "\n")

print("\n=== Distribuição de Frequência - LOCAL ===")
freq_local = df["Local"].value_counts().sort_index()
freq_relativa_local = (freq_local / freq_local.sum()) * 100
freq_acumulada_local = freq_local.cumsum()

for valor, f, fr, fa in zip(freq_local.index, freq_local, freq_relativa_local, freq_acumulada_local):
    print(f"Local: {valor:20s} | Freq: {f:4d} | Freq%: {fr:5.2f}% | Acumulada: {fa}")


for col in ["Empregos Criados", "Empregos Perdidos"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["Empregos Criados", "Empregos Perdidos"])

media_criados = df["Empregos Criados"].mean()
media_perdidos = df["Empregos Perdidos"].mean()
desvio_criados = df["Empregos Criados"].std()
desvio_perdidos = df["Empregos Perdidos"].std()

print("\n=== Estatísticas Descritivas ===")
print(f"Média de Empregos Criados: {media_criados:.2f}")
print(f"Desvio Padrão (Criados): {desvio_criados:.2f}")
print(f"Média de Empregos Perdidos: {media_perdidos:.2f}")
print(f"Desvio Padrão (Perdidos): {desvio_perdidos:.2f}")


df = df.reset_index(drop=True)
df["tempo"] = np.arange(len(df))

X = df[["tempo"]].values
y = df["Empregos Criados"].values

modelo = LinearRegression()
modelo.fit(X, y)

X_linha = np.linspace(0, len(df) - 1, 200).reshape(-1, 1)
y_prev = modelo.predict(X_linha)



plt.figure(figsize=(10, 6))
plt.scatter(df["tempo"], df["Empregos Criados"], color="#42B3ED", label="Empregos Criados (reais)")
plt.plot(X_linha, y_prev, color="#EB821C", linewidth=2, label="Regressão Linear")
plt.axhline(media_criados, color="gray", linestyle="--", linewidth=1.2, label=f"Média ({media_criados:.2f})")

if "Local" in df.columns:
    passo = max(1, len(df) // 10)
    plt.xticks(df["tempo"][::passo], df["Local"][::passo], rotation=45)
    plt.xlabel("Localidade")
else:
    plt.xlabel("Índice (Tempo)")

plt.ylabel("Empregos Criados")
plt.title("Regressão Linear: Evolução de Empregos Criados em TI")
plt.legend()
plt.tight_layout()
plt.show()

coef = modelo.coef_[0]
intercepto = modelo.intercept_
r2 = modelo.score(X, y)
tendencia = "aumento" if coef > 0 else "queda"

print("\n=== Resultados da Regressão Linear ===")
print(f"Coeficiente angular (tendência): {coef:.2f}")
print(f"Intercepto: {intercepto:.2f}")
print(f"R² (qualidade do ajuste): {r2:.4f}")
print(f"\n📈 Interpretação: Há uma tendência de {tendencia} na criação de empregos na área de TI.")

