# import pandas as pd

# arquivo = "niteroi.csv.ods"

# # Ler com header na primeira linha
# df = pd.read_excel(arquivo, engine="odf", header=0)

# # Limpeza: remover linhas/colunas vazias
# df = df.dropna(how="all")
# df = df.dropna(axis=1, how="all")

# # Remover colunas "Unnamed"
# df = df.loc[:, ~df.columns.str.contains("Unnamed")]

# # Transformar para formato longo
# df_long = df.melt(
#     id_vars=["UF", "Código do Município", "Município"],  # mantemos fixos
#     var_name="Periodo",   # nome da coluna que vai armazenar os meses
#     value_name="Valor"    # nome da coluna com os valores
# )

# print("Formato final:", df_long.shape)
# print(df_long.head(12))


from pyspark.sql import SparkSession

# 1. Criar sessão Spark
spark = SparkSession.builder \
    .appName("NiteroiBigData") \
    .getOrCreate()

# 2. Caminho do CSV
arquivo = "c:/projetoBigData/niteroi_2020_2025_todos_meses.csv"

# 3. Ler CSV com cabeçalho
df = spark.read.csv(arquivo, header=True, inferSchema=True)

# 4. Mostrar schema e primeiras linhas
df.printSchema()
df.show(10, truncate=False)

# 5. Exemplo: filtrar só 2025
df.filter(df["Ano"] == 2025).show()

# 6. Exemplo: média por ano
df.groupBy("Ano").avg("Valor").show()

# 7. Exemplo: ordenar por período
df.orderBy("Periodo_dt").show(20, truncate=False)

# 8. Encerrar sessão
spark.stop()


