Este projeto realiza a análise de dados de desemprego em Niterói entre os anos de 2020 e 2025, utilizando PySpark para processamento e cálculos e Pandas/Matplotlib para a etapa de visualização.
Tecnologias utilizadas
* PySpark – leitura do CSV, tratamento e cálculos estatísticos.
* Pandas – manipulação dos resultados do PySpark em memória.
* Matplotlib – geração de gráficos para análise visual.
Estrutura dos dados
O dataset utilizado foi:niteroi_2020_2025_todos_meses.csv
Colunas principais:
* Ano – ano da medição.
* Mes – mês da medição.
* Valor – taxa de desemprego registrada.
Funcionalidades do código
1. Leitura do CSV com PySpark, detectando o schema e exibindo as primeiras linhas.
2. Filtragem dos dados para o ano de 2025.
3. Cálculo da média anual da taxa de desemprego, com ordenação decrescente por ano.
4. Conversão dos resultados para Pandas.
5. Visualização gráfica da taxa média de desemprego em cada ano.
Saída esperada
* Exibição do schema do dataset.
* Primeiras linhas dos dados carregados.
* Dados filtrados de 2025.
* Tabela com a média de desemprego por ano (ordenada de forma decrescente).
* Gráfico de barras representando a evolução da taxa média de desemprego no período analisado.
