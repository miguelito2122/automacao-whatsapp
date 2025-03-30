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
    from config import launch_error
except ImportError as e:
    messagebox.showerror('Erro', f'Erro ao importar módulos (main.py)\nErro: {e}')
    sys.exit(1)


def get_base_path():
    """ Resolve caminhos para ambos os modos: desenvolvimento e empacotado """
    try:
        if getattr(sys, 'frozen', False):
            base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
            print(base_path)
        else:
            base_path = Path(__file__).resolve().parent.parent

        return base_path
    except AttributeError as e: 
        launch_error('Erro ao obter o caminho base (main.py)', e)

if __name__ == '__main__':
    try:
        app = Root(get_base_path())
        app.mainloop()
    except Exception as e:
        launch_error('Erro ao abrir o aplicativo (main.py)', e)
