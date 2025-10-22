import pandas as pd

# Lê o CSV
df = pd.read_csv(r"C:\Users\thais\Downloads\niteroi_2020_2025_todos_meses.csv")

# Verifica linhas e as colunas disponíveis
print("Colunas disponíveis:")
print(df.columns)
print("\nPrimeiras linhas:")
print(df.head())

# --- Frequência-período ---
print("\nDistribuição de frequência - PERÍODO")
freq_periodo = df['Periodo'].value_counts().sort_index()
freq_relativa_periodo = (freq_periodo / freq_periodo.sum()) * 100
freq_acumulada_periodo = freq_periodo.cumsum()

for valor, f, fr, fa in zip(freq_periodo.index, freq_periodo, freq_relativa_periodo, freq_acumulada_periodo):
    print(f"Valor: {valor} | Freq: {f:4d} | Freq%: {fr:5.2f}% | Acumulada: {fa}")

# --- Frequência-ano ---
print("\nDistribuição de frequência - ANO")
freq_ano = df['Ano'].value_counts().sort_index()
freq_relativa_ano = (freq_ano / freq_ano.sum()) * 100
freq_acumulada_ano = freq_ano.cumsum()

for valor, f, fr, fa in zip(freq_ano.index, freq_ano, freq_relativa_ano, freq_acumulada_ano):
    print(f"Valor: {valor} | Freq: {f:4d} | Freq%: {fr:5.2f}% | Acumulada: {fa}")
