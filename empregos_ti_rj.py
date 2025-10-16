# === [1] Importação de bibliotecas ===
from pyspark.sql import SparkSession
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import os

# === [2] Configurar caminho do arquivo (ajuste automático) ===
base_dir = os.path.dirname(os.path.abspath(__file__))
arquivo = os.path.join(base_dir, "empregos_ti_texto.csv")

# === [3] Criar sessão Spark ===
spark = SparkSession.builder \
    .appName("EmpregosTI_RJ") \
    .getOrCreate()

# === [4] Ler o arquivo CSV com Spark ===
df_spark = spark.read.csv(arquivo, header=True, inferSchema=True)

print("=== [PySpark] Schema detectado ===")
df_spark.printSchema()

print("=== [PySpark] Primeiras linhas ===")
df_spark.show(10, truncate=False)

# === [5] Converter para Pandas para análise visual ===
df = df_spark.toPandas()

print("\n=== [Pandas] Informações iniciais ===")
print(df.info())
print(df.head())

# === [6] Estatísticas descritivas ===
print("\n=== [Pandas] Estatísticas descritivas ===")
print(df.describe())

# === [7] Gráfico de empregos criados e perdidos ===
ax = df.plot(
    x="Local",
    y=["Empregos Criados", "Empregos Perdidos"],
    kind="bar",
    figsize=(12,6)
)

ax.set_title("Empregos Criados x Perdidos (TI e Geral)", fontsize=14)
ax.set_ylabel("Quantidade de Empregos")

# Formatando os números com separador de milhares
ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))

# Adicionando rótulos acima de cada barra
for p in ax.patches:
    ax.annotate(f'{int(p.get_height()):,}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='bottom', fontsize=9)

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# === [8] Gráfico de saldo de empregos ===
ax2 = df.plot(
    x="Local",
    y="Saldo",
    kind="bar",
    color="green",
    figsize=(12,6)
)

ax2.set_title("Saldo de Empregos", fontsize=14)
ax2.set_ylabel("Saldo")

# Formatando os números com separador de milhares
ax2.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))

# Adicionando rótulos acima das barras
for p in ax2.patches:
    ax2.annotate(f'{int(p.get_height()):,}',
                 (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='bottom', fontsize=9)

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
