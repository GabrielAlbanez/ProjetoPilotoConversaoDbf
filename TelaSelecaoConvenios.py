import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import os.path

# Definições de cores e estilos
bg_color = '#2b2b2b'
fg_color = '#ffffff'
button_color = '#5A9'
hover_color = '#76c7c0'  # Cor mais chamativa no hover
progress_color = '#4CAF50'
font_family = "Poppins"
font_size = 17

def _style_code():
    style = ttk.Style()
    style.theme_use('clam')  # Tema moderno
    style.configure("TButton",
                    foreground=fg_color,
                    background=button_color,
                    font=(font_family, 12, 'bold'),
                    borderwidth=0,
                    padding=10,
                    relief="flat")
    
    style.map("TButton",
              foreground=[('active', fg_color)],
              background=[('active', hover_color)],
              relief=[('active', 'flat')])

    style.configure("TLabel", foreground=fg_color, background=bg_color, font=(font_family, font_size))

class Toplevel1:
    def __init__(self, top=None):
        top.geometry("600x500")
        top.title("Seleção de Convênio")
        top.configure(borderwidth="10", background=bg_color)

        self.top = top
        _style_code()

        # Botão Fechar
        self.btn_close = ttk.Button(self.top, text='Fechar', command=self.top.destroy)
        self.btn_close.place(relx=0.5, rely=0.85, anchor='center', height=40, width=120)

        # Botão Upload
        self.btn_upload = ttk.Button(self.top, text='Upload de arquivo')
        self.btn_upload.place(relx=0.3, rely=0.65, anchor='center', height=40, width=180)

        # Botão Remover Convênio
        self.btn_remove = ttk.Button(self.top, text='Remover convênio')
        self.btn_remove.place(relx=0.7, rely=0.65, anchor='center', height=40, width=180)

        # Título do Convênio sem aspas
        self.label_convenio = ttk.Label(self.top, text= 'Convênio Selecionado')
        self.label_convenio.place(relx=0.5, rely=0.3, anchor='center')

        # Barra de progresso personalizada
        self.barra_progresso = ttk.Progressbar(self.top, length=300, mode='determinate', style="green.Horizontal.TProgressbar")
        self.barra_progresso.place(relx=0.5, rely=0.75, anchor='center', height=25, width=400)

        # Customização da barra de progresso
        style = ttk.Style(self.top)
        style.configure("green.Horizontal.TProgressbar", troughcolor=bg_color, background=progress_color)

def main():
    global root
    root = tk.Tk()
    root.protocol('WM_DELETE_WINDOW', root.destroy)

    app = Toplevel1(root)  # Inicializa a interface gráfica
    root.mainloop()

if __name__ == '__main__':
    main()
