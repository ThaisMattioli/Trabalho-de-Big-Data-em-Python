from pyspark.sql import SparkSession
import pandas as pd
import matplotlib.pyplot as plt

spark = SparkSession.builder \
    .appName("NiteroiBigData") \
    .getOrCreate()

arquivo = "niteroi_2020_2025_todos_meses.csv"
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

plt.figure(figsize=(8, 5))
plt.bar(media_pandas["Ano"], media_pandas["Media_Desemprego"], color="salmon")
plt.xlabel("Ano")
plt.ylabel("Taxa média de desemprego")
plt.title("Evolução da taxa média de desemprego em Niterói")
plt.xticks(media_pandas["Ano"])
plt.tight_layout()
plt.show()

spark.stop()
