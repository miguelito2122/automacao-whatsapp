import tkinter as tk
from tkinter import ttk
from root import ToolTip, carregar_imagens

def abrir_abas(notebook):
    # Frames
    frame_conexao = ttk.Frame(notebook)
    frame_checkin = AppCheckin(notebook)
    frame_checkout = ttk.Frame(notebook)

    # Abrindo Notebook
    notebook.add(frame_conexao, text='Conexão')
    notebook.add(frame_checkin, state='normal', text='Check-in')
    notebook.add(frame_checkout, state='normal', text='Check-out')

class AppCheckin(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)  # Inicialização correta do Frame
        self.carregar_imagens()
        self.criar_frames()
        self.criar_widgets_conexao()
        self.criar_widgets_checkin()
        self.criar_tooltips()

    def carregar_imagens(self):
        # Supondo que carregar_imagens() retorne uma tupla com 4 ícones na ordem correta
        self.icone_refresh, self.icone_show, self.icone_upload, self.icone_whatsapp = carregar_imagens()

    def criar_frames(self):
        # Criar frames containers
        self.frame_conexao = ttk.Frame(self)
        self.frame_conexao.place(relwidth=1, relheight=0.3)  # Ajuste conforme necessidade
        
        self.frame_checkin = ttk.Frame(self)
        self.frame_checkin.place(rely=0.3, relwidth=1, relheight=0.7)

    def criar_widgets_conexao(self):
        # Widgets de Conexão
        self.label_conexao = ttk.Label(
            self.frame_conexao, 
            text='Conexão: Desconectado.', 
            font=('Courier', 16, 'bold')
        )
        self.label_conexao.place(rely=0.1, relx=0.16)

        self.botao_conectar = ttk.Button(
            self.frame_conexao, 
            text='Abrir Whatsapp'
        )
        self.botao_conectar.place(rely=0.25, relx=0.345)

        self.label_icone_upload = ttk.Label(
            self.frame_conexao, 
            image=self.icone_whatsapp
        )
        self.label_icone_upload.image = self.icone_whatsapp
        self.label_icone_upload.place(rely=0.45, relx=0.415)

    def criar_widgets_checkin(self):
        # Widgets de Check-In
        self.botao_abrir_arquivo = ttk.Button(
            self.frame_checkin, 
            text='Escolher Planilha'
        )
        self.botao_abrir_arquivo.place(relx=0.05, rely=0.05)

        # Botões com ícones
        botoes_icones = [
            (self.icone_upload, 0.75, 'Carregar Mensagem'),
            (self.icone_show, 0.85, 'Pré-Visualizar'),
            (self.icone_refresh, 0.65, 'Atualizar')
        ]

        for icone, posx, comando in botoes_icones:
            btn = ttk.Button(self.frame_checkin, image=icone)
            btn.image = icone  # Manter referência
            btn.place(relx=posx, rely=0.05)
            setattr(self, f'botao_{comando.lower().replace(" ", "_")}', btn)

        # Treeview
        colunas = ('col1', 'col2', 'col3', 'col4', 'col5', 'col6')
        cabecalhos = ['Data', 'Nome', 'ID', 'Status', 'Valor', 'Observação']
        larguras = [20] * 6  # Simplificado para mesma largura

        self.treeview_checkin = ttk.Treeview(
            self.frame_checkin, 
            columns=colunas, 
            show='headings'
        )
        
        for col, cab, larg in zip(colunas, cabecalhos, larguras):
            self.treeview_checkin.column(col, width=larg)
            self.treeview_checkin.heading(col, text=cab)
            
        self.treeview_checkin.place(relx=0.05, rely=0.15, relheight=0.75, relwidth=0.85)

    def criar_tooltips(self):
        # Adicionar tooltips
        ToolTip(self.botao_carregar_mensagem, 'Carregar Mensagem (.txt)')
        ToolTip(self.botao_abrir_arquivo, 'Planilhas (.xlsx)')
        ToolTip(self.botao_pré_visualizar, 'Pré-Visualizar Mensagem')