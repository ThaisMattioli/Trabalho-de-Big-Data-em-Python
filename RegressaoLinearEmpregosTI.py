import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import os

# === 1. Caminho do arquivo ===
caminho_arquivo = r"C:\Projetos\projetoBigData\projetoBigData\empregos_ti_texto.csv"

# === 2. Leitura inteligente do arquivo ===
ext = os.path.splitext(caminho_arquivo)[1].lower()

try:
    if ext == '.csv':
        try:
            df = pd.read_csv(caminho_arquivo, sep=';', encoding='latin1')
        except Exception:
            df = pd.read_csv(caminho_arquivo, sep=',', encoding='utf-8')
    elif ext in ['.xls', '.xlsx']:
        df = pd.read_excel(caminho_arquivo)
    elif ext == '.ods':
        df = pd.read_excel(caminho_arquivo, engine='odf')
    else:
        raise ValueError(f"Formato de arquivo não reconhecido: {ext}")
    print("✅ Arquivo carregado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao ler o arquivo: {e}")
    raise SystemExit

# === 3. Conferir colunas disponíveis ===
print("\n=== Colunas encontradas ===")
print(df.columns)

# === 4. Limpar e preparar os dados ===
# Garantir que as colunas relevantes existam
coluna_alvo = "Empregos Perdidos"
if coluna_alvo not in df.columns:
    raise ValueError(f"A coluna '{coluna_alvo}' não foi encontrada no arquivo.")

# Converter para numérico e remover valores inválidos
df[coluna_alvo] = pd.to_numeric(df[coluna_alvo], errors="coerce")
df = df.dropna(subset=[coluna_alvo])

# Criar índice contínuo (serve como 'tempo' ou eixo de regressão)
df = df.reset_index(drop=True)
df["tempo"] = np.arange(len(df))

# === 5. Definir variáveis para regressão ===
X = df[["tempo"]].values
y = df[coluna_alvo].values

# === 6. Criar e ajustar o modelo ===
modelo = LinearRegression()
modelo.fit(X, y)

# === 7. Fazer previsões ===
X_linha = np.linspace(0, len(df)-1, 200).reshape(-1, 1)
y_prev = modelo.predict(X_linha)

# === 8. Gráfico ===
plt.figure(figsize=(10, 6))
plt.scatter(df["tempo"], df[coluna_alvo], color="#EB821C", label="Dados reais")
plt.plot(X_linha, y_prev, color="#42B3ED", linewidth=2, label="Reta ajustada")

# Eixo X com os nomes dos locais, se existir a coluna 'Local'
if "Local" in df.columns:
    plt.xticks(df["tempo"], df["Local"], rotation=45)
    plt.xlabel("Local")
else:
    plt.xlabel("Índice (Tempo)")

plt.ylabel(coluna_alvo)
plt.title("Regressão Linear: Empregos Perdidos em setores de TI")
plt.legend()
plt.tight_layout()
plt.show()

# === 9. Exibir resultados do modelo ===
print("\n=== Resultados da Regressão Linear ===")
print(f"Coeficiente angular (tendência): {modelo.coef_[0]:.2f}")
print(f"Intercepto: {modelo.intercept_:.2f}")
print(f"R² (qualidade do ajuste): {modelo.score(X, y):.4f}")
