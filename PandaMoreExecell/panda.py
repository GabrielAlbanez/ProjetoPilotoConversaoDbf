import pandas as pd
import os
import simpledbf 




# Corrigir o caminho do arquivo
arquivo = "PandaMoreExecell/FilesInput/Faturamentos.csv"  # Verifique se o caminho está correto

# Ler o arquivo CSV
try:
    dt = pd.read_csv(arquivo, sep=',', encoding='ISO-8859-1')  # Especifica o delimitador correto

except FileNotFoundError:
    print(f"Arquivo '{arquivo}' não encontrado.")
    exit()

# Calcular a coluna 'Total'

dt["Total"] = dt['quantidade'] * dt['preço unitario']

# Agrupar por cliente e somar o total de faturamento

# dt.groupby('cliente'):

# Esta parte do código está agrupando o DataFrame dt pela coluna 'cliente'.
# O groupby() é uma função que permite agregar dados com base em uma ou mais colunas. Aqui, todos os registros com o mesmo nome de cliente serão agrupados juntos.

# ['Total']:

# Após o agrupamento, você seleciona a coluna 'Total' do DataFrame agrupado. Isso indica que você deseja realizar operações apenas nessa coluna.
# .sum():

# Essa função calcula a soma dos valores da coluna 'Total' para cada grupo de clientes.
# O resultado será uma nova série onde cada cliente tem associado o total de suas compras (ou faturamento).
# .reset_index():

# Após a operação de agrupamento e soma, o resultado mantém o índice dos grupos (neste caso, os nomes dos clientes) como índice do DataFrame resultante.
# Usar reset_index() transforma esse índice de volta em uma coluna normal do DataFrame, resultando em um DataFrame mais fácil de manipular e visualizar.



faturamento_cliente = dt.groupby('cliente')['Total'].sum().reset_index()  # Corrigido: 'groupby' e 'reset_index'


dbf = simpledbf(dt)



# Savar em formato de html
Caminho = "PandaMoreExecell/FilesOutPut/faturamento_por_cliente.html"
Caminho2 = "PandaMoreExecell/FilesOutPut/faturamento_por_cliente.csv"

# verifica se o caminho existe , caos nao existir o caminho sera craido sozinho
os.makedirs(os.path.dirname(Caminho), exist_ok=True)

# esta dentro da pasta de files, ou seja tudo que criar daq para baixo vai cair na pasta files

faturamento_cliente.to_html(Caminho,  index=False, border=1, classes='tabela-faturamento')
faturamento_cliente.to_csv(Caminho2,  index=False)

print("Tabela de faturamento por cliente gerada com sucesso!")
