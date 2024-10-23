import pandas as pd
import os
import dbf
import json
import difflib

# Função para carregar configurações do arquivo JSON
def carregar_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Função para converter valores de string para float
def converter_valor(valor):
    if pd.isna(valor):
        return 0.0
    valor = str(valor).replace('R$ ', '').replace('.', '').replace(',', '.')
    return float(valor)

# Função para gerar mapeamento automático
def gerar_mapeamento(colunas_df, colunas_dbf, cutoff=0.9):
    mapping = {}
    for col_dbf in colunas_dbf:
        # Encontrar a melhor correspondência usando difflib com o cutoff especificado
        melhor_correspondencia = difflib.get_close_matches(col_dbf, colunas_df, n=1, cutoff=cutoff)
        if melhor_correspondencia:
            mapping[col_dbf] = melhor_correspondencia[0]
    return mapping

# Função principal para processar o Excel e converter para DBF
def processar_excel_para_dbf(arquivo):
    config = carregar_config()
   
    try:
        # Lê o Excel ignorando linhas em branco e a partir da linha definida no config
        dt = pd.read_excel(arquivo, skiprows=config['skip_rows'])

        # Limpa os nomes das colunas
        dt.columns = dt.columns.str.strip().str.replace('\n', ' ').str.replace('  ', ' ')

        # Filtra linhas e colunas de interesse
        dt = dt[dt['CÓDIGO'].notna()]
        colunas_desejadas = config['columns']
        dt = dt[colunas_desejadas]
        dt_filtrado = dt.dropna()

        # Define o caminho de saída para o arquivo DBF
        caminho_saida = os.path.join("Convenios", "Santander", config['output_directory'], config['output_file_name'])
        os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)

        # Definição das colunas da tabela DBF
        colunas_dbf = [
            'CODTBPPROP', 'CODTBPPADR', 'CODSPPROP', 'CODSPPADR',
            'DESCRSP', 'VALORHOSP', 'VALORPROF', 'VALORANE',
            'VALORSADT', 'CODMOEDVAL', 'CODMOEDASH', 'CODMOEDANE',
            'CODMOEDASD', 'PTOPORANE', 'NUMAUX', 'FILMEM2'
        ]

        # Gera o mapeamento automático com cutoff
        mapping = gerar_mapeamento(dt.columns.tolist(), colunas_dbf, cutoff=0.3)

        # Cria a tabela DBF com as colunas especificadas
        with dbf.Table(
            caminho_saida,
            'CODTBPPROP C(2); CODTBPPADR C(2); CODSPPROP C(10); CODSPPADR C(10); '
            'DESCRSP C(65); VALORHOSP N(15,4); VALORPROF N(15,4); VALORANE N(15,4); '
            'VALORSADT N(15,4); CODMOEDVAL C(2); CODMOEDASH C(2); CODMOEDANE C(2); '
            'CODMOEDASD C(2); PTOPORANE N(5,0); NUMAUX N(1,0); FILMEM2 N(7,4)'
        ) as table:
            # Mapeia os valores a serem adicionados
            for index, row in dt_filtrado.iterrows():
                try:
                    linha_dbf = {
                        'CODTBPPROP': '',  # CODTBPPROP (valor vazio)
                        'CODTBPPADR': '31',  # CODTBPPADR (valor 31)
                        'CODSPPROP': str(row[mapping.get('CODSPPROP', '')]),  # CODSPPROP
                        'CODSPPADR': str(row[mapping.get('CODSPPROP', '')]),  # CODSPPADR
                        'DESCRSP': str(row.get(mapping.get('DESCRSP', ''), ''))[:65],  # DESCRSP
                        'VALORHOSP': 0.0,  # VALORHOSP
                        'VALORPROF': converter_valor(row.get(mapping.get('VALORPROF', ''), 0.0)),  # VALORPROF
                        'VALORANE': 0.0,  # VALORANE
                        'VALORSADT': 0.0,  # VALORSADT
                        'CODMOEDVAL': 'MM',  # CODMOEDVAL
                        'CODMOEDASH': 'MM',  # CODMOEDASH
                        'CODMOEDANE': 'MM',  # CODMOEDANE
                        'CODMOEDASD': 'MM',  # CODMOEDASD
                        'PTOPORANE': 0,  # PTOPORANE
                        'NUMAUX': 0,  # NUMAUX
                        'FILMEM2': float(str(row.get(mapping.get('FILMEM2', ''), 0)).replace(',', '.')) if pd.notna(row.get(mapping.get('FILMEM2', ''))) else 0.0  # FILMEM2 convertido para float
                    }

                    # Adiciona a linha no DBF
                    table.append(tuple(linha_dbf.values()))
                except Exception as e:
                    print(f"Erro ao adicionar linha {index}: {e}")

        print(f"Arquivo DBF '{caminho_saida}' gerado com sucesso!")

    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo}' não encontrado.")
    except ValueError as e:
        print(f"Erro ao ler o arquivo: {e}")
    except KeyError as e:
        print(f"Erro ao acessar as colunas: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    print(gerar_mapeamento(dt.columns.tolist(), colunas_dbf, cutoff=0.3))
    print("Colunas do DataFrame:", dt.columns.tolist())
    

def takeArchive():
    config = carregar_config()  # Carrega as configurações do JSON
    caminho_diretorio = config.get("DiretorioArquivoXlsx")  # Obtém o nome do diretório

    if not os.path.isdir(caminho_diretorio):
        print(f"Erro: O diretório '{caminho_diretorio}' não existe.")
        return []

    arquivos_encontrados = []  # Lista para armazenar os caminhos dos arquivos
    for arquivo in os.listdir(caminho_diretorio):
        caminho_arquivo = os.path.join(caminho_diretorio, arquivo)
        
        if os.path.isfile(caminho_arquivo) and arquivo.lower().endswith('.xlsx'):
            arquivos_encontrados.append(caminho_arquivo)  # Adiciona o caminho do arquivo à lista

    return arquivos_encontrados  # Retorna a lista de arquivos encontrados

def excluir_arquivo(caminho):
     try:
        os.remove(caminho)  # Tenta remover o arquivo
        print(f"Arquivo '{caminho}' excluído com sucesso!")
     except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho}' não foi encontrado.")
     except PermissionError:
        print(f"Erro: Permissão negada para excluir o arquivo '{caminho}'.")
     except Exception as e:
        print(f"Erro inesperado: {e}")

arquivos_xlsx = takeArchive()
# Processa cada arquivo .xlsx encontrado
for arquivo in arquivos_xlsx:
    processar_excel_para_dbf(arquivo)
    excluir_arquivo(arquivo)
