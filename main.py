from pyspark.sql import SparkSession

# Cria a sessão Spark
spark = SparkSession.builder \
    .appName("NiteroiBigData") \
    .getOrCreate()

# O caminho do csv
arquivo = "niteroi_2020_2025_todos_meses.csv"

# Ler CSV com cabeçalho  --- Tipo “importar a planilha para dentro do Spark”.
df = spark.read.csv(arquivo, header=True, inferSchema=True)

# Mostra schema e primeiras 10 linhas sem ortar os conteudos
df.printSchema()
df.show(10, truncate=False)

# filtrando só 2025
print("=== Dados de 2025 ===")
df.filter(df["Ano"] == 2025).show()

#  média por ano
print("=== Média por ano ===")
df.groupBy("Ano").avg("Valor").show()

# Encerrar sessão
spark.stop()
