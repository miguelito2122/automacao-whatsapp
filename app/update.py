#!/usr/bin/env python3
"""
Este script é responsável por atualizar o aplicativo para a última versão disponível
no repositório remoto, utilizando uma estrutura modular e organizada para facilitar a
manutenção e a reutilização das funções.
"""

import sys
import os
import shutil
import zipfile
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from pathlib import Path
import requests

# Importa funções de segurança (estas funções devem estar implementadas em módulos externos)
from security import gerar_chave, criptografar_credencial, descriptografar_credencial, obter_documento_crypto
from config import timed_input, ChaveAPIEntry, log, write_file_bytes, ensure_directory, read_file_bytes, center_window

# =====================================================
# FUNÇÕES DE DOWNLOAD, EXTRAÇÃO E LIMPEZA
# =====================================================

def download_latest_release(base_path: str, download_path: str, console=None) -> str:
    """
    Faz o download do último release do repositório remoto e salva em download_path.
    Retorna o caminho para o arquivo ZIP baixado.
    """
    log(console, "Buscando Chaves API e chaves criptografadas...")
    folder = 'keys' if getattr(sys, 'frozen', False) else 'docs'
    doc_dir = os.path.join(base_path, folder)
    chaves = {
        'ia': (".key", ".crypto"),
        'github': (".key", ".crypto"),
        }
    if os.path.exists(doc_dir):
        for key_type, extensions in chaves.items():
            print(key_type)
            print(extensions)
            found = False
            for extension in extensions:
                chave_path = os.path.join(doc_dir, f'{key_type}{extension}')
                if os.path.exists(chave_path):
                    log(console, f"Chave para '{key_type}' encontrada: {chave_path}")
                    found = True
                    break
            if not found:
                log(console, f"Nenhum documento encontrado para '{key_type}'.")
                log(console, "Não é possível atualizar sem as API_KEYS, solicitar ao desenvolvedor.")
                raise ValueError("Nenhum documento encontrado.")
    else:
        log(console, "Nenhum documento encontrado.")
        log(console, "Não é possível atualizar sem as API_KEYS, solicitar ao desenvolvedor.")
        raise ValueError("Nenhum documento encontrado.")

    crypto_doc_path = obter_documento_crypto(base_path, 'github', console)
    crypto_doc = read_file_bytes(crypto_doc_path, console)
    key_crypto = obter_chave(base_path, 'github', console)

    if not crypto_doc or not key_crypto:
        log(console, "Um dos dois documentos não foi encontrado.")
        raise ValueError("Um dos dois documentos não foi encontrado.")

    log(console, "Descriptografando Credenciais...")
    try:
        api_chave = descriptografar_credencial(crypto_doc, key_crypto)
    except Exception as e:
        log(console, f"Erro ao descriptografar credenciais: {e}")
        raise ValueError("Erro ao descriptografar credenciais") from e

    log(console, "Efetuando Download das Atualizações...")

    GITHUB_TOKEN = api_chave
    REPO_OWNER = 'miguelito2122'
    REPO_NAME = 'automacao-whatsapp'
    ASSET_NAME = 'latest_release'

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Obtém a última release do repositório via API do GitHub.
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        log(console,
            f"Erro ao buscar a última release: {response.status_code} - {response.text}")
        raise ValueError("Erro ao buscar a última release")
    log(console, "Ultima release encontrada com sucesso!")

    release_data = response.json()
    assets = release_data.get("assets", [])

    asset_id = None
    for asset in assets:
        if asset.get("name") == ASSET_NAME:
            asset_id = asset.get("id")
            break

    if not asset_id:
        log(console, f"Arquivo de atualização '{ASSET_NAME}' nao encontrado na ultima release.")
        raise ValueError("Arquivo de atualização não encontrado")
    log(console, f"Arquivo de atualização '{ASSET_NAME}' encontrado na ultima release.")

    # Busca o URL para o arquivo de atualização.
    download_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/assets/{asset_id}"
    headers["Accept"] = "application/octet-stream"
    response_download = requests.get(download_url, headers=headers, stream=True, timeout=10)

    if response_download.status_code != 200:
        log(console, f"Erro ao baixar o asset: {response_download.status_code} - {response_download.text}")
        raise ValueError("Erro ao baixar o asset")
    log(console, "Asset encontrado com sucesso!")

    doc_path = os.path.join(download_path, 'latest_release.zip')

    with open(doc_path, "wb") as f:
        f.write(response_download.content)
    log(console, f"Asset '{ASSET_NAME}' baixado com sucesso em: {doc_path}")

    return doc_path
