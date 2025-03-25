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
        raise ValueError("O arquivo baixado não é um arquivo ZIP válido.")
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    
    console.insert(tk.END, "Extração concluída.\n")

def update_application(repo_url, app_path, console):
    try:
        console.insert(tk.END, "Iniciando atualização...\n")
        download_path = os.path.join(app_path, 'update')
        os.makedirs(download_path, exist_ok=True)
        zip_path = download_latest_release(repo_url, download_path, console)
        extract_zip(zip_path, app_path, console)
        shutil.rmtree(download_path)
        console.insert(tk.END, "Atualização concluída com sucesso!\n")
    except Exception as e:
        console.insert(tk.END, f"Erro durante a atualização: {e}\n")

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