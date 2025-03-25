import tkinter as tk
from tkinter import ttk
from notebook import Notebook
from update import update_application
import subprocess
import sys

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Automação de Avaliações")
        self.geometry('400x300')
        self.resizable(False, False)
        self.centralizar_tela(self)
        # Notebook
        self.atualizar_aplicativo()
        self.notebook = Notebook(self)
    def atualizar_aplicativo():
        subprocess.run([sys.executable, 'update.py'])
    def centralizar_tela(self, tela):
        tela.update_idletasks()

        # Calcula as coordenadas para centralização
        largura_janela = tela.winfo_width()
        altura_janela = tela.winfo_height()
        largura_tela = tela.winfo_screenwidth()
        altura_tela = tela.winfo_screenheight()

        x = (largura_tela // 2) - (largura_janela // 2)
        y = (altura_tela // 2) - (altura_janela // 2)

        # Aplica a nova posição sem alterar o tamanho
        return tela.geometry(f'+{x}+{y}')