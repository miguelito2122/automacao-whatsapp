"""
Módulo responsável por criar a aba de Check-in.
"""
# Importações necessárias
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, StringVar
import pandas as pd
from config import ToolTip
from planilhas import JanelaEnvio

class AppCheckin(ttk.Frame):
    """ Classe para a aba de Check-in """
    def __init__(self, parent):
        super().__init__(parent)
        self.notebook = parent
        self.caminho_planilha = None
        self.carregar_widget()
        self.documento = None  # Initialize 'documento' attribute
        self.mes = None  # Initialize 'mes' attribute
        self.criar_tooltips()
        self.mensagem = None  # Initialize 'mensagem' attribute
        self.treeview_checkin.bind('<Double-1>', self.conversar)
        self.combobox_meses.bind('<<ComboboxSelected>>', self.mudar_mes)
        # Imagens
        self.botao_agente_ia.image = self.notebook.icone_agente # Icone Agente
        self.botao_carregar_mensagem.image = self.notebook.icone_upload # Icone Upload
        self.botao_mostrar_mensagem.image = self.notebook.icone_show # Icone Show
        self.botao_enviar_mensagem.image = self.notebook.icone_send # Icone Send
    def carregar_widget(self):
        """ Método para carregar os widgets da aba de Check-in """
        # Meses Usados no Combobox
        self.meses = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ]
        ## Widgets Principais
        # Botão para abrir arquivo
        self.botao_abrir_arquivo = ttk.Button(
            self,
            text='Escolher Planilha',
            command=self.abrir_arquivo
        )
        # Combobox para selecionar o mês
        self.mes_selecionado = StringVar(value='Janeiro') # Valor padrão
        self.combobox_meses = ttk.Combobox(
            self,
            textvariable=self.mes_selecionado,
            values=self.meses,
            state='readonly'
        )
        # Botão de Agente IA
        self.botao_agente_ia = ttk.Button(
            self,
            image=self.notebook.icone_agente,
            command=self.agente_ia
        )
        # Botão de upload
        self.botao_carregar_mensagem = ttk.Button(
            self,
            image=self.notebook.icone_upload,
            command=self.carregar_mensagem
        )
        # Botão de visualização
        self.botao_mostrar_mensagem = ttk.Button(
            self,
            image=self.notebook.icone_show,
            command=self.mostrar_mensagem
        )
        # Botão de Enviar
        self.botao_enviar_mensagem = ttk.Button(
            self,
            image=self.notebook.icone_send,
            command=self.abrir_lista
        )
        # Treeview com Scrollbar
        self.treeview_checkin = ttk.Treeview(
            self,
            columns=('col1', 'col2', 'col3', 'col4'),
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

        # Posicionamento dos Widgets
        self.botao_abrir_arquivo.place(relx=0.01,
                                       rely=0.05, relheight=0.125) # Botão de Abrir Arquivo
        self.combobox_meses.place(relx=0.315,
                                  rely=0.055, relwidth=0.27, relheight=0.115) # Combobox dos Meses
        self.botao_agente_ia.place(relx=0.7, rely=0.05) # Botão do Agente IA
        self.botao_carregar_mensagem.place(relx=0.8, rely=0.05) # Botão de Carregar Mensagem
        self.botao_mostrar_mensagem.place(relx=0.9, rely=0.05) # Botão de Mostrar Mensagem
        self.botao_enviar_mensagem.place(relx=0.6, rely=0.05) # Botão de Enviar Mensagem

        # Posicionamento do Treeview e Scrollbar
        self.treeview_checkin.place(relx=0.01, rely=0.2, relheight=0.775, relwidth=0.94)
        self.scrollbar.place(relx=0.95, rely=0.2, relheight=0.775, relwidth=0.04)

        # Configuração das colunas
        colunas = [
            ('col1', 'Data', 20),
            ('col2', 'Nome', 20),
            ('col3', 'ID', 20),
            ('col4', 'Status', 20)
        ]

        # Adiciona as colunas ao Treeview
        for col, cab, larg in colunas:
            self.treeview_checkin.column(col, width=larg)
            self.treeview_checkin.heading(col, text=cab)
    def criar_tooltips(self):
        """ Método para criar os tooltips dos botões """
        ToolTip(self.botao_abrir_arquivo, 'Abrir Planilha (.xlsx)')
        ToolTip(self.botao_carregar_mensagem, 'Carregar Mensagem (.txt)')
        ToolTip(self.botao_mostrar_mensagem, 'Pré-Visualizar Mensagem')
        ToolTip(self.botao_agente_ia, 'Agente IA')
        ToolTip(self.botao_enviar_mensagem, 'Enviar Mensagens')
    def conversar(self, event):
        """ Método para abrir o WhatsApp Web com o número selecionado """
        # Obtém o item clicado
        item = self.treeview_checkin.identify_row(event.y)
        if item:  # Verifica se clicou em uma linha válida
            valores = self.treeview_checkin.item(item, 'values')
            if len(valores) >= 3:  # Verifica se existe a terceira coluna
                numero = valores[2]  # Índice 2 para a terceira coluna
                if self.notebook.frame_conexao.running:
                    driver = self.notebook.frame_conexao.driver.driver
                    url = f"https://web.whatsapp.com/send?phone={numero}"
                    driver.get(url)
                else:
                    messagebox.showwarning("Erro", "Conexão com o WhatsApp não está ativa!")
            else:
                messagebox.showwarning("Erro", "A linha não possui a terceira coluna!")
    def abrir_arquivo(self):
        """ Método para abrir a planilha de check-in """
        # Carregar planilha
        caminho = filedialog.askopenfilename(
            filetypes=[("Excel", "*.xlsx")]
        )
        if caminho: # Verifica se o caminho não é vazio
            try:
                self.documento = pd.read_excel(caminho, sheet_name=None) # Lê todas as abas
                self.caminho_planilha = caminho
                self.mes = self.mes_selecionado.get()[:3]
                if self.mes in self.documento:
                    self.atualizar_treeview(self.documento[self.mes]) # Atualiza o Treeview
            except (FileNotFoundError, ValueError) as e:
                messagebox.showerror('Erro', f'Erro ao carregar planilha: {str(e)}')
    def mudar_mes(self, event):
        """ Método para mudar o mês selecionado no Combobox """
        if self.caminho_planilha:
            mes = self.mes_selecionado.get()[:3]  # Obtém o mês selecionado (3 primeiros caracteres)
            if mes in self.documento:
                self.atualizar_treeview(self.documento[mes]) # Atualiza o Treeview
            else:
                messagebox.showerror('Erro', f'Sheet "{mes}" não encontrada na planilha!')
        else:
            messagebox.showwarning('Aviso', 'Por favor, selecione uma planilha primeiro!')
    def atualizar_treeview(self, documento):
        """ Método para atualizar o Treeview com os dados da planilha """
        self.treeview_checkin.delete(*self.treeview_checkin.get_children()) # Limpa o Treeview
        for index, row in documento.iterrows():
            if index >= 11:  # Começa a partir da 12ª linha
                data = row.iloc[1]  # Coluna B
                nome = row.iloc[2]  # Coluna C
                id_ = row.iloc[3]  # Coluna D
                status = row.iloc[9]  # Coluna J
                if isinstance(data,
                   pd.Timestamp) or isinstance(data, datetime.datetime):
                    data_formatada = data.strftime('%d/%m/%y')
                else:
                    data_formatada = str(data)

                if any([data, nome, id_, status]):  # Checa se algum valor é diferente de vazio
                    self.treeview_checkin.insert(
                        '',
                        'end', 
                        values=(data_formatada, nome, id_, status)
                    )
    def carregar_mensagem(self):
        """ Método para carregar a mensagem de um arquivo .txt """
        # Carregar mensagem
        caminho = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt")]
        )
        if caminho:
            try:
                with open(caminho, 'r', encoding='utf-8') as file:
                    self.mensagem = file.read()
                messagebox.showinfo('Sucesso', 'Mensagem carregada com sucesso!')
            except (OSError, IOError) as e:
                messagebox.showerror('Erro', f'Erro ao carregar mensagem: {str(e)}')
    def mostrar_mensagem(self):
        """ Método para mostrar a mensagem carregada """
        if hasattr(self, 'mensagem'): # Verifica se a mensagem foi carregada
            top = tk.Toplevel(self)
            top.title("Mensagem")
            text = tk.Text(top, wrap='word')
            self.mensagem = self.editar_mensagem('{Nome}', '{Local}', '{Cliente}')
            text.insert('1.0', self.mensagem)
            text.config(state='disabled')
            text.pack(expand=1, fill='both')
        else:
            messagebox.showwarning('Aviso', 'Nenhuma mensagem carregada!')
    def abrir_lista(self):
        """ Método para abrir a janela de envio de mensagens """
        # Abre a janela de seleção de intervalo
        if hasattr(self, 'documento'):
            JanelaEnvio(self)
        else:
            messagebox.showwarning('Aviso', 'Carregue uma planilha primeiro!')
    def editar_mensagem(self, nome, local, cliente):
        """ Método para editar a mensagem com os valores da planilha """
        mensagem = self.mensagem
        mensagem = mensagem.replace('${1}', nome)
        mensagem = mensagem.replace('${2}', local)
        mensagem = mensagem.replace('${3}', cliente)
        return mensagem
    def agente_ia(self):
        """ Método para abrir a janela do Agente IA """
