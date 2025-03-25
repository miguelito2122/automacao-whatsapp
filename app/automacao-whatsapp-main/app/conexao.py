import tkinter as tk
from tkinter import ttk
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

        self.botao_tentar_novamente = ttk.Button(
            self, 
            text='Tentar Novamente',
            command=self.tentar_novamente
        )
        self.botao_tentar_novamente.place(rely=0.7, relx=0.32)

        self.label_icone_upload = ttk.Label(
            self, 
            image=self.notebook.icone_whatsapp
        )
        self.label_icone_upload.image = self.notebook.icone_whatsapp
        self.label_icone_upload.place(rely=0.45, relx=0.415)
    def iniciar_conexao(self):
        if not self.running:
            self.notebook.atualizar_status("Conectando...", "orange")
            self.running = True
            self.driver = Driver(self)
            self.notebook.conexao = self  # Adiciona a conexão ao notebook
    def verificar_conexao_periodicamente(self):
        if self.running and self.driver:
            if self.driver.is_connected():
                self.notebook.atualizar_status("Conectado!", "green")
            else:
                self.notebook.atualizar_status("Conexão Perdida!", "red")
        self.after(30000, self.verificar_conexao_periodicamente)  # Verifica novamente após 30 segundos
    def tentar_novamente(self):
        if self.driver:
            if self.driver.is_connected():
                self.notebook.atualizar_status("Conectado!", "green")
            else:
                self.notebook.atualizar_status("Desconectado!", "red")
                self.driver.parar_conexao()
