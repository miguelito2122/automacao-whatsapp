"""
Este módulo contém a classe Root, que representa a janela principal do aplicativo.
"""
from tkinter import messagebox
import os
import sys
import subprocess
import tkinter as tk
try:
    import requests
    from config import launch_error
    from notebook import Notebook
except ImportError as e:
    messagebox.showerror('Erro', f'Erro ao importar módulos(root.py)\nErro: {e}')
    sys.exit(1)

class Root(tk.Tk):
    def __init__(self, base_path=None):
        """
        Inicializa a janela principal do aplicativo.

        Este construtor configura a janela principal do aplicativo, definindo seu
        título, tamanho e propriedades de layout. Ele também inicializa o processo
        de atualização do aplicativo e o componente notebook.

        Atributos:
            notebook (Notebook): A interface notebook principal do aplicativo.
        """

        super().__init__()
        self.title("Automação de Avaliações")
        self.geometry('400x300')
        self.resizable(False, False)
        self.centralizar_tela(self)
        try:
            self.checar_atualizacao(base_path)
            self.base_path = base_path
        except AttributeError as e:
            launch_error('Erro ao obter o caminho base (root.py)', e)
        try:
            self.notebook = Notebook(self, self.base_path)
        except Exception as e:
            launch_error('Erro ao abrir Notebook (root.py)', e)
    def checar_atualizacao(self, base_path):
        """
        Atualiza o aplicativo verificando se há uma versão mais recente no repositório.

        Se o arquivo update.py existir, ele é executado com o interpretador Python para
        verificar se há uma versão mais recente do aplicativo no repositório. Se uma versão
        mais recente for encontrada, o aplicativo é atualizado automaticamente.

        :return: None
        """
        print(base_path)
        try:
            if getattr(sys, 'frozen', False):
                update_script = os.path.join(base_path, 'update/', 'update.py')
                version_txt = os.path.join(base_path, 'version.txt')
                print(version_txt)
            else:
                update_script = os.path.join(base_path, 'app', 'update.py')
                version_txt = os.path.join(base_path, 'version.txt')
                print(version_txt)
        except AttributeError as e:
            launch_error('Erro ao obter o caminho base (root.py)', e)

        # for root, dirs, files in os.walk(base_path):
        #     for file in files:
        #         print(os.path.join(root, file))


        if os.path.exists(update_script):
            try:
                repo_url = 'https://github.com/miguelito2122/automacao-whatsapp/archive/refs/heads/main.zip'
                response = requests.get(repo_url, timeout=10)
                if response.status_code == 200:
                    print('OK')
            except subprocess.CalledProcessError as e:
                launch_error('Erro ao atualizar o aplicativo', e)
        else:
            launch_error('Arquivo update.py nao encontrado', 'RaisedError')
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
