import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import json
import subprocess
import os
import shutil

# Função para carregar a configuração a partir do arquivo JSON
def carregar_configuracao(caminho_config):
    with open(caminho_config, 'r', encoding='utf-8') as f:
        return json.load(f)

# Função para criar pastas e arquivos para cada convênio

def criar_estrutura_convênios(convenios, output_dir):
    for convenio in convenios:
        dir_convenio = os.path.join(os.getcwd(), f"Convenios/{convenio}")
        os.makedirs(dir_convenio, exist_ok=True)

        # Criar a pasta de saída dentro da pasta do convênio
        dir_output = os.path.join(dir_convenio, output_dir)
        os.makedirs(dir_output, exist_ok=True)

        # Criar um arquivo de texto com o nome do convênio
        
        
        arquivo_py = os.path.join(dir_convenio, f"{convenio}.py")
        if not os.path.exists(arquivo_py):
               with open(arquivo_py, 'w', encoding='utf-8') as f:
                pass  # Apenas cria o arquivo vazio
        

        # Criar um arquivo JSON para o convênio, se não existir
        arquivo_json = os.path.join(dir_convenio, "config.json")
        
        if not os.path.exists(arquivo_json):  # Verifica se o arquivo já existe
            dados_convenio = {
                "DiretorioArquivoXlsx": f"Convenios/{convenio}",
                "output_directory": "FilesOutPut",  # Adicione mais informações se necessário
                "output_file_name": "Tabela_Convertida.dbf",
                "skip_rows": 0,
                "columns": [],
            }
            with open(arquivo_json, 'w', encoding='utf-8') as f:
                json.dump(dados_convenio, f, ensure_ascii=False, indent=4)


# Função para remover um convênio
def remover_convenio(convenio, modal):
    if convenio in config["Convenios"]:
        config["Convenios"].remove(convenio)
        atualizar_json('config.json', config)

        dir_convenio = os.path.join(os.getcwd(), f"Convenios/{convenio}")
        if os.path.exists(dir_convenio):
            shutil.rmtree(dir_convenio)
            messagebox.showinfo("Sucesso", f"Convênio '{convenio}' removido com sucesso!")
            modal.destroy()
            atualizar_combobox()  # Atualiza o combobox após a remoção
        else:
            messagebox.showwarning("Aviso", f"Pasta '{convenio}' não encontrada.")
    else:
        messagebox.showwarning("Aviso", f"Convênio '{convenio}' não encontrado no JSON.")

# Função para atualizar o arquivo JSON
def atualizar_json(caminho_json, dados):
    with open(caminho_json, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# Função para executar o arquivo do convênio
def executar_arquivo(conv):
    try:
        caminho_arquivo = os.path.join(os.getcwd(), f"Convenios/{conv}/{conv.lower()}.py")
        subprocess.run(["python", caminho_arquivo], check=True)
    except FileNotFoundError:
        messagebox.showerror("Erro", f"Arquivo '{conv.lower()}.py' não encontrado.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao executar o arquivo: {e}")

# Função que associa as clínicas a suas funções
def criar_switch(clinicas):
    switch = {}
    for clinica in clinicas:
        switch[clinica] = lambda c=clinica: executar_arquivo(c)  # Cria uma função para cada convênio
    return switch

def caseListeningClinica(clinica):
    clinicas = config["Convenios"]
    switch = criar_switch(clinicas)
    
    if clinica in switch:
        switch[clinica]()  # Executa a função se ela existir
    else:
        messagebox.showerror("Erro", "Convênio não reconhecido.")

def mostrar_modal(clinica):
    modal = tk.Toplevel(root)
    modal.title("Seleção de Convênio")
    largura_modal = 400
    altura_modal = 300
    
    # Obtém as dimensões da tela
    largura_tela = modal.winfo_screenwidth()
    altura_tela = modal.winfo_screenheight()
    
    # Calcula as coordenadas x e y para centralizar o modal
    x = (largura_tela // 2) - (largura_modal // 2)
    y = (altura_tela // 2) - (altura_modal // 2)
    
    modal.geometry(f"{largura_modal}x{altura_modal}+{x}+{y}")
    modal.transient(root)
    modal.grab_set()

    label = tk.Label(modal, text=f"Você selecionou: {clinica}", font=("Arial", 14))
    label.pack(pady=20)

    upload_button = tk.Button(modal, text="Fazer Upload", command=lambda: fazer_upload(clinica), bg="#4CAF50", fg="white", font=("Arial", 12))
    upload_button.pack(pady=10, padx=10)

    remove_button = tk.Button(modal, text="Remover Convênio", command=lambda: remover_convenio(clinica, modal), bg="#f44336", fg="white", font=("Arial", 12))
    remove_button.pack(pady=10, padx=10)

    close_button = tk.Button(modal, text="Fechar", command=modal.destroy, bg="#2196F3", fg="white", font=("Arial", 12))
    close_button.pack(pady=10, padx=10)

def fazer_upload(clinica):
    caminho_arquivo = filedialog.askopenfilename(title="Selecione um arquivo para upload")
    
    if not caminho_arquivo:
        messagebox.showwarning("Upload Cancelado", "Nenhum arquivo selecionado.")
        return

    caminho_destino = os.path.join(os.getcwd(), f"Convenios/{clinica}/{os.path.basename(caminho_arquivo)}")

    try:
        with open(caminho_arquivo, 'rb') as src_file:
            with open(caminho_destino, 'wb') as dst_file:
                dst_file.write(src_file.read())

        messagebox.showinfo("Sucesso", f"Arquivo enviado para {clinica} com sucesso!")
        
        # Executar o arquivo do convênio após o upload
        executar_arquivo(clinica)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao enviar o arquivo: {e}")

def atualizar_combobox():
    # Atualiza o Combobox com a nova lista de convênios
    combobox['values'] = config["Convenios"]
    combobox.set("Escolha um convênio")  # Reseta o valor do Combobox

def mostrar_selecao():
    selecao = combobox.get()
    mostrar_modal(selecao)  # Apenas mostra o modal, sem chamar a função de execução

# Carregar a configuração
config = carregar_configuracao('config.json')

# Criar pastas e arquivos para os convênios
criar_estrutura_convênios(config["Convenios"], config["output_directory"])

icon_path = os.path.abspath("images/favicon.ico")

root = tk.Tk()
largura_root = 600
altura_root = 400
root.title("Lista de convênios")
largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()
x = (largura_tela // 2) - (largura_root // 2)
y = (altura_tela // 2) - (altura_root // 2)
root.geometry(f"{largura_root}x{altura_root}+{x}+{y}")
root.configure(bg="#f0f0f0")  # Cor de fundo da janela principal
root.iconbitmap(icon_path)

# Estilo para o Combobox
combobox = ttk.Combobox(root, values=config["Convenios"], font=("Arial", 12))
combobox.set("Escolha um convênio")
combobox.pack(pady=10, padx=20)

# Botão para selecionar
botao = tk.Button(root, text="Selecionar", command=mostrar_selecao, bg="#4CAF50", fg="white", font=("Arial", 12))
botao.pack(pady=20, padx=20)

root.mainloop()