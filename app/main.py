"""
Este módulo contém a classe Main,
que representa a chamada principal para o aplicativo.
"""
# -*- coding: utf-8 -*-

try:
    import sys
    import os
    import threading
    import time
    from tkinter import messagebox
    import tkinter as tk
except ImportError as e:
    raise ImportError(f'Erro ao importar módulos (main.py)\nErro: {e}') from e
try:
    from pathlib import Path
    from root import Root
    from config import launch_error, ensure_directory, timed_input, log, SplashScreen
except ImportError as e:
    messagebox.showerror('Erro', f'Erro ao importar módulos (main.py)\nErro: {e}')
    sys.exit(1)

class Main:
    """
    Classe principal do aplicativo, responsável por gerenciar a inicialização
    e o carregamento do aplicativo.
    Esta classe é responsável por criar a janela de splash, carregar os
    componentes do aplicativo e iniciar a interface gráfica principal.

    Atributos:
        root (tk.Tk): Janela principal do aplicativo.
        splash (SplashScreen): Tela de splash do aplicativo.
        base_path (str): Caminho base do aplicativo.
        keys_path (str): Caminho para o diretório de chaves.
        versions_path (list): Caminho para o arquivo de versão.
        update_path (str): Caminho para o diretório de atualizações.
        updater_exec (bool): Indica se o instalador de atualização foi encontrado.
        img_path (str): Caminho para o diretório de imagens.
        debug (bool): Indica se o modo de depuração está ativado.

    Métodos:
        __init__(): Inicializa o aplicativo e gerencia a sequência de carregamento.
        carregar_aplicativo(): Realiza a inicialização dos componentes do aplicativo
        exibindo logs na splash.
        finalizar(): Interrompe o splash e agenda o fechamento das janelas.
        iniciar_aplicativo(): Fecha a janela de splash e encerra a aplicação.
        obter_caminho_base(): Obtém o caminho base do aplicativo.
        obter_caminho_chaves(): Obtém o caminho para o diretório de chaves.
        obter_caminho_versoes(): Obtém o caminho para os textos de versionamento.
        obter_caminho_update(): Obtém o caminho para o diretório de atualizações
        obter_caminho_imagens(): Obtém o caminho para o diretório de imagens.
        e consta a existência do executável do instalador de atualização.
    """
    def __init__(self):
        """Inicializa o aplicativo e gerencia a sequência de carregamento."""
        self.root = tk.Tk()
        self.root.withdraw()  # Oculta a janela principal durante o splash

        # Inicializa a tela de splash
        self.splash = SplashScreen(self.root)

        # Inicializações dos caminhos
        self.base_path = None
        self.keys_path = None
        self.keys = {}
        self.missing_keys = False
        self.versions_path = None
        self.update_path = None
        self.updater_exec = None
        self.img_path = None

        # Configuração do modo DEBUG
        try:
            self.debug = not getattr(sys, 'frozen', False)
            if not self.debug:
                resp = timed_input("Deseja abrir o modo DEBUG? (s/n): ", 10, default="n")
                if resp.lower() == "s":
                    self.debug = True
        except AttributeError:
            self.debug = False

        # Inicia a barra de progresso e carrega o aplicativo em thread separada
        self.splash.start()
        threading.Thread(target=self.carregar_aplicativo, daemon=True).start()

        # Inicia o loop da interface gráfica
        self.root.mainloop()

    def carregar_aplicativo(self):
        """Realiza a inicialização dos componentes do aplicativo exibindo logs na splash."""
        log(self.splash.console, 'Iniciando o aplicativo...')

        if self.debug:
            log(self.splash.console, 'Modo DEBUG ativado.')
            self.splash.console.see("end")
            self.splash.window.overrideredirect(False)
        else:
            log(self.splash.console, 'Modo DEBUG desativado.')

        self.base_path = self.obter_caminho_base()
        log(self.splash.console, 'Base carregada.')

        self.keys_path = self.obter_caminho_chaves()
        log(self.splash.console, 'Chaves carregadas.')

        self.versions_path = self.obter_caminho_versoes()
        log(self.splash.console, 'Versões carregadas.')

        self.update_path = self.obter_caminho_update()
        log(self.splash.console, 'Diretório de update pronto.')

        self.keys, self.missing_keys = self.obter_chaves()
        log(self.splash.console, 'As chaves foram carregadas.')

        self.img_path = self.obter_caminho_imagens()
        log(self.splash.console, 'Imagens carregadas.')

        if self.missing_keys:
            log(self.splash.console, 'Alguma chave está ausente. Solicite ao desenvolvedor.')
        else:
            log(self.splash.console, 'Chaves obtidas.')

        log(self.splash.console, 'Inicialização completa.')
        time.sleep(0.5)  # Simula tempo de carregamento

        # Agenda a finalização do carregamento na thread principal
        self.root.after(0, self.finalizar)

    def finalizar(self):
        """Interrompe o splash e agenda o fechamento das janelas."""

        # Permite que o usuário visualize o fim do carregamento por 3 segundos
        if not self.debug:
            self.splash.stop()
            self.root.after(3000, self.iniciar_aplicativo)
        else:
            self.splash.progress.config(length=160)
            btn_close = tk.Button(self.splash.window, text="Fechar", command=self.fechar_janelas)
            btn_close.place(x=175, y=115)

    def fechar_janelas(self):
        """Fecha a janela de splash e encerra a aplicação."""
        self.splash.stop()
        self.splash.destroy()
        self.root.destroy()
        app = Root(self)
        app.run()

    def iniciar_aplicativo(self):
        """Fecha a janela de splash e encerra a aplicação."""

        self.splash.destroy()
        self.root.destroy()

        app = Root(self)
        app.run()

    def obter_caminho_base(self) -> str:
        try:
            path_exec = os.path.abspath(os.path.dirname(sys.executable))
            path_dev = Path(__file__).resolve().parent.parent
            base_path = path_exec if getattr(sys, 'frozen', False) else path_dev
            return base_path
        except Exception as e:
            launch_error('Erro ao obter o caminho base (main.py)', e)

    def obter_caminho_chaves(self) -> str:
        try:
            keys_dir = '_internal/keys' if getattr(sys, 'frozen', False) else 'docs'
            keys_path = os.path.join(self.base_path, keys_dir)
            ensure_directory(keys_path)
            return keys_path
        except Exception as e:
            launch_error('Erro ao obter o diretórios de chaves (main.py)', e)

    def obter_caminho_versoes(self) -> list:
        try:
            if getattr(sys, 'frozen', False):
                version_path = os.path.join(self.base_path, '_internal/version.txt')
                updater_version_path = os.path.join(self.base_path, '_internal/updaterversion.txt')
            else:
                version_path = os.path.join(self.base_path, 'version.txt')
                updater_version_path = os.path.join(self.base_path, 'updaterversion.txt')
            if not os.path.exists(version_path) or not os.path.exists(updater_version_path):
                log(self.splash.console, f"Arquivo de versão não encontrado. {version_path}, {updater_version_path}")
            return [version_path, updater_version_path]
        except Exception as e:
            launch_error('Erro ao obter as versões (main.py)', e)

    def obter_caminho_update(self) -> str:
        try:
            release_path = os.path.join(self.base_path, 'release')
            updater_path = os.path.join(self.base_path, 'Updater')
            if not os.path.exists(updater_path + '.exe') and not os.path.exists(updater_path):
                self.updater_exec = False
                log(self.splash.console,
                    f"Instalador de atualização não encontrado. {updater_path}")
            else:
                self.updater_exec = True
            ensure_directory(release_path)
            return release_path, updater_path
        except Exception as e:
            launch_error('Erro ao obter o diretório de atualização (main.py)', e)

    def obter_caminho_imagens(self) -> str:
        try:
            path = '_internal/data' if getattr(sys, 'frozen', False) else 'data'
            img_path = os.path.join(self.base_path, path)
            ensure_directory(img_path)
            return img_path
        except Exception as e:
            launch_error('Erro ao obter o diretório de imagens (main.py)', e)

    def obter_chaves(self):
        keys_path = self.keys_path
        keys = {}
        missing_keys = []
        chaves = {
            'ia': (".key", ".crypto"),
            'github': (".key", ".crypto"),
            }
        try:
            for key_type, extensions in chaves.items():
                for extension in extensions:
                    chave_path = os.path.join(keys_path, f'{key_type}{extension}')
                    if not os.path.exists(chave_path):
                        missing_keys.append(f"{key_type}{extension}")
                        log(self.splash.console, f"Chave {key_type}{extension} não encontrada.")
                    else:
                        keys[f"{key_type}{extension}"] = chave_path
        except Exception as e:
            launch_error('Erro ao obter as chaves (main.py)', e)

        return keys, missing_keys

if __name__ == '__main__':
    Main()
