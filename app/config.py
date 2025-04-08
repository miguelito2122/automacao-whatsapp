"""
Módulo que contém as configurações do programa.
"""

import os
import sys
from threading import Thread
import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext


import requests

class ToolTip:
    """
    Classe que representa um tooltip para exibição de informações adicionais em widgets.

    Args:
        widget: O widget ao qual o tooltip ser  anexado.
        text: O texto a ser exibido no tooltip.
    """

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

class SplashScreen:
    """
    Classe responsável por criar e gerenciar a tela de splash (carregamento)
    do aplicativo, exibindo um console e uma barra de progresso.
    """
    def __init__(self, master: tk.Tk):
        # Cria a janela de splash
        self.window = tk.Toplevel(master)
        self.window.title("Iniciando o aplicativo")
        self.window.geometry("250x150")
        self.window.resizable(False, False)
        self.window.attributes('-topmost', True)
        self.window.overrideredirect(True)

        # Centraliza a janela de splash
        center_window(self.window)

        # Cria o console (scrolledtext)
        self.console = scrolledtext.ScrolledText(
            self.window, wrap=tk.WORD, font=("Courier", 8)
        )
        self.console.place(x=0, y=0, width=250, height=110)

        # Cria a barra de progresso
        self.progress = ttk.Progressbar(
            self.window, orient="horizontal", mode="indeterminate", length=230
        )
        self.progress.place(x=10, y=120)

    def start(self):
        """Inicia a barra de progresso."""
        self.progress.start(10)

    def stop(self):
        """Interrompe a barra de progresso."""
        self.progress.stop()

    def destroy(self):
        """Destroi a janela de splash."""
        self.window.destroy()

def launch_error(msg, erro):
    """
    Exibe uma mensagem de erro em uma janela modal.
    
    Exibe uma janela de erro com o título "Erro", o texto da mensagem e o erro.
    Args:
        msg (str): Mensagem a ser exibida ao usuário.
        erro (Exception): Mensagem de erro retornado.
    Returns:
        str: Retorna a mensagem de erro, formatada. 
    """
    messagebox.showerror('Erro', f'{msg}\nTipo de erro: {erro}')
    sys.exit(1)

def timed_input(prompt, timeout, default='n'):
    """
    Obtém a entrada do usuário com um limite de tempo.

    Exibe um prompt para o usuário e aguarda a entrada por um tempo
    especificado. Se o usuário não fornecer uma entrada dentro do tempo
    limite, a função retorna None. Caso contrário, retorna a entrada 
    convertida para minúsculas e sem espaços extras.

    Args:
        prompt (str): Mensagem a ser exibida ao usuário.
        timeout (float): Tempo máximo em segundos para aguardar a entrada.

    Returns:
        str or None: A entrada do usuário em minúsculas ou None se o tempo
        limite for atingido.
    """

    result = []
    def get_input():
        try:
            inp = input(prompt)
            result.append(inp.strip().lower())
        except AttributeError as e:
            result.append(default)

    input_thread = Thread(target=get_input)
    input_thread.daemon = True
    input_thread.start()
    input_thread.join(timeout)

    if input_thread.is_alive():
        return None  # Timeout ocorreu
    else:
        return result[0] if result else None