def mock_download_latest_release(download_path: str, console=None) -> str:
    """
    Cria um arquivo ZIP de mock para testes.
    """
    log(console, "Mockando o download do último release...")
    zip_path = os.path.join(download_path, 'latest_release.zip')
    with zipfile.ZipFile(zip_path, 'w') as zip_ref:
        zip_ref.writestr('dummy_file.txt', 'conteúdo de teste')
        zip_ref.writestr('config.json', '{"key": "value"}')
        zip_ref.writestr('README.md', '# Arquivo de teste\nMock de atualização.')
    log(console, f"Mock concluído. Arquivo ZIP criado em: {zip_path}")
    return zip_path

def extract_zip_item(zip_path: str, extract_to: str, console=None):
    """
    Extrai arquivos do ZIP que estejam dentro do diretório especificado (item)
    e os salva em extract_to.
    """
    log(console, f"Extraindo arquivos para {extract_to}...")
    if not zipfile.is_zipfile(zip_path):
        raise ValueError("O arquivo baixado não é um ZIP válido.")

    download_path = os.path.abspath(extract_to)
    ensure_directory(download_path, console)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            zip_ref.extract(file, download_path)
    log(console, "Arquivos extraidos com sucesso.")

def clean_directory(directory: str, console=None, exclude_files: list = None):
    """
    Limpa o diretório, removendo arquivos e subdiretórios, exceto os especificados em exclude_files.
    """
    if exclude_files is None:
        exclude_files = []
    log(console, f"Limpando o diretório {directory}...")
    for item in os.listdir(directory):
        if item in exclude_files:
            continue
        item_path = os.path.join(directory, item)
        try:
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        except Exception as e:
            log(console, f"Erro ao remover {item_path}: {e}")
    log(console, "Limpeza concluída.")

# =====================================================
# FUNÇÃO PRINCIPAL DE ATUALIZAÇÃO
# =====================================================

def update_application(repo_path: str, console, debug_mode: bool = False):
    """
    Gerencia o processo de atualização do aplicativo.
    """

    folder = '../release' if getattr(sys, 'frozen', False) else 'release'
    download_path = os.path.join(repo_path, folder)
    ensure_directory(download_path, console)

    log(console, "Iniciando atualização...")

    # Limpa o diretório de release antes de iniciar a atualização
    clean_directory(download_path, console)


    # Escolhe o download real ou o mock, conforme o modo
    if debug_mode:
        log(console, "Modo DEBUG ativado. Usando download mock.")
        zip_path = mock_download_latest_release(download_path, console)
        log(console, "Mock de download concluído.")
        extract_zip_item(zip_path, download_path, console)
        log(console, f"{repo_path} Será Limpo..")
        clean_directory(repo_path, console)
        exe_dir = os.path.abspath(os.path.join(repo_path, '..'))
        log(console, f"Limpando Diretório {exe_dir}...")
        clean_directory(exe_dir, console, exclude_files=['Updater', 'Updater.exe', 'release'])

    else:
        try:
            log(console, "Fazendo Download do Aplicativo.")
            zip_path = download_latest_release(repo_path, download_path, console)
            log(console, "Download do aplicativo concluído. Extraindo...")
            extract_zip_item(zip_path, download_path, console)
            log(console, "Extração concluída.")
            log(console, "Limpando o diretório principal...")
            clean_directory(repo_path, console)
            log(console, "Lipando o diretório dos executáveis...")
            # Move os arquivos extraídos para o diretório principal
        except Exception as e:
            log(console, f"Erro ao baixar a última release: {e}")
            raise ValueError("Erro ao baixar a última release") from e

    log(console, "Atualização concluída com sucesso!")


# =====================================================
# UTILITÁRIOS DE INTERFACE (Tkinter)
# =====================================================


