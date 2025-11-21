import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

caminho_csv = r"C:\Projetos\projetoBigData\projetoBigData1\niteroi_2020_2025_todos_meses.csv"
df = pd.read_csv(caminho_csv)
print("✅ Arquivo carregado com sucesso!\n")

print("=== Colunas disponíveis ===")
print(df.columns, "\n")

print("=== Primeiras linhas ===")
print(df.head(), "\n")


df = df[df["Mes"].isin([1, 6, 12])]

df = df.sort_values(["Ano", "Mes"]).reset_index(drop=True)

print("\n=== Dados filtrados (jan, jun, dez) ===")
print(df[["Ano", "Mes", "Periodo", "Valor"]])


print("\n=== Distribuição de Frequência - PERÍODO ===")
freq_periodo = df["Periodo"].value_counts().sort_index()
freq_relativa_periodo = (freq_periodo / freq_periodo.sum()) * 100
freq_acumulada_periodo = freq_periodo.cumsum()

for valor, f, fr, fa in zip(freq_periodo.index, freq_periodo, freq_relativa_periodo, freq_acumulada_periodo):
    print(f"Valor: {valor} | Freq: {f:4d} | Freq%: {fr:5.2f}% | Acumulada: {fa}")

print("\n=== Distribuição de Frequência - ANO ===")
freq_ano = df["Ano"].value_counts().sort_index()
freq_relativa_ano = (freq_ano / freq_ano.sum()) * 100
freq_acumulada_ano = freq_ano.cumsum()

for valor, f, fr, fa in zip(freq_ano.index, freq_ano, freq_relativa_ano, freq_acumulada_ano):
    print(f"Ano: {valor} | Freq: {f:4d} | Freq%: {fr:5.2f}% | Acumulada: {fa}")


df = df.dropna(subset=["Valor"])

media = df["Valor"].mean()
desvio = df["Valor"].std()

print("\n=== Estatísticas Descritivas ===")
print(f"Média do Valor: {media:.2f}")
print(f"Desvio Padrão: {desvio:.2f}")

df["tempo"] = np.arange(len(df))

X = df["tempo"].values.reshape(-1, 1)
y = df["Valor"].values

modelo = LinearRegression()
modelo.fit(X, y)


X_linha = np.linspace(0, len(df) - 1, 200).reshape(-1, 1)
y_prev = modelo.predict(X_linha)


plt.figure(figsize=(12, 6))
plt.scatter(df["tempo"], df["Valor"], color="#EB821C", label="Dados reais (jan/jun/dez)")
plt.plot(X_linha, y_prev, color="#42B3ED", linewidth=2, label="Reta ajustada")
plt.axhline(media, color="gray", linestyle="--", linewidth=1.2, label=f"Média ({media:.2f})")

plt.xticks(df["tempo"], df["Periodo"], rotation=45)

plt.xlabel("Período (Ano/Mês)")
plt.ylabel("Valor de desempregados")
plt.title("Regressão Linear: Dados filtrados (Jan, Jun, Dez) — 2020 a 2025")
plt.legend()
plt.tight_layout()
plt.show()


coef = modelo.coef_[0]
intercepto = modelo.intercept_
r2 = modelo.score(X, y)
tendencia = "queda" if coef < 0 else "aumento"

print("\n=== Resultados da Regressão Linear ===")
print(f"Coeficiente angular (tendência por período): {coef:.2f}")
print(f"Intercepto: {intercepto:.2f}")
print(f"R² (qualidade do ajuste): {r2:.4f}")
print(f"\n📈 Interpretação: Há uma tendência de {tendencia} no número de desempregados em Niterói.")
