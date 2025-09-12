from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("NiteroiBigData") \
    .getOrCreate()

arquivo = "niteroi_2020_2025_todos_meses.csv"
df = spark.read.csv(arquivo, header=True, inferSchema=True)

df.printSchema()
df.show(10, truncate=False)

print("=== Dados de 2025 ===")
df.filter(df["Ano"] == 2025).show()

print("=== Média por ano ===")
df.groupBy("Ano").avg("Valor").show()
spark.stop()
