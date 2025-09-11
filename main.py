from pyspark.sql import SparkSession

# Criar sessão Spark
spark = SparkSession.builder \
    .appName("NiteroiBigData") \
    .getOrCreate()

# Caminho do CSV
arquivo = "niteroi_2020_2025_todos_meses.csv"

# Ler CSV com cabeçalho
df = spark.read.csv(arquivo, header=True, inferSchema=True)

# Mostrar schema e primeiras linhas
df.printSchema()
df.show(10, truncate=False)

# Exemplo: filtrar só 2025
print("=== Dados de 2025 ===")
df.filter(df["Ano"] == 2025).show()

# Exemplo: média por ano
print("=== Média por ano ===")
df.groupBy("Ano").avg("Valor").show()

# Encerrar sessão
spark.stop()
