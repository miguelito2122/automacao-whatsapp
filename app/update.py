import os
import shutil
import zipfile
import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox
from packaging.version import Version, InvalidVersion

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
        raise ValueError(f"Erro de conexão: {e}")
    
    console.insert(tk.END, f"Status da resposta HTTP: {response.status_code}\n")
    if response.status_code != 200:
        console.insert(tk.END, f"Erro ao baixar o arquivo: {response.status_code}\n")
        raise ValueError(f"Erro ao baixar o arquivo: {response.status_code}")
    
    if not response.content:    
        console.insert(tk.END, "Erro: O conteúdo do arquivo está vazio.\n")
        raise ValueError(f"O conteúdo do arquivo está vazio.")

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

def mock_download_latest_release(repo_url, download_path, console):
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
    console.insert(tk.END, "Extraindo arquivos...\n")
    if not zipfile.is_zipfile(zip_path):
        console.insert(tk.END, "Erro: O arquivo baixado não é um arquivo ZIP válido.\n")
        raise ValueError("O arquivo baixado não é um arquivo ZIP válido.")
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.startswith(f'automacao-whatsapp-main/{item}/') and not file.endswith('/'):
                if file.endswith('update.py'):
                    console.insert(tk.END, f"Preservando: {file}\n")
                    continue

                relative_path = os.path.relpath(file, f'automacao-whatsapp-main/{item}/')
                target_path = os.path.join(extract_to, relative_path)

                os.makedirs(os.path.dirname(target_path), exist_ok=True)

                with zip_ref.open(file) as source, open(target_path, 'wb') as target:
                    shutil.copyfileobj(source, target)
                console.insert(tk.END, f"Extraindo: {file}. Para: {extract_to}\n")


    console.insert(tk.END, "Extração concluída.\n")

def clean_directory(directory, console, exclude_files=[]):
    """Limpa o diretório antes da atualização, preservando arquivos essenciais."""
    console.insert(tk.END, "Limpando o diretório antes da atualização...\n")
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if item in exclude_files:
            console.insert(tk.END, f"Preservando: {item_path}\n")
            continue
        try:
            if os.path.isfile(item_path):
                os.remove(item_path)
                console.insert(tk.END, f"Removido arquivo: {item_path}\n")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                console.insert(tk.END, f"Removido diretório: {item_path}\n")
        except Exception as e:
            console.insert(tk.END, f"Erro ao remover {item_path}: {e}\n")
    console.insert(tk.END, "Limpeza concluída.\n")


# ==========================
# Funções de Verificação de Versão
# ==========================

def check_version(repo_url, app_path, console, branch="main"):
    """Verifica se a versão local é diferente da versão remota."""
    console.insert(tk.END, f"Verificando versão na branch '{branch}'...\n")
    
    # Construindo o caminho para o arquivo de versão remota
    archive_path = f"archive/refs/heads/{branch}.zip"
    if archive_path in repo_url:
        version_url = repo_url.replace(archive_path, f"raw/{branch}/version.txt")
    else:
        console.insert(tk.END, f"Erro: O repo_url não contém o caminho esperado para a branch '{branch}'.\n")
        raise ValueError(f"The repo_url does not contain the expected archive path for branch '{branch}'.")
    
    try:
        # Obter a versão remota
        response = requests.get(version_url, timeout=10)
        if response.status_code != 200:
            console.insert(tk.END, f"Erro ao verificar a versão remota: {response.status_code}\n")
            return False
        remote_version = response.text.strip()
        if not remote_version:
            console.insert(tk.END, "Aviso: A versão remota está vazia. Parando a instalação...\n")
            raise ValueError("A versão remota está vazia.")
        console.insert(tk.END, f"Versão remota na branch '{branch}': {remote_version}\n") # Exemplo: '1.0.0'

        # Obter a versão local
        local_version_path = os.path.join(app_path, 'version.txt')
        if not os.path.exists(local_version_path):
            console.insert(tk.END, "Aviso: O arquivo de versão local não foi encontrado. Continuando a instalação...\n")
            return True
        
        with open(local_version_path, 'r') as file:
            local_version = file.read().strip()
        if not local_version:
            console.insert(tk.END, "Aviso: O arquivo de versão local está vazio. Continuando a instalação...\n")
            return True
        console.insert(tk.END, f"Versão local: {local_version}\n")

        try:
            if Version(local_version) > Version(remote_version):
                console.insert(tk.END, "A versão local é a mais recente.\n")
                return False
            else:
                console.insert(tk.END, "Uma nova versão está disponível.\n")
                return True
        except InvalidVersion as e:
            console.insert(tk.END, f"Erro ao comparar as versões: {e}\n")
            raise ValueError(f"Erro ao comparar as versões: {e}")

    except requests.exceptions.RequestException as e:
        console.insert(tk.END, f"Erro ao verificar a versão remota: {e}\n")
        raise ValueError(f"Erro ao verificar a versão remota: {e}")
    
