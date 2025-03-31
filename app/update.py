"""
Este script é responsável por atualizar o aplicativo para a última versão disponível no repositório remoto.
"""
import sys
from pathlib import Path
import os
import shutil
import zipfile
import tkinter as tk
from tkinter import scrolledtext
import requests

# ==========================
# Funções de Download e Mock
# ==========================

def download_latest_release(repo_url, download_path, console):
    """Faz o download do último release do repositório remoto."""
    console.insert(tk.END, f"Baixando o último release de: {repo_url}\n")
    try:
        response = requests.get(repo_url, timeout=10)
    except requests.exceptions.RequestException as e:
        console.insert(tk.END, f"Erro de conexão: {e}\n")
        raise ValueError(f"Erro de conexão: {e}") from e
    console.insert(tk.END, f"Status da resposta HTTP: {response.status_code}\n")
    if response.status_code != 200:
        console.insert(tk.END, f"Erro ao baixar o arquivo: {response.status_code}\n")
        raise ValueError(f"Erro ao baixar o arquivo: {response.status_code}")
    if not response.content:    
        console.insert(tk.END, "Erro: O conteúdo do arquivo está vazio.\n")
        raise ValueError("O conteúdo do arquivo está vazio.")
    zip_path = os.path.join(download_path, 'latest_release.zip')
    with open(zip_path, 'wb') as file:
        file.write(response.content)
    file_size = os.path.getsize(zip_path)
    console.insert(tk.END, f"Tamanho do arquivo baixado: {file_size} bytes\n")
    if file_size == 0:
        console.insert(tk.END, "Erro: O arquivo baixado está vazio.\n")
        raise ValueError("O arquivo baixado está vazio.")
    console.insert(tk.END, "Download concluído.\n")
    return zip_path

def mock_download_latest_release(download_path, console):
    """Mock do processo de download para testes."""
    console.insert(tk.END, "Mockando o download do último release...\n")
    zip_path = os.path.join(download_path, 'latest_release.zip')
    with zipfile.ZipFile(zip_path, 'w') as zip_ref:
        zip_ref.writestr('dummy_file.txt', 'conteúdo de teste')
        zip_ref.writestr('config.json', '{"key": "value"}')
        zip_ref.writestr('README.md', '# Arquivo de teste\nEste é um mock de atualização.')
    console.insert(tk.END, f"Mock concluído. Arquivo ZIP criado em: {zip_path}\n")
    return zip_path

# ==========================
# Funções de Manipulação de Arquivos
# ==========================

def extract_zip_item(zip_path, extract_to, item, console):
    """Extrai os arquivos de um ZIP para o diretório especificado."""
    console.insert(tk.END, f"Extraindo arquivos para {extract_to}...\n")
    if not zipfile.is_zipfile(zip_path):
        console.insert(tk.END, "Erro: O arquivo baixado não é um arquivo ZIP válido.\n")
        raise ValueError("O arquivo baixado não é um arquivo ZIP válido.")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.startswith(f'automacao-whatsapp-main/{item}/') and not file.endswith('/'):
                if file.endswith('update.py'):
                    continue

                relative_path = os.path.relpath(file, f'automacao-whatsapp-main/{item}/')
                target_path = os.path.join(extract_to, relative_path)

                os.makedirs(os.path.dirname(target_path), exist_ok=True)

                with zip_ref.open(file) as source, open(target_path, 'wb') as target:
                    shutil.copyfileobj(source, target)

    console.insert(tk.END, "Extração concluída.\n")

def clean_directory(directory, console, exclude_files=None):
    """Limpa o diretório antes da atualização, preservando arquivos essenciais."""
    if exclude_files is None:
        exclude_files = []
    console.insert(tk.END, f"Limpando o diretório {directory} antes da atualização...\n")
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if item in exclude_files:
            continue
        try:
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        except (OSError, PermissionError) as e:
            console.insert(tk.END, f"Erro ao remover {item_path}: {e}\n")
    console.insert(tk.END, "Limpeza concluída.\n")