class AlterarChavesAPIWindow(tk.Toplevel):
    def __init__(self, parent, base_path: str):
        """
        Janela para alteração das chaves de API.
        """
        super().__init__(parent)
        self.base_path = base_path
        self.parent = parent

        self.title("API Keys Manager")
        self.geometry("300x200")
        self.resizable(False, False)
        centralizar_tela(self)

        # Console de log interno
        self.console = scrolledtext.ScrolledText(self, wrap=tk.WORD, font=("Courier", 10))
        self.console.place(x=0, y=50, width=300, height=150)
        log(self.console, "Selecione a chave a ser alterada...")

        # Frame de botões
        btn_frame = tk.Frame(self)
        btn_frame.place(relx=0, rely=0, width=300, height=50)

        btn_github = tk.Button(btn_frame, text="Github",
                               command=lambda: self.modificar_tela('github'))
        btn_github.place(rely=0.0, relx=0.05, relheight=1, relwidth=0.45)

        btn_ia = tk.Button(btn_frame, text="IA",
                           command=lambda: self.modificar_tela('ia'))
        btn_ia.place(relx=0.5, rely=0.0, relheight=1, relwidth=0.45)

    def modificar_tela(self, key_type: str):
        """
        Abre uma janela com opções para adicionar, alterar ou remover a chave do tipo especificado.
        """
        option_window = tk.Toplevel(self)
        self.option_window = option_window
        option_window.title("Alterar API Keys")
        option_window.geometry("250x75")
        option_window.resizable(False, False)
        centralizar_tela(option_window)

        btn_frame = tk.Frame(option_window)
        btn_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Apenas o botão "Adicionar" está implementado para exemplificar a funcionalidade
        add_button = tk.Button(btn_frame, text="Adicionar",
                               command=lambda: self.adicionar_encript(key_type))
        add_button.place(relx=0, rely=0, relwidth=0.33, relheight=1)
        self.add_button = add_button

        # Botões para "Alterar" e "Remover" podem ser implementados de forma similar
        update_button = tk.Button(btn_frame, text="Alterar",
                                  command=lambda: self.alterar_encrypt(key_type))
        update_button.place(relx=0.33, rely=0, relwidth=0.33, relheight=1)
        self.update_button = update_button

        remove_button = tk.Button(btn_frame, text="Remover",
                                  command=lambda: self.remover_encrypt(key_type))
        remove_button.place(relx=0.66, rely=0, relwidth=0.33, relheight=1)
        self.remove_button = remove_button

        try:
            chave_doc = obter_chave(self.base_path, key_type, self.console)
            if not chave_doc or chave_doc is None:
                if messagebox.askyesno("Chave Não Encontrada",
                                       f"Chave de criptografia para {key_type} não encontrada. Deseja procurar?"
                                       , parent=option_window):
                    self.chave_crypto = filedialog.askopenfilename(
                        initialdir=self.base_path,
                        title="Selecione o arquivo de Chave",
                        filetypes=[("Arquivos de Chave", "*.key")]
                    )
                    if not self.chave_crypto:
                        log(self.console, "Operação cancelada!")
                        option_window.destroy()
                        raise Exception("Operação cancelada pelo usuário")
                else:
                    if messagebox.askyesno("Chave Não Encontrada",
                                           f"Chave de criptografia para {key_type} não encontrada. Deseja gerar nova?"
                                           , parent=option_window):
                        self.chave_crypto = gerar_chave(self.base_path, self.console, key_type)
                    else:
                        log(self.console, "Operação cancelada!")
                        option_window.destroy()
                        raise Exception
            else:
                self.chave_crypto = chave_doc
        except Exception as e:
            log(self.console, f"Erro ao procurar chave: {e}")
            option_window.destroy()
            return

        try:
            crypto_doc = obter_documento_crypto(self.base_path, key_type, self.console)
            if crypto_doc is None:
                if messagebox.askyesno("Documento Não Encontrado",
                                       f"Documento de criptografia para {key_type} não encontrado. Deseja procurar?"
                                       , parent=option_window):
                    self.crypto_doc = filedialog.askopenfilename(
                        initialdir=self.base_path,
                        title="Selecione o arquivo de Documento",
                        filetypes=[("Arquivos de Documento", "*.crypto")]
                    )
                    if not self.crypto_doc:
                        log(self.console, "Operação cancelada!")
                        option_window.destroy()
                        raise Exception("Operação cancelada pelo usuário")
                else:
                    log(self.console, "Sem Documento Cryptografado em disposição.")
                    update_button.config(state=tk.DISABLED)
                    remove_button.config(state=tk.DISABLED)
                    self.crypto_doc = None
            else:
                self.crypto_doc = crypto_doc
        except Exception as e:
            log(self.console, f"Erro ao procurar documento: {e}")
            option_window.destroy()
            return

    def adicionar_encript(self, key_type: str):
        """
        Tenta adicionar uma nova chave API para o key_type.
        """

        # Cria o diretório, se necessário
        folder = 'keys' if getattr(sys, 'frozen', False) else 'docs'
        doc_dir = os.path.join(self.base_path, folder)
        ensure_directory(doc_dir, self.console)
        doc_path = os.path.join(doc_dir, f'{key_type}.crypto')

        try:
            api_key = self.requisitar_chave(self.option_window)
            log(self.console, "Encriptando chave...")
            criptografada = criptografar_credencial(api_key, self.chave_crypto)
            write_file_bytes(doc_path, criptografada, self.console)
        except Exception as e:
            log(self.console, f"Operação cancelada! Erro: {e}")
            self.option_window.destroy()
            return

        self.update_button.config(state=tk.NORMAL)
        self.remove_button.config(state=tk.NORMAL)
        self.crypto_doc = doc_path
        log(self.console, "Chave criptografada com sucesso!")

    def alterar_encrypt(self, key_type: str):
        if not messagebox.askokcancel("Alterar Chave",
                               f"Tem certeza de que deseja alterar a chave (.key) para {key_type}?"):
            return

        with open(self.crypto_doc, 'rb') as f:
            data = f.read()
        try:
            api_key = descriptografar_credencial(data, self.chave_crypto)
        except Exception as e:
            log(self.console, f"Erro ao descriptografar credencial: {e}")
            return

        change_window = tk.Toplevel(self.option_window)
        change_window.title("Chaves")
        change_window.geometry("200x100")
        centralizar_tela(change_window)
        self.change_window = change_window

        button_frame = tk.Frame(change_window)
        button_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        chave_button = tk.Button(button_frame, text="Alterar Chave",
                                 command=lambda: self.alterar_encrypt_chave(key_type, api_key))
        chave_button.pack(pady=(0, 5))

        documento_button = tk.Button(button_frame, text="Alterar Documento",
                                     command=lambda: self.alterar_api_keys(key_type))
        documento_button.pack(pady=(0, 5))

    def alterar_encrypt_chave(self, key_type: str, api_key: str):

        folder = 'keys' if getattr(sys, 'frozen', False) else 'docs'
        doc_dir = os.path.join(self.base_path, folder)
        ensure_directory(doc_dir, self.console)
        doc_path = os.path.join(doc_dir, f'{key_type}.crypto')

        try:
            nova_chave = gerar_chave(self.base_path, self.console, key_type)
            self.chave_crypto = nova_chave
        except Exception as e:
            log(self.console, f"Erro ao gerar nova chave: {e}")
            return

        try:
            log(self.console, "Encriptando chave...")
            criptografada = criptografar_credencial(api_key, self.chave_crypto)
            write_file_bytes(doc_path, criptografada, self.console)
        except Exception as e:
            log(self.console, f"Erro ao encriptar chave: {e}")
            return

    def alterar_api_keys(self, key_type: str):
        if not messagebox.askokcancel("Alterar Chave",
                                    f"Tem certeza de que deseja alterar a chave (.crypto) para {key_type}?"):
            return

        folder = 'keys' if getattr(sys, 'frozen', False) else 'docs'
        doc_dir = os.path.join(self.base_path, folder)
        ensure_directory(doc_dir, self.console)
        doc_path = os.path.join(doc_dir, f'{key_type}.crypto')

        try:
            nova_chave = self.requisitar_chave(self.change_window)
            log(self.console, "Encriptando chave...")
            criptografada = criptografar_credencial(nova_chave, self.chave_crypto)
            write_file_bytes(doc_path, criptografada, self.console)
        except Exception as e:
            log(self.console, f"Erro ao encriptar chave: {e}")
            return

    def remover_encrypt(self, key_type: str):
        if not messagebox.askokcancel("Remover Chaves",
                                    f"Tem certeza de que deseja remover as chaves para {key_type}?",
                                    parent=self.option_window):
            return
        
        if not messagebox.askokcancel("Remover Chaves",
                                    f"Essa ação é definitiva e irá excluir ambos os documentos para {key_type}, tem certeza?",
                                    parent=self.option_window):
            return
        
        folder = 'keys' if getattr(sys, 'frozen', False) else 'docs'
        doc_dir = os.path.join(self.base_path, folder)
        ensure_directory(doc_dir, self.console)

        try:
            os.remove(os.path.join(doc_dir, f'{key_type}.crypto'))
            os.remove(os.path.join(doc_dir, f'{key_type}.key'))
            self.option_window.destroy()
            log(self.console, "Chaves removidas com sucesso!")
        except Exception as e:  
            log(self.console, f"Erro ao remover chaves: {e}")
            return

    def requisitar_chave(self, window):
        entry = ChaveAPIEntry(window).result
        if not entry:
            log(self.console, "Operação cancelada!")
            window.destroy()
            raise Exception
        log(self.console, "Chave inserida com sucesso!")
        return entry

