import tkinter as tk
import tkinter.font as tkFont

# Criação da janela principal
root = tk.Tk()
root.withdraw()  # Esconde a janela principal

# Listando as famílias de fontes disponíveis
font_families = tkFont.families()
print(font_families)

# Se você quiser ver as fontes em uma janela, use:
root.deiconify()  # Mostra a janela principal novamente
root.mainloop()  # Mantém a janela aberta
