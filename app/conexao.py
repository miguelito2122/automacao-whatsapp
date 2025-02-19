import tkinter as tk
from tkinter import ttk
from root import ToolTip, carregar_imagens

class Conexao(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.carregar_imagens()
        self.criar_widgets_conexao()
    def carregar_imagens(self):
        self.icone_refresh, self.icone_show, self.icone_upload, self.icone_whatsapp, self.icone_send = carregar_imagens()
    def criar_widgets_conexao(self):
        self.label_conexao = ttk.Label(
            self, 
            text='Conexão: Desconectado.', 
            font=('Courier', 16, 'bold')
        )
        self.label_conexao.place(rely=0.1, relx=0.16)

        self.botao_conectar = ttk.Button(
            self, 
            text='Abrir Whatsapp'
        )
        self.botao_conectar.place(rely=0.25, relx=0.345)

        self.label_icone_upload = ttk.Label(
            self, 
            image=self.icone_whatsapp
        )
        self.label_icone_upload.image = self.icone_whatsapp
        self.label_icone_upload.place(rely=0.45, relx=0.415)
