import tkinter as tk
import tkinter.ttk as ttk
import os.path

# Definições de cores e estilos
_bgcolor = '#d9d9d9'
_fgcolor = '#000000'
_style_code_ran = 0

def _style_code():
    global _style_code_ran
    if _style_code_ran:
        return
    try:
        root.tk.call('source', os.path.join(os.path.dirname(__file__), 'themes', 'default.tcl'))
    except:
        pass
    style = ttk.Style()
    style.theme_use('default')
    style.configure('.', font="TkDefaultFont")
    _style_code_ran = 1

class Toplevel1:
    def __init__(self, top=None):
        top.geometry("600x472+337+104")
        top.title("Seleção de Convênio")
        top.configure(borderwidth="10", relief="ridge", background="#696969")

        self.top = top
        _style_code()

        # Botões da interface
        self.btn_close = ttk.Button(self.top, text='Fechar', command=self.top.destroy)
        self.btn_close.place(relx=0.417, rely=0.822, height=26, width=100)

        self.btn_upload = ttk.Button(self.top, text='Upload de arquivo')
        self.btn_upload.place(relx=0.167, rely=0.6, height=26, width=150)

        self.btn_remove = ttk.Button(self.top, text='Remover convênio')
        self.btn_remove.place(relx=0.583, rely=0.6, height=26, width=150)

        self.label_convenio = ttk.Label(self.top, text='Convênio selecionado!')
        self.label_convenio.place(relx=0.2, rely=0.233, height=49, width=360)

        # Barra de progresso
        self.barra_progresso = ttk.Progressbar(self.top, length=300, mode='determinate')
        self.barra_progresso.place(relx=0.083, rely=0.712, relwidth=0.833, height=19)

def main():
    global root
    root = tk.Tk()
    root.protocol('WM_DELETE_WINDOW', root.destroy)

    app = Toplevel1(root)  # Inicializa a interface gráfica
    root.mainloop()

if __name__ == '__main__':
    main()
