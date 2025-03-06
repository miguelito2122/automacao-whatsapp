from conexao import Conexao
from checkin import AppCheckin
from tkinter import ttk

class Notebook(ttk.Notebook):
    def __init__(self, parent):
        super().__init__(parent)
        self.conexao = Conexao(self)
        self.add(self.conexao, text='Conexão')
        self.checkin = AppCheckin(self)
        self.add(self.checkin, text='Check-in')
