import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import subprocess
import os
import shutil
from TelaSelecaoConvenios import ModalSelecao  

def carregar_configuracao(caminho_config):
    with open(caminho_config, 'r', encoding='utf-8') as f:
        return json.load(f)

def criar_estrutura_convênios(convenios, output_dir):
    for convenio in convenios:
        dir_convenio = os.path.join(os.getcwd(), f"Convenios/{convenio}")
        os.makedirs(dir_convenio, exist_ok=True)

        dir_output = os.path.join(dir_convenio, output_dir)
        os.makedirs(dir_output, exist_ok=True)

        arquivo_py = os.path.join(dir_convenio, f"{convenio}.py")
        if not os.path.exists(arquivo_py):
            with open(arquivo_py, 'w', encoding='utf-8') as f:
                pass

        arquivo_json = os.path.join(dir_convenio, "config.json")
        if not os.path.exists(arquivo_json):
            dados_convenio = {
                "DiretorioArquivoXlsx": f"Convenios/{convenio}",
                "output_directory": "FilesOutPut",
                "output_file_name": "Tabela Convertida.dbf",
                "skip_rows": 0,
                "columns": [],
            }
            with open(arquivo_json, 'w', encoding='utf-8') as f:
                json.dump(dados_convenio, f, ensure_ascii=False, indent=4)

def remover_convenio(convenio, modal):
    if convenio in config["Convenios"]:
        config["Convenios"].remove(convenio)
        atualizar_json('config.json', config)

        dir_convenio = os.path.join(os.getcwd(), f"Convenios/{convenio}")
        if os.path.exists(dir_convenio):
            shutil.rmtree(dir_convenio)
            messagebox.showinfo("Sucesso", f"Convênio '{convenio}' removido com sucesso!")
            modal.destroy()
            atualizar_combobox()
        else:
            messagebox.showwarning("Aviso", f"Pasta '{convenio}' não encontrada.")

def atualizar_json(caminho_json, dados):
    with open(caminho_json, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def executar_arquivo(conv):
    try:
        caminho_arquivo = os.path.join(os.getcwd(), f"Convenios/{conv}/{conv.lower()}.py")
        subprocess.run(["python", caminho_arquivo], check=True)
    except FileNotFoundError:
        messagebox.showerror("Erro", f"Arquivo '{conv.lower()}.py' não encontrado.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao executar o arquivo: {e}")

def fazer_upload(clinica):
    caminho_arquivo = filedialog.askopenfilename(title="Selecione um arquivo para upload")
    if not caminho_arquivo:
        messagebox.showwarning("Upload Cancelado", "Nenhum arquivo selecionado.")
        return

    caminho_destino = os.path.join(os.getcwd(), f"Convenios/{clinica}/{os.path.basename(caminho_arquivo)}")
    try:
        shutil.copy(caminho_arquivo, caminho_destino)
        messagebox.showinfo("Sucesso", f"Arquivo enviado para {clinica} com sucesso!")
        executar_arquivo(clinica)
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao enviar o arquivo: {e}")

def atualizar_combobox():
    combobox['values'] = config["Convenios"]
    combobox.set("Escolha um convênio")

def mostrar_selecao():
    selecao = combobox.get()
    if selecao:
        ModalSelecao(root, selecao, remover_convenio, fazer_upload)

config = carregar_configuracao('config.json')
criar_estrutura_convênios(config["Convenios"], config["output_directory"])

root = tk.Tk()
root.title("Lista de Convênios")
root.geometry("600x400")
root.configure(bg="#f0f0f0")

combobox = ttk.Combobox(root, values=config["Convenios"], font=("Arial", 12))
combobox.set("Escolha um convênio")
combobox.pack(pady=10)

botao = tk.Button(root, text="Selecionar", command=mostrar_selecao, bg="#4CAF50", fg="white", font=("Arial", 12))
botao.pack(pady=20)

root.mainloop()