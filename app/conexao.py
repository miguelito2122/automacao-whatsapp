import tkinter as tk
from tkinter import ttk
import threading
from driver import Driver

class Conexao(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.running = False
        self.notebook = parent
        self.criar_widgets_conexao()
    def criar_widgets_conexao(self):
        self.label_conexao = ttk.Label(
            self, 
            text='Conexão: Desconectado.', 
            font=('Courier', 16, 'bold')
        )
        self.label_conexao.place(rely=0.1, relx=0.16)

        self.botao_conectar = ttk.Button(
            self, 
            text='Abrir Whatsapp',
            command=self.iniciar_conexao
        )
        self.botao_conectar.place(rely=0.25, relx=0.345)

        self.label_icone_upload = ttk.Label(
            self, 
            image=self.notebook.icone_whatsapp
        )
        self.label_icone_upload.image = self.notebook.icone_whatsapp
        self.label_icone_upload.place(rely=0.45, relx=0.415)
    def atualizar_status(self, texto, cor):
        self.label_conexao.config(text=f"Conexão: {texto}", foreground=cor)
    def iniciar_conexao(self):
        if not self.running:
            self.atualizar_status("Conectando...", "orange")
            self.running = True
            self.driver = Driver(self)
