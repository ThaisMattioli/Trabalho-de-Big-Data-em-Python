import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# === 1️⃣ Leitura do arquivo CSV ===
caminho_csv = r"C:\Projetos\projetoBigData\projetoBigData\niteroi_2020_2025_todos_meses.csv"

df = pd.read_csv(caminho_csv)
print("✅ Arquivo carregado com sucesso!\n")

# === 2️⃣ Conferência das colunas e primeiras linhas ===
print("=== Colunas disponíveis ===")
print(df.columns, "\n")

print("=== Primeiras linhas ===")
print(df.head(), "\n")

# ============================================================
# 🔸 3️⃣ DISTRIBUIÇÃO DE FREQUÊNCIA (PERÍODO E ANO)
# ============================================================

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

# ============================================================
# 🔸 4️⃣ ESTATÍSTICAS DESCRITIVAS (MÉDIA E DESVIO PADRÃO)
# ============================================================

# Remover valores ausentes
df = df.dropna(subset=["Valor"])

media = df["Valor"].mean()
desvio = df["Valor"].std()

print("\n=== Estatísticas Descritivas ===")
print(f"Média do Valor: {media:.2f}")
print(f"Desvio Padrão: {desvio:.2f}")

# ============================================================
# 🔸 5️⃣ REGRESSÃO LINEAR
# ============================================================

# Organizar dados temporais
df = df.sort_values(["Ano", "Mes"]).reset_index(drop=True)
df["tempo"] = np.arange(len(df))

# Definir variáveis independentes (X) e dependentes (y)
X = df["tempo"].values.reshape(-1, 1)
y = df["Valor"].values

# Criar e ajustar modelo
modelo = LinearRegression()
modelo.fit(X, y)

# Fazer previsões
X_linha = np.linspace(0, len(df) - 1, 200).reshape(-1, 1)
y_prev = modelo.predict(X_linha)

# ============================================================
# 🔸 6️⃣ VISUALIZAÇÃO GRÁFICA
# ============================================================

plt.figure(figsize=(10, 6))
plt.scatter(df["tempo"], df["Valor"], color="#EB821C", label="Dados reais")
plt.plot(X_linha, y_prev, color="#42B3ED", linewidth=2, label="Reta ajustada")
plt.axhline(media, color="gray", linestyle="--", linewidth=1.2, label=f"Média ({media:.2f})")

# Eixo X com rótulos de períodos
passo = max(1, len(df) // 12)
plt.xticks(df["tempo"][::passo], df["Periodo"][::passo], rotation=45)

plt.xlabel("Período (Ano/Mês)")
plt.ylabel("Valor de desempregados")
plt.title("Regressão Linear: Valor de desempregados em Niterói (2020–2025)")
plt.legend()
plt.tight_layout()
plt.show()

# ============================================================
# 🔸 7️⃣ RESULTADOS DA REGRESSÃO E INTERPRETAÇÃO
# ============================================================

coef = modelo.coef_[0]
intercepto = modelo.intercept_
r2 = modelo.score(X, y)
tendencia = "queda" if coef < 0 else "aumento"

print("\n=== Resultados da Regressão Linear ===")
print(f"Coeficiente angular (tendência mensal): {coef:.2f}")
print(f"Intercepto: {intercepto:.2f}")
print(f"R² (qualidade do ajuste): {r2:.4f}")
print(f"\n📈 Interpretação: Há uma tendência de {tendencia} no número de desempregados em Niterói.")


