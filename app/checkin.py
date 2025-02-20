import tkinter as tk
from tkinter import ttk
from config import ToolTip

class AppCheckin(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.notebook = parent
        self.caminho_planilha = None
        self.carregar_widget()
        self.criar_tooltips()
        self.treeview_checkin.bind('<Double-1>', self.abrir_conversa)
    def carregar_widget(self):
        # Botão para abrir arquivo
        self.botao_abrir_arquivo = ttk.Button(
            self, 
            text='Escolher Planilha',
            command=self.notebook.abrir_arquivo
        )
        self.botao_abrir_arquivo.place(relx=0.01, rely=0.05, relheight=0.125)

        self.nome = ''
        # Entry para Nome à ser Inserido na Mensagem
        self.entry_nome = ttk.Entry(self, textvariable=self.nome)
        self.entry_nome.place(relx=0.315, rely=0.055, relwidth=0.27, relheight=0.115)

        # Botão de atualizar
        self.botao_atualizar_mensagens = ttk.Button(
            self, 
            image=self.notebook.icone_refresh
        )
        self.botao_atualizar_mensagens.image = self.notebook.icone_refresh
        self.botao_atualizar_mensagens.place(relx=0.7, rely=0.05)

        # Botão de upload
        self.botao_carregar_mensagem = ttk.Button(
            self, 
            image=self.notebook.icone_upload
        )
        self.botao_carregar_mensagem.image = self.notebook.icone_upload
        self.botao_carregar_mensagem.place(relx=0.8, rely=0.05)

        # Botão de visualização
        self.botao_mostrar_mensagem = ttk.Button(
            self, 
            image=self.notebook.icone_show
        )
        self.botao_mostrar_mensagem.image = self.notebook.icone_show
        self.botao_mostrar_mensagem.place(relx=0.9, rely=0.05)

        # Botão de Enviar
        self.botao_enviar_mensagem = ttk.Button(
            self, 
            image=self.notebook.icone_send
        )
        self.botao_enviar_mensagem.image = self.notebook.icone_send
        self.botao_enviar_mensagem.place(relx=0.6, rely=0.05)

        # Treeview com Scrollbar
        self.treeview_checkin = ttk.Treeview(
            self, 
            columns=('col1', 'col2', 'col3', 'col4', 'col5'), 
            show='headings'
        )

        # Scrollbar vertical
        self.scrollbar = ttk.Scrollbar(
            self,
            orient='vertical',
            command=self.treeview_checkin.yview
        )

        # Configurar a comunicação entre Treeview e Scrollbar
        self.treeview_checkin.configure(yscrollcommand=self.scrollbar.set)

        colunas = [
            ('col1', 'Data', 20),
            ('col2', 'Nome', 20),
            ('col3', 'ID', 20),
            ('col4', 'Status', 20),
            ('col5', 'Valor', 20)
        ]

        for col, cab, larg in colunas:
            self.treeview_checkin.column(col, width=larg)
            self.treeview_checkin.heading(col, text=cab)

        # Posicionamento do Treeview e Scrollbar
        self.treeview_checkin.place(relx=0.01, rely=0.2, relheight=0.775, relwidth=0.94)
        self.scrollbar.place(relx=0.95, rely=0.2, relheight=0.775, relwidth=0.04)
    def criar_tooltips(self):
        ToolTip(self.botao_carregar_mensagem, 'Carregar Mensagem (.txt)')
        ToolTip(self.botao_abrir_arquivo, 'Planilhas (.xlsx)')
        ToolTip(self.botao_mostrar_mensagem, 'Pré-Visualizar Mensagem')
        # Dados de exemplo
        self.treeview_checkin.insert('', 'end', values=('07-20', 'João Silva', '5551999142035', 'Ativo', 1500.00))
        self.treeview_checkin.insert('', 'end', values=('07-21', 'Miguel Souza', '002', 'Inativo', 2300.50))
    def abrir_conversa(self, event):
        # Obtém o item clicado
        item = self.treeview_checkin.identify_row(event.y)
        
        if item:  # Verifica se clicou em uma linha válida
            valores = self.treeview_checkin.item(item, 'values')
            
            if len(valores) >= 3:  # Verifica se existe a terceira coluna
                valor_coluna_3 = valores[2]  # Índice 2 para a terceira coluna
                self.processar_numero(valor_coluna_3)
            else:
                print("Erro: A linha não possui a terceira coluna!")
    def processar_numero(self, num_valor):
        # Sua lógica de processamento do Número aqui
        print(f"Número selecionado para processamento: {num_valor}")
        print("Executando operações específicas com o Número...")