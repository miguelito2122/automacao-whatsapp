"""
Este módulo contém a classe Root, que representa a janela principal do aplicativo.
"""
from tkinter import messagebox
import os
import time
import sys
import subprocess
import threading
import tkinter as tk
try:
    from config import launch_error, center_window, log, read_file_bytes, buscar_arquivo
    from security import descriptografar_credencial
    from notebook import Notebook

except ImportError as e:
    messagebox.showerror('Erro', f'Erro ao importar módulos(root.py)\nErro: {e}')
    sys.exit(1)

class Root(tk.Tk):
    def __init__(self, master):
        """
        Inicializa a janela principal do aplicativo.

        Este construtor configura a janela principal do aplicativo, definindo seu
        título, tamanho e propriedades de layout. Ele também inicializa o processo
        de atualização do aplicativo e o componente notebook.

        Atributos:
            notebook (Notebook): O componente notebook principal do aplicativo.
        """
        self.notebook = None

        super().__init__()
        self.main = master
        self.ia_key = None
        self.github_key = None
        self.app_version = None
        self.updater_version = None
        self.remote_app_version = None
        self.remote_updater_version = None
        self.title("Automação de Avaliações")
        self.geometry('400x300')
        self.resizable(False, False)
        center_window(self)


        self.status_label = tk.Label(
            self, 
            text="Status: Inicializando...",
            font=("Arial", 10)
        )
        self.status_label.place(relx=0, rely=0.5, relheight=0.1, relwidth=1)

        btn_close = tk.Button(self, text="Começar", command=self.carregar_dados)
        btn_close.place(x=180, y=10)

    def run(self):
        """
        Executa o loop principal da interface gráfica.
        """

        threading.Thread(target=self.carregar_dados, daemon=True).start()

        self.mainloop()
    def carregar_dados(self):
        """
        Carrega os dados necessários para o aplicativo.
        """

        self.status_label.config(text="Status: Carregando dados para aplicação...")
        self.status_label.update_idletasks()

        try:
            self.status_label.config(text="Status: Carregando versões locais...")
            time.sleep(1.5)
            self.app_version = read_file_bytes(self.main.versions_path[0]).decode('utf-8').strip()
            self.updater_version = read_file_bytes(self.main.versions_path[1]).decode('utf-8').strip()
        except Exception as e:
            launch_error('Erro ao carregar versões (root.py)', e)

        try:
            if not self.main.missing_keys:
                credenciais = self.carregar_chaves_descriptografadas(self.main.keys)
                self.status_label.config(text="Status: Chaves API carregadas com sucesso!")
                time.sleep(1.5)
                self.ia_key = credenciais.get('ia')
                self.github_key = credenciais.get('github')

            else:
                self.status_label.config(text="Status: Chaves API ausentes!")
                self.after(0, self.iniciar_notebook)
                return
        except Exception as e:
            launch_error('Erro ao carregar chaves API (root.py)', e)

        if not self.main.missing_keys:
            try:
                if self.github_key:
                    self.status_label.config(text="Status: Buscando Versões Remotas...")
                    time.sleep(1.5)
                    self.remote_updater_version, self.remote_app_version = self.carregar_versoes_remotas(self.github_key)
            except Exception as e:
                launch_error('Erro ao carregar versões remotas (root.py)', e)

            if self.updater_version != self.remote_updater_version:
                self.status_label.config(text="Status: Atualizando o Updater...")
                time.sleep(1.5)
                if self.main.debug:
                    self.status_label.config(text="Status: Modo Debug - Atualização do Updater não realizada.")
                else:
                    try:
                        self.status_label.config(text="Status: Atualizando o Updater...")
                        time.sleep(1.5)
                        self.atualizar_updater()
                    except Exception as e:
                        launch_error('Erro ao atualizar o updater', e)

            if self.app_version != self.remote_app_version:
                self.status_label.config(text="Status: Atualizando o Aplicativo...")
                time.sleep(1.5)
                if self.main.debug:
                    self.status_label.config(text="Status: Modo Debug - Atualização do Aplicativo não realizada.")
                else:
                    try:
                        self.status_label.config(text="Status: Atualizando o Aplicativo...")
                        time.sleep(1.5)
                        self.atualizar_aplicativo()
                    except Exception as e:
                        launch_error('Erro ao atualizar o aplicativo', e)

        self.status_label.config(text="Status: Aplicativo carregado com sucesso!")
        time.sleep(1.0)
        self.status_label.config(text="Status: Iniciando o aplicativo...")

        try:
            self.after(0, self.iniciar_notebook)
        except Exception as e:
            launch_error('Erro ao iniciar o notebook', e)

    def iniciar_notebook(self):
        """
        Inicia o notebook do aplicativo.
        Cria uma instância do componente Notebook e a exibe na janela principal.
        """
        self.notebook = Notebook(self)

    def atualizar_updater(self):
        """
        Atualiza o updater.exe do base_path.

        Se o arquivo update.exe existir, ele é sobrescrito com o
        último release do update.exe da versão atual do repositório.

        Se for em modo debug é feito mock do updater para a pasta release.

        :param base_path: O diretório base do aplicativo.

        :return: None
        """
        pass

    def atualizar_aplicativo(self):
        """
        Atualiza o aplicativo do base_path.

        Se o arquivo update.exe existir, ele é executado 
        na versão atual do repositório.

        Se for em modo debug é feito mock do latest_release.zip para a pasta release.

        :param base_path: O diretório base do aplicativo.

        :return: None
        """
        # try:
        #     if getattr(sys, 'frozen', False):
        #         # Executa o update.exe (gerado pelo PyInstaller)
        #         process = subprocess.run(
        #             [update_exec],
        #             check=True,
        #             stdout=subprocess.PIPE,
        #             stderr=subprocess.PIPE,
        #             text=True  # Windows: exibe o console
        #         )
        #         print("SAÍDA:", process.stdout)
        #         print("ERROS", process.stderr)
        #         sys.exit(0)
        #     else:
        #         # Ambiente de desenvolvimento
        #         subprocess.run([sys.executable, update_exec], check=True)
        #         sys.exit(0)
        # except Exception as e:
        #     launch_error('Erro ao atualizar o aplicativo', e)
    def carregar_versoes_remotas(self, key):
        """
        Carrega as versões remotas do repositório.
        Para comparar com a versão local.
        """

        try:
            # Obter versão do updater
            versao_updater = buscar_arquivo(api_chave=key, nome_arquivo='updaterversion.txt')
            log(console=None, mensagem=f"Versão do updater obtida: {versao_updater}")

            # Obter versão principal
            versao_aplicativo = buscar_arquivo(api_chave=key, nome_arquivo='version.txt')
            log(console=None, mensagem=f"Versão do aplicativo obtida: {versao_aplicativo}")

            return versao_updater, versao_aplicativo

        except Exception as e:
            launch_error('Erro ao verificar versão remota', e)
            return None, None

    def carregar_chaves_descriptografadas(self, keys_dict):
        """
        Carrega e descriptografa chaves API.

        Itera sobre os tipos de chave ('ia' e 'github'), obtém os caminhos dos arquivos
        de chave e de dados criptografados do dicionário `keys_dict`, e tenta
        descriptografar os dados usando a chave Fernet correspondente.

        Parâmetros:
            keys_dict (dict): Dicionário contendo os caminhos para os arquivos de chave
            e dados criptografados, com extensões '.key' e '.crypto'.

        Retorna:
            dict: Um dicionário contendo as credenciais descriptografadas para cada tipo
            de chave, ou None em caso de erro.
        """

        credenciais = {}
        for key_type in ['ia', 'github']:
            # Obter caminhos dos arquivos
            chave_key = keys_dict.get(f"{key_type}.key")
            chave_crypto = keys_dict.get(f"{key_type}.crypto")

            if chave_key and chave_crypto:
                try:
                    # Ler chave Fernet
                    fernet_key = read_file_bytes(chave_key)

                    # Ler dados criptografados
                    encrypted_data = read_file_bytes(chave_crypto)

                    # Descriptografar
                    credenciais[key_type] = descriptografar_credencial(encrypted_data, fernet_key)

                except Exception as e:
                    launch_error(f'Erro ao processar chaves {key_type}', e)
                    return None
        return credenciais

