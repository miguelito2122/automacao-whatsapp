import tkinter as tk
from tkinter import ttk
from config import ToolTip

class AppCheckout(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.carregar_imagens()
        self.criar_widgets_checkin()
        self.criar_tooltips()
    def carregar_imagens(self):
        self.icone_refresh, self.icone_show, self.icone_upload, self.icone_whatsapp, self.icone_send = self.parent.parent.carregar_imagens()
    def criar_widgets_checkin(self):
        # Botão para abrir arquivo
        self.botao_abrir_arquivo = ttk.Button(
            self, 
            text='Escolher Planilha'
        )
        self.botao_abrir_arquivo.place(relx=0.05, rely=0.05)

        # Botão de upload
        self.botao_carregar_mensagem = ttk.Button(
            self, 
            image=self.icone_upload
        )
        self.botao_carregar_mensagem.image = self.icone_upload
        self.botao_carregar_mensagem.place(relx=0.75, rely=0.05)

        # Botão de visualização
        self.botao_mostrar_mensagem = ttk.Button(
            self, 
            image=self.icone_show
        )
        self.botao_mostrar_mensagem.image = self.icone_show
        self.botao_mostrar_mensagem.place(relx=0.85, rely=0.05)

        # Botão de atualizar
        self.botao_atualizar_mensagens = ttk.Button(
            self, 
            image=self.icone_refresh
        )
        self.botao_atualizar_mensagens.image = self.icone_refresh
        self.botao_atualizar_mensagens.place(relx=0.65, rely=0.05)

        # Treeview
        self.treeview_checkin = ttk.Treeview(
            self, 
            columns=('col1', 'col2', 'col3', 'col4', 'col5', 'col6'), 
            show='headings'
        )
        
        colunas = [
            ('col1', 'Data', 20),
            ('col2', 'Nome', 20),
            ('col3', 'ID', 20),
            ('col4', 'Status', 20),
            ('col5', 'Valor', 20),
            ('col6', 'Observação', 20)
        ]

        for col, cab, larg in colunas:
            self.treeview_checkin.column(col, width=larg)
            self.treeview_checkin.heading(col, text=cab)
            
        self.treeview_checkin.place(relx=0.05, rely=0.15, relheight=0.75, relwidth=0.85)
    def criar_tooltips(self):
        ToolTip(self.botao_carregar_mensagem, 'Carregar Mensagem (.txt)')
        ToolTip(self.botao_abrir_arquivo, 'Planilhas (.xlsx)')
        ToolTip(self.botao_mostrar_mensagem, 'Pré-Visualizar Mensagem')