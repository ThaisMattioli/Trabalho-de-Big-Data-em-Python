import pandas as pd
import matplotlib.pyplot as plt

# === [1] Caminho do arquivo CSV ===
caminho_csv = r"C:\Projetos\projetoBigData\projetoBigData\empregos_ti_texto.csv"

# === [2] Leitura do CSV com separador ===
df = pd.read_csv(caminho_csv, sep=';', encoding='latin1')

# === [3] Conferir colunas e primeiras linhas ===
print("=== Colunas do DataFrame ===")
print(df.columns, "\n")

print("=== Primeiras linhas ===")
print(df.head(), "\n")

# === [4] Estatísticas descritivas ===
print("=== Estatísticas descritivas ===")
print(df.describe(include='all'), "\n")

# === [5] Gráfico de Empregos Criados x Empregos Perdidos ===
fig, ax = plt.subplots(figsize=(10, 6))
df.plot(
    x='Local',
    y=['Empregos Criados', 'Empregos Perdidos'],
    kind='bar',
    color=['#42B3ED', '#EB821C'],
    ax=ax
)

ax.set_title("Empregos Criados x Empregos Perdidos", fontsize=14)
ax.set_ylabel("Quantidade de Empregos")

# Formatar números no eixo Y com separador de milhares
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))

# Adicionar rótulos em cima de cada barra
for p in ax.patches:
    altura = int(p.get_height())
    ax.annotate(f"{altura:,}".replace(",", "."),
                (p.get_x() + p.get_width() / 2, altura),
                ha='center', va='bottom', fontsize=9)

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
