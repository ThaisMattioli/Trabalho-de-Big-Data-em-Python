from pyspark.sql import SparkSession
import pandas as pd
import matplotlib.pyplot as plt
import os
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"


spark = SparkSession.builder \
    .appName("NiteroiBigData") \
    .master("local[*]") \
    .getOrCreate()

arquivo = "projetoBigData/niteroi_2020_2025_todos_meses.csv"
df = spark.read.csv(arquivo, header=True, inferSchema=True)

print("=== [PySpark] Schema detectado ===")
df.printSchema()

print("=== [PySpark] Primeiras linhas ===")
df.show(10, truncate=False)

print("=== [PySpark] Dados de 2025 ===")
df.filter(df["Ano"] == 2025).show()

print("=== [PySpark] Média de desemprego por ano (ordenado) ===")
media_por_ano = df.groupBy("Ano").avg("Valor").orderBy("Ano", ascending=False)

media_por_ano = media_por_ano.withColumnRenamed("avg(Valor)", "Media_Desemprego")
media_por_ano.show()


media_pandas = media_por_ano.toPandas()

print("\n=== [Pandas] Dados convertidos para visualização ===")
print(media_pandas)


media_pandas_formatado = media_pandas.copy()
media_pandas_formatado["Media_Desemprego"] = media_pandas_formatado["Media_Desemprego"].apply(lambda x: f"{x:,.0f}".replace(",", "."))
print("\n=== [Pandas] Dados formatados (valores em milhar) ===")
print(media_pandas_formatado)

plt.figure(figsize=(8, 5))
plt.bar(media_pandas["Ano"], media_pandas["Media_Desemprego"], color="#EB821C")
plt.xlabel("Ano")
plt.ylabel("Taxa média de desemprego")
plt.title("Evolução da taxa média de desemprego em Niterói")
plt.xticks(media_pandas["Ano"])

plt.gca().get_yaxis().set_major_formatter(
    plt.FuncFormatter(lambda x, _: f"{x:,.0f}".replace(",", "."))
)

plt.tight_layout()
plt.show()

spark.stop()

