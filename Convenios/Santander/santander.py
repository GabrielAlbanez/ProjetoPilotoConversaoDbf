import pandas as pd
import os
import dbf
import json
import difflib
import tkinter as tk
from tkinter import ttk, messagebox

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
        melhor_correspondencia = difflib.get_close_matches(col_dbf, colunas_df, n=1, cutoff=cutoff)
        if melhor_correspondencia:
            mapping[col_dbf] = melhor_correspondencia[0]
    return mapping

# Função principal para processar o Excel e converter para DBF com barra de progresso
def processar_excel_para_dbf(arquivo, progress_var, progress_bar, root):
    config = carregar_config()

    try:
        dt = pd.read_excel(arquivo, skiprows=config['skip_rows'])
        dt.columns = dt.columns.str.strip().str.replace('\n', ' ').str.replace('  ', ' ')
        dt = dt[dt['CÓDIGO'].notna()]
        colunas_desejadas = config['columns']
        dt = dt[colunas_desejadas]
        dt_filtrado = dt.dropna()

        caminho_saida = os.path.join("Convenios", "Santander", config['output_directory'], config['output_file_name'])
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

                    # Atualiza a barra de progresso
                    progress_var.set(min((index + 1) / total_rows * 100, 100))
                    root.update_idletasks()

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

    # Verifica se a barra de progresso chegou a 100% e fecha a janela
    print(progress_var.get())
    if progress_var.get() == 100:
        messagebox.showinfo("Sucesso", "Upload realizado com sucesso!")
        root.after(1000, root.destroy)  # Fechar janela após 1 segundo

# Função para iniciar o processamento e exibir a barra de progresso
def iniciar_processo():
    arquivos_xlsx = takeArchive()
    if not arquivos_xlsx:
        print("Nenhum arquivo .xlsx encontrado.")
        return

    for arquivo in arquivos_xlsx:
        processar_excel_para_dbf(arquivo, progress_var, progress_bar, root)
        excluir_arquivo(arquivo)

# Função para excluir o arquivo após o processamento
def excluir_arquivo(caminho):
    try:
        os.remove(caminho)
        print(f"Arquivo '{caminho}' excluído com sucesso!")
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho}' não foi encontrado.")
    except PermissionError:
        print(f"Erro: Permissão negada para excluir o arquivo '{caminho}'.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

# Função para listar os arquivos .xlsx no diretório configurado
def takeArchive():
    config = carregar_config()
    caminho_diretorio = config.get("DiretorioArquivoXlsx")

    if not os.path.isdir(caminho_diretorio):
        print(f"Erro: O diretório '{caminho_diretorio}' não existe.")
        return []

    arquivos_encontrados = []
    for arquivo in os.listdir(caminho_diretorio):
        caminho_arquivo = os.path.join(caminho_diretorio, arquivo)
        
        if os.path.isfile(caminho_arquivo) and arquivo.lower().endswith('.xlsx'):
            arquivos_encontrados.append(caminho_arquivo)

    return arquivos_encontrados

# Configurações da janela e barra de progresso
root = tk.Tk()
root.title("Conversão de Excel para DBF")
root.geometry("400x150")


progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(pady=20)

start_button = tk.Button(root, text="Iniciar Conversão", command=iniciar_processo)
start_button.pack(pady=10)

root.mainloop()