def center_window(window: tk.Tk):
    """
    Centraliza a janela na tela.

    Args:
        window (tk.Tk): A janela que deve ser centralizada.

    Returns:
        tuple: Uma tupla contendo a largura e a altura da janela.
    """
    window.update_idletasks()
    largura_janela = window.winfo_width()
    altura_janela = window.winfo_height()
    largura_tela = window.winfo_screenwidth()
    altura_tela = window.winfo_screenheight()
    x = (largura_tela // 2) - (largura_janela // 2)
    y = (altura_tela // 2) - (altura_janela // 2)
    window.geometry(f'+{x}+{y}')

    return largura_janela, altura_janela

def ensure_directory(directory: str, console=None):
    """
    Garante que o diretório exista.
    Retorna uma Mensagem para o console escolhido.
    Se o diretório não existir, ele será criado.
    Se ocorrer um erro ao criar o diretório, uma mensagem de erro será exibida.

    Args:
        directory (str): O caminho do diretório a ser verificado/criado.
        console (tk.Text, optional): O widget de console onde a mensagem será exibida.
        Se None, a mensagem será impressa no console padrão.

    Returns:
        None
    
    """
    try:
        os.makedirs(directory, exist_ok=True)
        log(console, f"Diretório '{directory}' verificado/criado.")
    except Exception as e:
        log(console, f"Erro ao criar diretório '{directory}': {e}")

def log(console, mensagem: str):
    """Insere uma mensagem no widget de log de forma segura."""
    def inserir():
        console.insert(tk.END, mensagem + "\n")
        console.see(tk.END)

    if console is not None:
        console.after(0, inserir)  # Executa na thread principal
    else:
        print(mensagem)

def read_file_bytes(file_path: str, console=None) -> bytes:
    """Lê um arquivo em modo binário e retorna seu conteúdo."""
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        log(console, f"Arquivo lido: {file_path}")
        return data
    except Exception as e:
        log(console, f"Erro ao ler arquivo '{file_path}': {e}")
        return None

def write_file_bytes(file_path: str, data: bytes, console=None):
    """Escreve dados binários em um arquivo."""
    try:
        with open(file_path, 'wb') as f:
            f.write(data)
        log(console, f"Arquivo escrito: {file_path}")
    except Exception as e:
        log(console, f"Erro ao escrever arquivo '{file_path}': {e}")
        return None

def buscar_arquivo(api_chave, nome_arquivo, console=None, custom_headers=None):
    """
    Busca um arquivo no repositório do GitHub com possibilidade de personalizar headers
    
    Parâmetros:
        api_chave (str): Token de autenticação do GitHub
        nome_arquivo (str): Nome do arquivo a ser buscado
        console (objeto, opcional): Objeto para logging
        custom_headers (dict, opcional): Headers adicionais ou substitutos
    """
    REPO_OWNER = 'miguelito2122'
    REPO_NAME = 'automacao-whatsapp'
    BRANCH = 'main'

    # Headers base com valores padrão
    base_headers = {
        "Authorization": f"token {api_chave}",
        "Accept": "application/vnd.github.v3.raw"
    }

    # Combina headers base com customizados (se fornecido)
    headers = {**base_headers, **(custom_headers or {})}

    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{nome_arquivo}?ref={BRANCH}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        if response.status_code == 200:
            return response.content.decode('utf-8').strip()

    except requests.exceptions.HTTPError as e:
        error_msg = f"Erro ao buscar {nome_arquivo}: {e.response.status_code}"
        if console:
            log(console, error_msg)
        launch_error(error_msg, e)
    except Exception as e:
        if console:
            log(console, f"Erro na requisição: {str(e)}")
        launch_error(f"Erro ao buscar {nome_arquivo}", e)

    launch_error(f"Arquivo {nome_arquivo} não encontrado", "RaisedError")

    return None

def atualizar_updater(base_path):
    """
    Atualiza o updater.exe do base_path.

    Se o arquivo update.py ou update.exe existir, ele é sobrescrito com o
    último release do update.exe da versão atual do repositório.

    :param base_path: O diretório base do aplicativo.

    :return: None
    """
    pass




class ChaveAPIEntry(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Inserir Chave API")
        self.geometry("300x100")
        self.resizable(False, False)
        centralizar_tela(self)

        self.result = None

        # Frame principal
        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Entry para inserir a chave
        self.entry = tk.Entry(frame, width=40)
        self.entry.pack(pady=(0, 10))

        # Frame para os botões
        btn_frame = tk.Frame(frame)
        btn_frame.pack()

        # Botão OK
        ok_btn = tk.Button(btn_frame, text="OK", command=self.on_ok)
        ok_btn.pack(side=tk.LEFT, padx=(0, 5))

        # Botão Cancelar
        cancel_btn = tk.Button(btn_frame, text="Cancelar", command=self.on_cancel)
        cancel_btn.pack(side=tk.LEFT)

        # Focar no Entry e esperar a janela ser fechada
        self.entry.focus_set()
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.wait_window(self)

    def on_ok(self):
        self.result = self.entry.get()
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()