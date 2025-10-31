import pandas as pd
import matplotlib.pyplot as plt

caminho_csv = r"C:\Projetos\projetoBigData\projetoBigData\empregos_ti_texto.csv"

df = pd.read_csv(caminho_csv, sep=';', encoding='latin1')

print("=== Colunas do DataFrame ===")
print(df.columns, "\n")

print("=== Primeiras linhas ===")
print(df.head(), "\n")

print("=== Estatísticas descritivas ===")
print(df.describe(include='all'), "\n")

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

ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))

for p in ax.patches:
    altura = int(p.get_height())
    ax.annotate(f"{altura:,}".replace(",", "."),
                (p.get_x() + p.get_width() / 2, altura),
                ha='center', va='bottom', fontsize=9)

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