# ==========================
# Função Principal de Atualização
# ==========================

def update_application(repo_url, repo_path, console, debug=False):
    """Gerencia o processo de atualização do aplicativo."""
    try:
        console.insert(tk.END, "Iniciando atualização...\n")

        console.insert(tk.END, "Iniciando o download do último release...\n")
        # Diretório de download movido para a raiz do projeto
        download_path = os.path.join(repo_path, 'release')
        os.makedirs(download_path, exist_ok=True)

        if debug:
            mock_download_latest_release(download_path, console)
        else:
            download_latest_release(repo_url, download_path, console)

        # # Limpar o diretório 'app' antes da atualização
        # app_path = os.path.join(repo_path, 'app')
        # clean_directory(app_path, console, exclude_files=[
        #     'update.py'
        # ])

        # data_path = os.path.join(repo_path, 'data')
        # clean_directory(data_path, console, exclude_files=[
        #     'planilhas'
        # ])
        # extract_zip_item(zip_path, app_path, 'app', console)
        # extract_zip_item(zip_path, data_path, 'data', console)
        # shutil.rmtree(download_path)
        # # Atualizar o arquivo de versão local
        # version_url = repo_url.replace('archive/refs/heads/main.zip', 'raw/main/version.txt')
        # response = requests.get(version_url, timeout=10)
        # with open(os.path.join(repo_path, 'version.txt'), 'w', encoding='utf-8') as file:
        #     file.write(response.text.strip())
        console.insert(tk.END, "Atualização concluída com sucesso!\n")
    except (requests.exceptions.RequestException, ValueError, OSError, PermissionError) as e:
        console.insert(tk.END, f"Erro durante a atualização: {e}\n")

# ==========================
# Interface Gráfica
# ==========================
def centralizar_tela(tela):
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
def show_update_window(debug=False):
    """Exibe a interface gráfica para o processo de atualização."""
    update_window = tk.Tk()
    update_window.title("Atualização do Aplicativo")
    update_window.geometry("400x350")
    update_window.resizable(False, False)

    centralizar_tela(update_window)

    status_label = tk.Label(update_window, text="Status: Atualizando...",
                            font=("Arial", 14, "bold"))
    status_label.pack(pady=10)

    console = scrolledtext.ScrolledText(update_window, wrap=tk.WORD,
                                        font=("Courier", 10), height=15, width=60)
    console.pack(padx=10, pady=10)
    console.insert(tk.END, "Preparando para atualizar...\n")

    if getattr(sys, 'frozen', False):
        debug = True # Alterado para True para Testes
        repo_path = os.path.join(os.path.dirname(sys.executable), '_internal')
        print('release',repo_path)
    else:
        debug = True
        repo_path = Path(__file__).resolve().parent.parent
        print('debug',repo_path)

    def start_update(debug=False):
        """Inicia o processo de atualização."""
        repo_url = 'https://github.com/miguelito2122/automacao-whatsapp/archive/refs/heads/main.zip'

        try:
            update_application(repo_url, repo_path, console, debug)
            status_label.config(text="Status: Atualização Concluída!")
            close_button.config(state=tk.NORMAL)
        except Exception as e:
            console.insert(tk.END, f"Erro durante a atualização: {e}\n")

    button_frame = tk.Frame(update_window)
    button_frame.pack(pady=5)

    if debug:
        start_update_button = tk.Button(button_frame, text="Iniciar Atualização",
                                        command=lambda: start_update(debug=True))
        start_update_button.pack(pady=10, side='left')

    close_button = tk.Button(button_frame, text="Fechar",
                             command=update_window.destroy, state='disabled')
    close_button.pack(pady=10, side='right')

    update_window.mainloop()

    if not debug:
        update_window.after(200, start_update)

if __name__ == '__main__':
    show_update_window()


# ==========================
# Fim do Script
# ==========================
