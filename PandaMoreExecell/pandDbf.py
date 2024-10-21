import pandas as pd
import os
import dbf

# Caminho do arquivo Excel
arquivo = "PandaMoreExecell/FilesInput/Tabela_do_Cliente.xlsx"

# Tente ler o arquivo Excel
try:
    # Lê o arquivo, ignorando as linhas em branco e apenas a partir da linha 7
    dt = pd.read_excel(arquivo, skiprows=6)

    # Exibir os nomes das colunas para verificação
    print("Nomes das colunas:", dt.columns.tolist())

    # Limpar os nomes das colunas
    dt.columns = dt.columns.str.strip().str.replace('\n', ' ').str.replace('  ', ' ')

    # Exibir os nomes das colunas após a limpeza
    print("Nomes das colunas após limpeza:", dt.columns.tolist())

    # Filtrar as linhas que não estão vazias na coluna 'CÓDIGO'
    dt = dt[dt['CÓDIGO'].notna()]

    # Filtrar apenas as colunas de interesse, incluindo 'P.A.'
    colunas_desejadas = ['CÓDIGO', 'DESCRIÇÃO DO PROCEDIMENTO', 'P.A.', 'QTDE. AUXILIAR', 'FILME', 'INCIDÊNCIA', 'VALOR PROCEDIMENTO']
    dt = dt[colunas_desejadas]
except FileNotFoundError:
    print(f"Arquivo '{arquivo}' não encontrado.")
    exit()
except ValueError as e:
    print(f"Erro ao ler o arquivo: {e}")
    exit()
except KeyError as e:
    print(f"Erro ao acessar as colunas: {e}")
    exit()

# Filtrar apenas as linhas onde todas as colunas estão preenchidas
dt_filtrado = dt.dropna()

# Função para converter valores em string para float
def converter_valor(valor):
    if pd.isna(valor):
        return 0.0
    # Remove o símbolo de moeda e substitui vírgula por ponto
    valor = str(valor).replace('R$ ', '').replace('.', '').replace(',', '.')
    return float(valor)

# Caminho para salvar o arquivo DBF
CaminhoArquivo = "PandaMoreExecell/FilesOutPut/Tabela_do_Cliente.dbf"

# Verifica se o caminho existe, caso não exista, o caminho será criado automaticamente
os.makedirs(os.path.dirname(CaminhoArquivo), exist_ok=True)

# Definir o formato dos campos com nomes encurtados, incluindo 'P.A.'
with dbf.Table(CaminhoArquivo, 'CODIGO C(10); DESC_PROC C(100); P_A N(10,2); QTDE_AUX N(10,2); FILME C(50); INCIDENCIA C(50); VALOR_PROC N(10,2)') as table:
    for index, row in dt_filtrado.iterrows():
        try:
            # Converter e verificar os valores, garantindo que sejam numéricos ou zero
            p_a = float(row['P.A.']) if pd.notna(row['P.A.']) and str(row['P.A.']).replace('.', '', 1).isdigit() else 0.0
            qtde_aux = float(row['QTDE. AUXILIAR']) if pd.notna(row['QTDE. AUXILIAR']) and str(row['QTDE. AUXILIAR']).replace('.', '', 1).isdigit() else 0.0
            valor_proc = converter_valor(row['VALOR PROCEDIMENTO'])
            
            table.append((
                str(row['CÓDIGO']),
                str(row['DESCRIÇÃO DO PROCEDIMENTO']),
                p_a,
                qtde_aux,
                str(row['FILME']),
                str(row['INCIDÊNCIA']),
                valor_proc
            ))
        except Exception as e:
            print(f"Erro ao adicionar linha {index}: {e}")

print("Arquivo DBF gerado com sucesso!")