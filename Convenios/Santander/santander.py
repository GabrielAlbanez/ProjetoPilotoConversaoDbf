import os
import json
import pandas as pd

def converter_excel_para_dbf(arquivo_excel, caminho_saida, nome_saida):
    # Lê o arquivo Excel
    try:
        df = pd.read_excel(arquivo_excel)
        # Converte para DBF e salva no diretório de saída
        df.to_dbf(os.path.join(caminho_saida, nome_saida))
        print(f"Arquivo '{nome_saida}' criado com sucesso em '{caminho_saida}'!")
    except Exception as e:
        print(f"Ocorreu um erro ao converter o arquivo: {e}")

def main():
    # Carregar configuração
    caminho_json = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(caminho_json, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Caminhos e arquivos
    diretorio_arquivo_xlsx = config["DiretorioArquivoXlsx"]
    output_directory = config["output_directory"]
    output_file_name = config["output_file_name"]

    # Encontrar o arquivo .xlsx mais recente no diretório
    arquivos = [f for f in os.listdir(diretorio_arquivo_xlsx) if f.endswith('.xlsx')]
    if arquivos:
        arquivo_excel = os.path.join(diretorio_arquivo_xlsx, sorted(arquivos, key=os.path.getctime)[-1])
        caminho_saida = os.path.join(os.getcwd(), output_directory)
        converter_excel_para_dbf(arquivo_excel, caminho_saida, output_file_name)
    else:
        print("Nenhum arquivo .xlsx encontrado.")

if __name__ == '__main__':
    main()
