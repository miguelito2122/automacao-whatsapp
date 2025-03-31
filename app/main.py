"""
Este módulo contém a classe Root.
Que representa a chamada principal para o aplicativo.
"""
import sys
import os
from tkinter import messagebox
try:
    from pathlib import Path
    from root import Root
    from config import launch_error, checar_updater, atualizar_updater
except ImportError as e:
    messagebox.showerror('Erro', f'Erro ao importar módulos (main.py)\nErro: {e}')
    sys.exit(1)


def get_base_path():
    """ Resolve caminhos para ambos os modos: desenvolvimento e empacotado """
    try:
        if getattr(sys, 'frozen', False):
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(sys.executable)))
            print(base_path)
        else:
            base_path = Path(__file__).resolve().parent.parent

        return base_path
    except AttributeError as e:
        launch_error('Erro ao obter o caminho base (main.py)', e)

if __name__ == '__main__':
    try:
        path = get_base_path()
        check = checar_updater(path)
        if check:
            atualizar_updater(path)
            sys.exit(0)
        else:
            app = Root(path)
            app.mainloop()
    except Exception as e:
        launch_error('Erro ao abrir o aplicativo (main.py)', e)
