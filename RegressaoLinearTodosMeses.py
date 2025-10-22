import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# === 1. Carregamos os dados ===
df = pd.read_csv(r"C:\Projetos\projetoBigData\projetoBigData\niteroi_2020_2025_todos_meses.csv")

# === 2. Removemos as linhas sem valor ===
df = df.dropna(subset=["Valor"])

# === 3. Criamos uma variável de tempo contínua (mês desde o início) ===
df = df.sort_values(["Ano", "Mes"]).reset_index(drop=True)
df["tempo"] = np.arange(len(df))

# === 4. Definimos X (tempo) e Y (Valor) ===
X = df["tempo"].values.reshape(-1, 1)
y = df["Valor"].values

# === 5. Criando o modelo de regressão ===
modelo = LinearRegression()
modelo.fit(X, y)

# === 6. Previsões ===
X_linha = np.linspace(0, len(df) - 1, 200).reshape(-1, 1)
y_prev = modelo.predict(X_linha)

# === 7. Estatísticas descritivas ===
media = df["Valor"].mean()
desvio = df["Valor"].std()
print("\n=== Estatísticas Descritivas ===")
print(f"Média: {media:.2f}")
print(f"Desvio Padrão: {desvio:.2f}")

# === 8. Gráfico de dispersão com regressão linear ===
plt.figure(figsize=(10, 6))
plt.scatter(df["tempo"], df["Valor"], color="#EB821C", label="Dados reais")
plt.plot(X_linha, y_prev, color="#42B3ED", linewidth=2, label="Reta ajustada")
plt.axhline(media, color="gray", linestyle="--", linewidth=1.2, label=f"Média ({media:.2f})")

# Ajuste de rótulos no eixo x
passo = max(1, len(df) // 12)
plt.xticks(df["tempo"][::passo], df["Periodo"][::passo], rotation=45)

plt.xlabel("Período (Ano/Mês)")
plt.ylabel("Valor de desempregados")
plt.title("Regressão Linear: Valor de desempregados em Niterói (2020–2025)")
plt.legend()
plt.tight_layout()
plt.show()

# === 9. Resultados da regressão ===
coef = modelo.coef_[0]
intercepto = modelo.intercept_
r2 = modelo.score(X, y)

print("\n=== Resultados da Regressão Linear ===")
print(f"Coeficiente angular (tendência mensal): {coef:.2f}")
print(f"Intercepto: {intercepto:.2f}")
print(f"R²: {r2:.4f}")

# === 10. Interpretação automática ===
tendencia = "queda" if coef < 0 else "aumento"
print(f"\n📈 Interpretação: Há uma tendência de {tendencia} no número de desempregados em Niterói.")
