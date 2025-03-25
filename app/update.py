import os
import shutil
import zipfile
import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox

def download_latest_release(repo_url, download_path, console):
    console.insert(tk.END, f"Baixando o último release de: {repo_url}\n")
    try:
        # Tenta realizar a requisição HTTP
        response = requests.get(repo_url, timeout=10)
    except requests.exceptions.RequestException as e:
        # Trata erros de conexão
        console.insert(tk.END, f"Erro de conexão: {e}\n")
        raise ValueError(f"Erro de conexão: {e}")
    
    # Log do status da resposta HTTP
    console.insert(tk.END, f"Status da resposta HTTP: {response.status_code}\n")
    
    if response.status_code != 200:
        # Trata erros de resposta HTTP
        console.insert(tk.END, f"Erro ao baixar o arquivo: {response.status_code}\n")
        raise ValueError(f"Erro ao baixar o arquivo: {response.status_code}")
    
    # Salva o conteúdo do arquivo baixado
    zip_path = os.path.join(download_path, 'latest_release.zip')
    with open(zip_path, 'wb') as file:
        file.write(response.content)
    
    # Log do tamanho do arquivo baixado
    file_size = os.path.getsize(zip_path)
    console.insert(tk.END, f"Tamanho do arquivo baixado: {file_size} bytes\n")
    
    # Verifica se o arquivo baixado está vazio
    if file_size == 0:
        console.insert(tk.END, "Erro: O arquivo baixado está vazio.\n")
        raise ValueError("O arquivo baixado está vazio.")
    
    console.insert(tk.END, "Download concluído.\n")
    return zip_path

def extract_zip(zip_path, extract_to, console):
    console.insert(tk.END, "Extraindo arquivos...\n")
    
    # Verifica se o arquivo é um ZIP válido
    if not zipfile.is_zipfile(zip_path):
        console.insert(tk.END, "Erro: O arquivo baixado não é um arquivo ZIP válido.\n")
        raise ValueError("O arquivo baixado não é um arquivo ZIP válido.")
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    
    console.insert(tk.END, "Extração concluída.\n")

def clean_directory(directory, console, exclude_files=[]):
    console.insert(tk.END, "Limpando o diretório antes da atualização...\n")
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if item in exclude_files:
            console.insert(tk.END, f"Preservando: {item_path}\n")
            continue
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
            console.insert(tk.END, f"Removido diretório: {item_path}\n")
    console.insert(tk.END, "Limpeza concluída.\n")

def check_version(repo_url, app_path, console):
    console.insert(tk.END, "Verificando versão...\n")
    
    # URL do arquivo de versão no repositório remoto
    version_url = repo_url.replace('archive/refs/heads/main.zip', 'raw/main/version.txt')
    try:
        # Faz o download do arquivo de versão remoto
        response = requests.get(version_url, timeout=10)
        if response.status_code != 200:
            raise ValueError(f"Erro ao obter a versão remota: {response.status_code}")
        remote_version = response.text.strip()
        console.insert(tk.END, f"Versão remota: {remote_version}\n")
    except requests.exceptions.RequestException as e:
        console.insert(tk.END, f"Erro ao verificar a versão remota: {e}\n")
        raise ValueError(f"Erro ao verificar a versão remota: {e}")

    # Verifica a versão local
    local_version_file = os.path.join(os.path.dirname(app_path), 'version.txt')
    if os.path.exists(local_version_file):
        with open(local_version_file, 'r') as file:
            local_version = file.read().strip()
        console.insert(tk.END, f"Versão local: {local_version}\n")
    else:
        console.insert(tk.END, "Versão local não encontrada. Atualização necessária.\n")
        return True  # Atualização necessária

    # Compara as versões
    if remote_version != local_version:
        console.insert(tk.END, "Versões diferentes. Atualização necessária.\n")
        return True  # Atualização necessária
    else:
        console.insert(tk.END, "Versões iguais. Nenhuma atualização necessária.\n")
        return False  # Nenhuma atualização necessária
    
def update_application(repo_url, app_path, console):
    try:
        console.insert(tk.END, "Iniciando atualização...\n")

        if not check_version(repo_url, app_path, console):
            console.insert(tk.END, "Nenhuma atualização necessária.\n")
            return

        download_path = os.path.join(app_path, 'update')
        os.makedirs(download_path, exist_ok=True)
        zip_path = download_latest_release(repo_url, download_path, console)

        # Verifica se o arquivo baixado é válido antes de limpar o diretório
        if not zipfile.is_zipfile(zip_path):
            console.insert(tk.END, "Erro: O arquivo baixado não é um arquivo ZIP válido.\n")
            raise ValueError("O arquivo baixado não é um arquivo ZIP válido.")

        # Limpa o diretório, preservando arquivos essenciais
        clean_directory(app_path, console, exclude_files=['update.py', 'version.txt'])
        extract_zip(zip_path, app_path, console)
        shutil.rmtree(download_path)

        # Atualiza a versão local
        version_url = repo_url.replace('archive/refs/heads/main.zip', 'raw/main/version.txt')
        response = requests.get(version_url, timeout=10)
        with open(os.path.join(app_path, 'version.txt'), 'w') as file:
            file.write(response.text.strip())
        
        console.insert(tk.END, "Atualização concluída com sucesso!\n")
    except Exception as e:
        console.insert(tk.END, f"Erro durante a atualização: {e}\n")

def mock_download_latest_release(repo_url, download_path, console):
    console.insert(tk.END, "Mockando o download do último release...\n")
    zip_path = os.path.join(download_path, 'latest_release.zip')
    with zipfile.ZipFile(zip_path, 'w') as zip_ref:
        zip_ref.writestr('dummy_file.txt', 'conteúdo de teste')
    console.insert(tk.END, f"Mock concluído. Arquivo ZIP criado em: {zip_path}\n")
    return zip_path

def show_update_window():
    # Configuração da janela principal
    update_window = tk.Tk()
    update_window.title("Atualização do Aplicativo")
    update_window.geometry("500x400")
    update_window.resizable(False, False)

    # Status
    status_label = tk.Label(update_window, text="Status: Atualizando...", font=("Arial", 14, "bold"))
    status_label.pack(pady=10)

    # Console (textbox)
    console = scrolledtext.ScrolledText(update_window, wrap=tk.WORD, font=("Courier", 10), height=15, width=60)
    console.pack(padx=10, pady=10)
    console.insert(tk.END, "Preparando para atualizar...\n")

    # Botão para fechar
    def close_window():
        update_window.destroy()

    close_button = tk.Button(update_window, text="Fechar", command=close_window, state=tk.DISABLED)
    close_button.pack(pady=10)

    # Iniciar atualização
    def start_update():
        repo_url = 'https://github.com/miguelito2122/automacao-whatsapp/archive/refs/heads/main.zip'
        app_path = os.path.dirname(os.path.abspath(__file__))
        update_application(repo_url, app_path, console)
        status_label.config(text="Status: Atualização Concluída!")
        close_button.config(state=tk.NORMAL)

    # Executar a atualização após a janela ser carregada
    update_window.after(100, start_update)

    update_window.mainloop()

if __name__ == '__main__':
    show_update_window()