if __name__ == '__main__':
    app = Root()
    app.run()



        # try:
        #     self.base_path = base_path
        #     self.checar_atualizacao(base_path)
        # except AttributeError as e:
        #     launch_error('Erro ao obter o caminho base (root.py)', e)
        # try:
        #     self.notebook = Notebook(self, self.base_path)
        # except Exception as e:
        #     launch_error('Erro ao abrir Notebook (root.py)', e)
    # def checar_atualizacao(self, base_path):
    #     """
    #     Atualiza o aplicativo verificando se há uma versão mais recente no repositório.

    #     Se o arquivo update.py existir, ele é executado com o interpretador Python para
    #     verificar se há uma versão mais recente do aplicativo no repositório. Se uma versão
    #     mais recente for encontrada, o aplicativo é atualizado automaticamente.

    #     :return: None
    #     """

        # versao_atual = open(version_txt, 'r', encoding='utf-8').readline().strip()

        # if response.content.decode('utf-8') == versao_atual: #Colocar (NOT) AQUI NO FINAL
        #     messagebox.showinfo('Atualização',
        #                         'A versão mais recente do aplicativo ja foi instalada')
        #     return

        # resposta = messagebox.askyesno('Atualização disponível',
        #                                 'Deseja atualizar para a versão mais recente?')

        # if resposta:
        #     self.destroy()
        # else:
        #     messagebox.showinfo('Atualização', 'Atualização cancelada pelo usuário')
        #     return


