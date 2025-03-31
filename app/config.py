"""
Módulo que contém as configurações do programa.
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

import requests

class ToolTip:
    def __init__(self, widget, text):
        """
        Inicializa uma instância de ToolTip com um widget e um texto dados.

        Args:
            widget: O widget ao qual o tooltip ser  anexado.
            text: O texto a ser exibido no tooltip.

        Liga os eventos de mouse para mostrar e esconder o tooltip ao widget.
        """

        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.id = None

        widget.bind("<Enter>", self.on_enter)
        widget.bind("<Leave>", self.on_leave)
        widget.bind("<Motion>", self.on_motion)

    def on_enter(self, event=None):
        """
        Mostra o tooltip quando o mouse entra no widget.

        Args:
            event (tkinter.Event): O evento que desencadeou este método.
        """
        self.schedule(event)

    def on_motion(self, event):
        """
        Atualiza a posição do tooltip conforme o mouse se move sobre o widget.

        Args:
            event (tkinter.Event): O evento contendo a posição atual do mouse.
        """

        if self.tipwindow:
            x = event.x_root + 10
            y = event.y_root + 10
            self.tipwindow.wm_geometry(f"+{x}+{y}")

    def on_leave(self, event=None):
        """
        Esconde o tooltip quando o mouse sai do widget.

        Args:
            event (tkinter.Event): O evento que desencadeou este método (opcional).
        """
        self.unschedule()
        self.hide_tip()

    def schedule(self, event=None):
        """
        Agendar o tooltip para ser mostrado após um curto atraso.

        Args:
            event (tkinter.Event): O evento que desencadeou este método (opcional).

        Se o tooltip já estiver agendado para ser mostrado, este método irá
        cancelar o agendamento anterior e agendar um novo.
        """
        self.unschedule()
        self.id = self.widget.after(500, lambda: self.show_tip(event.x_root, event.y_root))

    def unschedule(self):
        """
        Cancela o agendamento de exibição do tooltip se ele estiver agendado para ser mostrado.

        Se o tooltip já estiver sendo exibido, este método cancela o agendamento.
        """
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def show_tip(self, x, y):
        """
        Mostra o tooltip nas coordenadas especificadas.

        Args:
            x (int): A coordenada x.
            y (int): A coordenada y.

        Se o tooltip já estiver sendo exibido, este m étodo não fará nada.
        """
        if self.tipwindow or not self.text:
            return
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # Remove a barra de título e bordas
        tw.wm_geometry(f"+{x + 10}+{y + 10}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self):
        """
        Esconde o tooltip se ele estiver atualmente visível.

        Destrói a janela do tooltip e define a variável de instância
        `tipwindow` como None.
        """
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def launch_error(msg, erro):
    """
    Exibe uma mensagem de erro em uma janela modal.
    
    Exibe uma janela de erro com o título "Erro", o texto da mensagem e o erro.
    """

    messagebox.showerror('Erro', f'{msg}\nTipo de erro: {erro}')
    sys.exit(1)

def printar_arquivos(base_path):
    """
    Imprime a lista de arquivos em um diretório e seus subdiretórios.

    Percorre o diretório especificado por `base_path` e seus subdiretórios,
    imprimindo o caminho absoluto de cada arquivo encontrado.

    Args:
        base_path (str): O diretório a ser percorrido.

    Returns:
        None
    """
    for root, dirs, files in os.walk(base_path):
        for file in files:
            print(os.path.join(root, file))

def checar_updater(base_path):
    """
    Atualiza o aplicativo verificando se há uma versão mais recente no repositório.

    Se o arquivo update.py existir, ele é executado com o interpretador Python para
    verificar se há uma versão mais recente do aplicativo no repositório. Se uma versão
    mais recente for encontrada, o aplicativo é atualizado automaticamente.

    :return: None
    """
    repo_url = 'https://raw.githubusercontent.com/miguelito2122/automacao-whatsapp/refs/heads/main/'
    versao_remota = repo_url + 'updaterversion.txt'
    try:
        if getattr(sys, 'frozen', False):
            update_exec = os.path.abspath(os.path.join(base_path, 'update'))
            version_txt = os.path.abspath(os.path.join(base_path, '_internal/','updaterversion.txt'))
            print('release\n', "Update:", update_exec, '\n', "updaterversion:",version_txt)
        else:
            update_exec = os.path.abspath(os.path.join(base_path, 'app', 'update.py'))
            version_txt = os.path.abspath(os.path.join(base_path, 'updaterversion.txt'))
            print('debug\n', "Update:", update_exec, '\n', "updaterversion:",version_txt)
    except AttributeError as e:
        launch_error('Erro ao obter os scripts e txt (root.py)', e)

    if os.path.exists(update_exec):
        print('update.py encontrado\n')
    else:
        launch_error('Arquivo update.exe nao encontrado', 'RaisedError')

    try:
        response = requests.get(versao_remota, timeout=10)
    except requests.exceptions.RequestException as e:
        launch_error('Erro ao obter versão remota (root.py)', e)

    if response.status_code != 200:
        launch_error('Erro ao obter versão remota (root.py)', 'HTTPError')

    versao_atual = open(version_txt, 'r', encoding='utf-8').readline().strip()
    if response.content.decode('utf-8') != versao_atual:
        return True
    else:
        messagebox.showinfo('Atualização',
                            'A versão mais recente do Updater ja foi instalada')
        return False


def atualizar_updater(base_path):
    """
    Atualiza o updater.exe do base_path.

    Se o arquivo update.py ou update.exe existir, ele é sobrescrito com o
    último release do update.exe da versão atual do repositório.

    :param base_path: O diretório base do aplicativo.

    :return: None
    """
    pass