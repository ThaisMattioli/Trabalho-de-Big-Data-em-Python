import pandas as pd
import matplotlib.pyplot as plt

caminho_csv = r"C:\Projetos\projetoBigData\projetoBigData1\empregos_ti_texto.csv"

df = pd.read_csv(caminho_csv, sep=';', encoding='latin1')

print("=== Colunas do DataFrame ===")
print(df.columns, "\n")

print("=== Primeiras linhas ===")
print(df.head(), "\n")

print("=== Estatísticas descritivas ===")
print(df.describe(include='all'), "\n")


df['Local'] = df['Local'].replace({
    "Brasil (geral)": "Brasil – Geral",
    "Brasil (TI)": "Brasil – TI",
    "Brasil (maio)": "Brasil – Maio (Geral)",
    "Brasil (maio - TI)": "Brasil – Maio (TI)",
    "Brasil (maio -TI)": "Brasil – Maio (TI)",        
    "Estado do Rio de Janeiro (geral)": "RJ – Geral",
})


ordem = [
    "Brasil – Geral",
    "Brasil – Maio (Geral)",
    "Brasil – TI",
    "Brasil – Maio (TI)",
    "RJ – Geral"
]

df = df.set_index("Local").reindex(ordem).reset_index()


fig, ax = plt.subplots(figsize=(12, 6))
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
    altura = p.get_height()
    try:
        altura_int = int(altura)
    except Exception:
        altura_int = 0
    ax.annotate(
        f"{altura_int:,}".replace(",", "."),
        (p.get_x() + p.get_width() / 2, altura if not pd.isna(altura) else 0),
        ha='center', va='bottom', fontsize=9
    )

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
