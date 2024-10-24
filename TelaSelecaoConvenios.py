import tkinter as tk
from tkinter import messagebox, filedialog
import os
import shutil

class ModalSelecao:
    def __init__(self, root, clinica, callback_remover, callback_upload):
        self.modal = tk.Toplevel(root)
        self.modal.title("Seleção de Convênio")
        largura_modal, altura_modal = 400, 300

        # Centraliza a janela
        largura_tela = self.modal.winfo_screenwidth()
        altura_tela = self.modal.winfo_screenheight()
        x = (largura_tela // 2) - (largura_modal // 2)
        y = (altura_tela // 2) - (altura_modal // 2)

        self.modal.geometry(f"{largura_modal}x{altura_modal}+{x}+{y}")
        self.modal.transient(root)
        self.modal.grab_set()

        # Label com a clínica selecionada
        label = tk.Label(self.modal, text=f"Você selecionou: {clinica}", font=("Arial", 14))
        label.pack(pady=20)

        # Botão de Upload
        upload_button = tk.Button(self.modal, text="Fazer Upload", bg="#4CAF50", fg="white",
                                  font=("Arial", 12), command=lambda: callback_upload(clinica))
        upload_button.pack(pady=10, padx=10)

        # Botão para remover convênio
        remove_button = tk.Button(self.modal, text="Remover Convênio", bg="#f44336", fg="white",
                                  font=("Arial", 12), command=lambda: callback_remover(clinica, self.modal))
        remove_button.pack(pady=10, padx=10)

        # Botão para fechar a janela
        close_button = tk.Button(self.modal, text="Fechar", bg="#2196F3", fg="white",
                                 font=("Arial", 12), command=self.modal.destroy)
        close_button.pack(pady=10, padx=10)
