import tkinter as tk
from tkinter import ttk
from config import abrir_abas
from root import centralizar_tela

# Interface gráfica
root = tk.Tk()
root.title("Automação de Avaliações")
root.geometry('400x300')
root.resizable(False, False)
centralizar_tela(root)

# Notebook
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

abrir_abas(notebook)

# Rodar a interface
root.mainloop()