# ==========================
# Função Principal de Atualização
# ==========================

def update_application(repo_url, repo_path, console):
    """Gerencia o processo de atualização do aplicativo."""
    try:
        console.insert(tk.END, "Iniciando atualização...\n")
        if not check_version(repo_url, repo_path, console, branch='main'):
            console.insert(tk.END, "Nenhuma atualização necessária. Processo interrompido.\n")
            return

        console.insert(tk.END, "Iniciando o download do último release...\n")
        # Diretório de download movido para a raiz do projeto
        download_path = os.path.join(repo_path, 'update')
        os.makedirs(download_path, exist_ok=True)

        USE_MOCK = False  # Altere para False para usar o download real

        if USE_MOCK:
            zip_path = mock_download_latest_release(repo_url, download_path, console)
        else:
            zip_path = download_latest_release(repo_url, download_path, console)

        # Limpar o diretório 'app' antes da atualização
        app_path = os.path.join(repo_path, 'app')
        clean_directory(app_path, console, exclude_files=[
            'update.py'
        ])

        data_path = os.path.join(repo_path, 'data')
        clean_directory(data_path, console, exclude_files=[
            'planilhas'
        ])

        extract_zip_item(zip_path, app_path, 'app', console)
        extract_zip_item(zip_path, data_path, 'data', console)

    
        shutil.rmtree(download_path)

        # Atualizar o arquivo de versão local
        version_url = repo_url.replace('archive/refs/heads/main.zip', 'raw/main/version.txt')
        response = requests.get(version_url, timeout=10)
        with open(os.path.join(repo_path, 'version.txt'), 'w') as file:
            file.write(response.text.strip())
        
        console.insert(tk.END, "Atualização concluída com sucesso!\n")
    except Exception as e:
        console.insert(tk.END, f"Erro durante a atualização: {e}\n")

# ==========================
# Interface Gráfica
# ==========================

def show_update_window():
    """Exibe a interface gráfica para o processo de atualização."""
    update_window = tk.Tk()
    update_window.title("Atualização do Aplicativo")
    update_window.geometry("400x350")
    update_window.resizable(False, False)

    status_label = tk.Label(update_window, text="Status: Atualizando...", font=("Arial", 14, "bold"))
    status_label.pack(pady=10)

    console = scrolledtext.ScrolledText(update_window, wrap=tk.WORD, font=("Courier", 10), height=15, width=60)
    console.pack(padx=10, pady=10)
    console.insert(tk.END, "Preparando para atualizar...\n")

    def start_update():
        repo_url = 'https://github.com/miguelito2122/automacao-whatsapp/archive/refs/heads/main.zip'
        repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        update_application(repo_url, repo_path, console)

        status_label.config(text="Status: Atualização Concluída!")
        close_button.config(state=tk.NORMAL)

    update_window.after(100, start_update)
    close_button = tk.Button(update_window, text="Testar", command=start_update, state='active')
    close_button.pack(pady=10)

    update_window.mainloop()

if __name__ == '__main__':
    show_update_window()