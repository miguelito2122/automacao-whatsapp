"""
Este módulo contém a classe Root, que representa a janela principal do aplicativo.
"""

import tkinter as tk
import subprocess
import os
import sys
from notebook import Notebook


class Root(tk.Tk):
    def __init__(self):
        """
        Initialize the main application window.

        This constructor sets up the main window of the application by configuring its
        title, size, and layout properties. It also initializes the application's
        update process and notebook component.

        Attributes:
            notebook (Notebook): The main notebook interface for the application.
        """

        super().__init__()
        self.title("Automação de Avaliações")
        self.geometry('400x300')
        self.resizable(False, False)
        self.centralizar_tela(self)
        # Notebook
        self.atualizar_aplicativo()
        self.notebook = Notebook(self)
    def atualizar_aplicativo(self):
        """
        Atualiza o aplicativo verificando se h  uma vers o mais recente no reposit rio.

        Se o arquivo update.py existir, ele   executado com o interpretador Python para
        verificar se h  uma vers o mais recente do aplicativo no reposit rio. Se uma vers o
        mais recente for encontrada, o aplicativo   atualizado automaticamente.

        :return: None
        """
        update_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'update.py')
        if os.path.exists(update_script):
            subprocess.run([sys.executable, update_script], check=True)
        else:
            print(f"Erro: O arquivo {update_script} não foi encontrado.")
    def centralizar_tela(self, tela):
        """
        Centraliza a janela na tela do monitor.

        Este método ajusta a posição de uma janela Tkinter para que ela seja centralizada
        na tela do monitor, sem alterar o tamanho da janela. Calcula as coordenadas
        necessárias considerando a largura e altura da janela e da tela.

        :param tela: O objeto da janela Tkinter que será centralizado.
        :return: A string contendo a nova geometria da janela no formato '+x+y'.
        """

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