import os
import json
import pandas as pd
import dbf
import difflib


def converter_valor(valor):
    if pd.isna(valor):
        return 0.0
    valor = str(valor).replace('R$ ', '').replace('.', '').replace(',', '.')
    return float(valor)


def gerar_mapeamento(colunas_df, colunas_dbf, cutoff=0.9):
    mapping = {}
    for col_dbf in colunas_dbf:
        melhor_correspondencia = difflib.get_close_matches(col_dbf, colunas_df, n=1, cutoff=cutoff)
        if melhor_correspondencia:
            mapping[col_dbf] = melhor_correspondencia[0]
    return mapping



    



def converter_excel_para_dbf(arquivo, caminho_saida, nome_saida,config):
    try:
        dt = pd.read_excel(arquivo, skiprows=config['skip_rows'])
        dt.columns = dt.columns.str.strip().str.replace('\n', ' ').str.replace('  ', ' ')
        dt = dt[dt['CÓDIGO'].notna()]
        colunas_desejadas = config['columns']
        dt = dt[colunas_desejadas]
        dt_filtrado = dt.dropna()

        caminho_saida = os.path.join(config["DiretorioArquivoXlsx"], config['output_directory'], config['output_file_name'])
        os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)

        colunas_dbf = [
            'CODTBPPROP', 'CODTBPPADR', 'CODSPPROP', 'CODSPPADR',
            'DESCRSP', 'VALORHOSP', 'VALORPROF', 'VALORANE',
            'VALORSADT', 'CODMOEDVAL', 'CODMOEDASH', 'CODMOEDANE',
            'CODMOEDASD', 'PTOPORANE', 'NUMAUX', 'FILMEM2'
        ]

        mapping = gerar_mapeamento(dt.columns.tolist(), colunas_dbf, cutoff=0.3)

        with dbf.Table(
            caminho_saida,
            'CODTBPPROP C(2); CODTBPPADR C(2); CODSPPROP C(10); CODSPPADR C(10); '
            'DESCRSP C(65); VALORHOSP N(15,4); VALORPROF N(15,4); VALORANE N(15,4); '
            'VALORSADT N(15,4); CODMOEDVAL C(2); CODMOEDASH C(2); CODMOEDANE C(2); '
            'CODMOEDASD C(2); PTOPORANE N(5,0); NUMAUX N(1,0); FILMEM2 N(7,4)'
        ) as table:
            total_rows = len(dt_filtrado)
            for index, row in dt_filtrado.iterrows():
                try:
                    linha_dbf = {
                        'CODTBPPROP': '', 
                        'CODTBPPADR': '31',  
                        'CODSPPROP': str(row[mapping.get('CODSPPROP', '')]),  
                        'CODSPPADR': str(row[mapping.get('CODSPPROP', '')]),  
                        'DESCRSP': str(row.get(mapping.get('DESCRSP', ''), ''))[:65],  
                        'VALORHOSP': 0.0,  
                        'VALORPROF': converter_valor(row.get(mapping.get('VALORPROF', ''), 0.0)),  
                        'VALORANE': 0.0,  
                        'VALORSADT': 0.0,  
                        'CODMOEDVAL': 'MM',  
                        'CODMOEDASH': 'MM',  
                        'CODMOEDANE': 'MM',  
                        'CODMOEDASD': 'MM',  
                        'PTOPORANE': 0,  
                        'NUMAUX': 0,  
                        'FILMEM2': float(str(row.get(mapping.get('FILMEM2', ''), 0)).replace(',', '.')) if pd.notna(row.get('FILMEM2', '')) else 0.0  
                    }
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

            


def main():
    # Carregar configuração
    caminho_json = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(caminho_json, 'r', encoding='utf-8') as f:
        config = json.load(f)
        
    print(config)

    def takeArchive():
        caminho_arquivo = os.path.join(config["DiretorioArquivoXlsx"], config["input_file_name"])
        print("Caminho do arquivo:", caminho_arquivo)
        return caminho_arquivo

    caminho_saida = config["output_directory"]
    output_file_name = config["output_file_name"]
    arquivo_excel = takeArchive()
    
    print("Arquivo Excel:", arquivo_excel)
    
    converter_excel_para_dbf(arquivo_excel, caminho_saida, output_file_name,config)
    
    caminho_arquivo = os.path.join(config["DiretorioArquivoXlsx"], config["input_file_name"])
    os.remove(caminho_arquivo)
    print(f"Arquivo excluído com sucesso!")


if __name__ == '__main__':
    main()