class UpdateWindow:
    def __init__(self, debug_mode: bool, repo_path: str):
        """
        Inicializa a interface de atualização.
        """
        self.debug_mode = debug_mode
        self.repo_path = repo_path
        self.chaves_git = None

        # Cria a janela principal
        self.window = tk.Tk()
        self.window.title("Atualização do Aplicativo")
        self.window.geometry("450x300")
        self.window.resizable(False, False)
        center_window(self.window)

        # Widget de log
        self.console = scrolledtext.ScrolledText(self.window, wrap=tk.WORD,
                                                   font=("Courier", 10))
        self.console.place(x=0, y=0, width=450, height=250)
        log(self.console, "Preparando para atualizar...")

        # Frame de botões
        self.button_frame = tk.Frame(self.window)
        self.button_frame.place(x=0, y=250, width=450, height=50)

        # if self.debug_mode:
        #     self._iniciar_debug()
        # else:
        #     # Em release, o botão fechar inicia desabilitado
        #     self.close_button = tk.Button(self.button_frame, text="Fechar",
        #                                   command=self.window.destroy, state='disabled')
        #     self.close_button.place(x=10, y=10, width=150, height=30)
        #     self.window.after(200, self._start_update)

    def _start_update(self):
        """Inicia o processo de atualização."""
        try:
            self.chaves_git = self._search_chaves_github()
            if not self.chaves_git:
                log(self.console, "Chaves Git não encontradas. Abortando atualização.")
                return
            log(self.console, "Chaves Git encontradas. Iniciando atualização...")
            update_application(self.repo_path, self.console, self.debug_mode)
            if hasattr(self, 'close_button'):
                self.close_button.config(state=tk.NORMAL)
        except Exception as e:
            log(self.console, f"Erro durante a atualização: {e}")

    def _iniciar_debug(self):
        """Configura a interface para o modo debug."""
        start_update_button = tk.Button(self.button_frame, text="Iniciar Atualização",
                                        command=self._start_update)
        start_update_button.place(x=50, y=10, width=150, height=30)

        close_button = tk.Button(self.button_frame, text="Fechar",
                                      command=self.window.destroy)
        close_button.place(x=250, y=10, width=150, height=30)

        # Abre a janela para alterar chaves API, se desejado
        if messagebox.askyesno("Debug Mode", "Debug Mode ativado. Deseja alterar Chaves Api?"):
            try:
                AlterarChavesAPIWindow(self.window, self.repo_path).keys
            except Exception as e:
                log(self.console, f"Erro ao alterar chaves: {e}")

    def show(self):
        self.window.mainloop()

    def _search_chaves_github(self):
        folder = 'keys' if getattr(sys, 'frozen', False) else 'docs'
        doc_dir = os.path.join(self.repo_path, folder)
        ensure_directory(doc_dir, self.console)
        key_path = os.path.join(doc_dir, 'github.key')
        crypto_path = os.path.join(doc_dir, 'github.crypto')
        if not os.path.exists(key_path) or not os.path.exists(crypto_path):
            return None
        chaves_git = {
            'key': read_file_bytes(key_path),
            'crypto': read_file_bytes(crypto_path)
        }
        return chaves_git

# =====================================================
# BLOCO PRINCIPAL
# =====================================================

def main():
    DEBUG = not getattr(sys, 'frozen', False)
    base_path = os.path.join(os.path.dirname(sys.executable), '_internal') if DEBUG is False else Path(__file__).resolve().parent.parent

    if DEBUG is False:
        resp = timed_input("Deseja abrir o modo DEBUG? (s/n): ", 10, default="n")
        if resp == "s":
            DEBUG = True
    app = UpdateWindow(DEBUG, base_path)
    app.show()

if __name__ == '__main__':
    main()
