import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import subprocess
import os
import shutil
from TelaSelecaoConvenios import Toplevel1
 
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
    else:
        messagebox.showwarning("Aviso", f"Convênio '{convenio}' não encontrado no JSON.")
 
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
 
def mostrar_modal(clinica):
    modal = tk.Toplevel(root)
    app = Toplevel1(modal)
 
    app.label_convenio.config(text=f'"{clinica}" selecionado!')
    app.btn_upload.config(command=lambda: iniciar_upload(clinica, app.barra_progresso))
    app.btn_remove.config(command=lambda: remover_convenio(clinica, modal))
    app.btn_close.config(command=modal.destroy)
 
    largura_modal, altura_modal = 600, 472
    largura_tela = modal.winfo_screenwidth()
    altura_tela = modal.winfo_screenheight()
    x = (largura_tela // 2) - (largura_modal // 2)
    y = (altura_tela // 2) - (altura_modal // 2)
    modal.geometry(f"{largura_modal}x{altura_modal}+{x}+{y}")
 
    modal.transient(root)
    modal.grab_set()
 
def takeArchive():
    arquivos = filedialog.askopenfilenames(title="Selecione arquivos .xlsx", filetypes=[("Excel files", "*.xlsx")])
    return list(arquivos)
 
 
def iniciar_upload(clinica, progress_bar):
    arquivos_xlsx = takeArchive()
    if not arquivos_xlsx:
        messagebox.showwarning("Aviso", "Nenhum arquivo .xlsx encontrado.")
        return
 
    progress_var = tk.DoubleVar()
    progress_bar.config(variable=progress_var)
    iniciar_processo(arquivos_xlsx, progress_var, clinica)
 
def iniciar_processo(arquivos, progress_var, clinica):
    total_arquivos = len(arquivos)
 
    # Definir o diretório de destino para onde os arquivos devem ser movidos
    dir_destino = os.path.join("Convenios", clinica)
 
    for i, arquivo in enumerate(arquivos):
        try:
            # Mover o arquivo Excel para o diretório do convênio
            shutil.copy(arquivo, dir_destino)  # Copiar o arquivo para a pasta do convênio
           
            # Listar todos os arquivos .xlsx no diretório do convênio
            arquivos_xlsx = [f for f in os.listdir(dir_destino) if f.endswith('.xlsx')]
            if not arquivos_xlsx:
                messagebox.showwarning("Aviso", "Nenhum arquivo .xlsx encontrado no diretório do convênio.")
                return
 
            # O arquivo .xlsx mais recente
            arquivo_excel = os.path.join(dir_destino, sorted(arquivos_xlsx, key=lambda x: os.path.getctime(os.path.join(dir_destino, x)))[-1])
            print(f"Processando arquivo: {arquivo_excel}")
 
            # Definir o caminho do arquivo Python do convênio
            caminho_arquivo = os.path.join(dir_destino, f"{clinica.lower()}.py")
 
            # Verifique se o arquivo Python existe antes de tentar executá-lo
            if not os.path.exists(caminho_arquivo):
                messagebox.showerror("Erro", f"Arquivo '{clinica.lower()}.py' não encontrado.")
                return
 
            # Executar o arquivo Python passando o arquivo Excel como argumento
            subprocess.run(["python", caminho_arquivo, arquivo_excel], check=True)
           
            progress_var.set((i + 1) / total_arquivos * 100)  # Atualiza a barra de progresso
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao executar o arquivo: {e}")
            return  # Interrompa o processamento se ocorrer um erro
 
    messagebox.showinfo("Sucesso", "Processamento concluído!")
 
def atualizar_combobox():
    combobox['values'] = config["Convenios"]
    combobox.set("Escolha um convênio")
 
def mostrar_selecao():
    selecao = combobox.get()
    mostrar_modal(selecao)
 
config = carregar_configuracao('config.json')
criar_estrutura_convênios(config["Convenios"], config["output_directory"])
 
def main():
    global root
    root = tk.Tk()
    root.title("Lista de convênios")
 
    largura_root, altura_root = 600, 400
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    x = (largura_tela // 2) - (largura_root // 2)
    y = (altura_tela // 2) - (altura_root // 2)
    root.geometry(f"{largura_root}x{altura_root}+{x}+{y}")
    root.configure(bg="#f0f0f0")
 
    global combobox
    combobox = ttk.Combobox(root, values=config["Convenios"], font=("Arial", 12))
    combobox.set("Escolha um convênio")
    combobox.pack(pady=10, padx=20)
 
    botao = tk.Button(root, text="Selecionar", command=mostrar_selecao, bg="#4CAF50", fg="white", font=("Arial", 12))
    botao.pack(pady=20, padx=20)
 
    root.mainloop()
 
if __name__ == '__main__':
    main()