"""
Módulo responsável por criar a aba de Checkout.
- Botão para escolher planilha
- Botão para carregar mensagem
- Botão para mostrar mensagem
- Botão para atualizar mensagens
- Treeview para exibir mensagens
"""
from tkinter import ttk
from config import ToolTip

class AppCheckout(ttk.Frame):
    def __init__(self, parent):
        """
        Initializes the AppCheckout frame.

        Args:
            parent: The parent widget for this frame.

        Sets up the initial state by creating the widgets for the checkout tab 
        and adding tooltips for the buttons.
        """

        super().__init__(parent)
        self.notebook = parent
        self.criar_widgets_checkin()
        self.criar_tooltips()
    def criar_widgets_checkin(self):
        # Botão para abrir arquivo
        """
        Creates the widgets for the checkout tab, including buttons and a Treeview.

        This method initializes and places the buttons for opening a file, uploading
        a message, viewing a message, and updating messages on the checkout tab.
        Additionally, it sets up a Treeview to display message data with columns
        for date, name, ID, status, value, and observation.
        """

        self.botao_abrir_arquivo = ttk.Button(
            self,
            text='Escolher Planilha'
        )
        self.botao_abrir_arquivo.place(relx=0.05, rely=0.05)

        # Botão de upload
        self.botao_carregar_mensagem = ttk.Button(
            self,
            image=self.notebook.icone_upload
        )
        self.botao_carregar_mensagem.image = self.notebook.icone_upload
        self.botao_carregar_mensagem.place(relx=0.75, rely=0.05)

        # Botão de visualização
        self.botao_mostrar_mensagem = ttk.Button(
            self,
            image=self.notebook.icone_show
        )
        self.botao_mostrar_mensagem.image = self.notebook.icone_show
        self.botao_mostrar_mensagem.place(relx=0.85, rely=0.05)

        # Botão de atualizar
        self.botao_atualizar_mensagens = ttk.Button(
            self,
            image=self.notebook.icone_refresh
        )
        self.botao_atualizar_mensagens.image = self.notebook.icone_refresh
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
        """
        Creates tooltips for the buttons on the checkout tab.

        This method creates tooltips for the buttons to open a file, upload a message,
        view a message, and update messages. The tooltips describe the action each
        button performs.
        """
        ToolTip(self.botao_carregar_mensagem, 'Carregar Mensagem (.txt)')
        ToolTip(self.botao_abrir_arquivo, 'Planilhas (.xlsx)')
        ToolTip(self.botao_mostrar_mensagem, 'Pré-Visualizar Mensagem')
