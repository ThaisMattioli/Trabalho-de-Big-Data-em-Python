from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent
EXCEL = BASE_DIR / "pnad_covid_19_divulgacao_semanal.ots"

OUT_DIR = BASE_DIR / "outputs_covid"
OUT_DIR.mkdir(exist_ok=True, parents=True)

print("📄 Lendo planilha COVID-19...")
df = pd.read_excel(EXCEL, sheet_name="Trabalho", header=5)

print("Formato bruto:", df.shape)
print("\n🔎 Colunas lidas da aba 'Trabalho':")
print(list(df.columns))


def pick_col(cols, *fragmentos):
    cols = list(cols)
    for c in cols:
        nome = str(c).lower()
        if all(frag.lower() in nome for frag in fragmentos):
            return c
    raise KeyError(f"Não encontrei coluna contendo {fragmentos} em {cols}")

col_indicador = "Indicador"

col_unid = "Abertura Territorial"


print("\n✅ Colunas de identificação:")
print("   Indicador:", col_indicador)
print("   Unidade  :", col_unid)

colunas_semana = [
    c for c in df.columns
    if ("semana" in str(c).lower()) and ("situação" not in str(c).lower())
]

print("\n📅 Colunas de semanas identificadas:")
for c in colunas_semana:
    print("  -", c)



mask_indicador = df[col_indicador].astype(str).str.contains(
    "Taxa de desocupação", case=False, na=False
)

mask_brasil = df[col_unid].astype(str).str.contains(
    "Brasil", case=False, na=False
)

df_taxa = df[mask_indicador & mask_brasil].copy()

print("\n🧾 Linhas encontradas para 'Taxa de desocupação' – Brasil:")
print(df_taxa[[col_indicador, col_unid]].head())

if df_taxa.empty:
    print("\n⚠️ Nenhuma linha encontrada com 'Taxa de desocupação' e 'Brasil'.")
    print("   Veja acima as linhas de amostra para ajustar o filtro, se necessário.")
    raise SystemExit(1)



df_long = df_taxa.melt(
    id_vars=[col_indicador, col_unid],
    value_vars=colunas_semana,
    var_name="semana",
    value_name="valor",
)

df_long["valor"] = (
    df_long["valor"]
    .astype(str)
    .str.replace("%", "", regex=False)
    .str.replace(",", ".", regex=False)
    .str.strip()
)

df_long = df_long[df_long["valor"].ne("-")]  # remove '-'
df_long["valor"] = pd.to_numeric(df_long["valor"], errors="coerce")
df_long = df_long.dropna(subset=["valor"])

df_long["semana_num"] = (
    df_long["semana"].astype(str).str.extract(r"(\d+)", expand=False)
)
df_long["semana_num"] = pd.to_numeric(df_long["semana_num"], errors="coerce")

df_long = df_long.sort_values("semana_num").reset_index(drop=True)

print("\n📊 Prévia da série tratada:")
print(df_long.head())


print("\n📈 Estatísticas — Taxa de Desocupação (Brasil, semanal):")
print("   Mínimo:", df_long["valor"].min())
print("   Máximo:", df_long["valor"].max())
print("   Média :", df_long["valor"].mean())


plt.figure(figsize=(12, 6))

plt.bar(
    df_long["semana_num"],
    df_long["valor"]
)

rotulos = df_long["semana"].fillna(df_long["semana_num"])
plt.xticks(df_long["semana_num"], rotulos, rotation=45, ha="right")

plt.grid(axis="y", alpha=0.3)
plt.title("Taxa de Desocupação (%) – PNAD COVID-19 (Brasil, semanal)")
plt.xlabel("Semana")
plt.ylabel("Taxa de desocupação (%)")
plt.tight_layout()

grafico_path = OUT_DIR / "pnad_covid_taxa_desocupacao_brasil_semana.png"
plt.savefig(grafico_path, dpi=150)
plt.show()

print("\n📊 Gráfico salvo em:", grafico_path)

csv_path = OUT_DIR / "pnad_covid_taxa_desocupacao_brasil_semana.csv"
df_long.to_csv(csv_path, index=False, float_format="%.4f")

print("💾 CSV salvo em:", csv_path)
print("\n✅ Análise da PNAD COVID-19 concluída com sucesso.")
