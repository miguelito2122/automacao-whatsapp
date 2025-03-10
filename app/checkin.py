import tkinter as tk
import pandas as pd
from tkinter import ttk, messagebox, filedialog
from config import ToolTip
from tkinter import StringVar

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
            command=self.abrir_arquivo
        )
        self.botao_abrir_arquivo.place(relx=0.01, rely=0.05, relheight=0.125)

        self.nome = ''
        # Combobox para selecionar o mês
        self.meses = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ]
        self.mes_selecionado = StringVar(value='Janeiro')
        self.combobox_meses = ttk.Combobox(
            self, 
            textvariable=self.mes_selecionado,
            values=self.meses,
            state='readonly'
        )
        self.combobox_meses.place(relx=0.315, rely=0.055, relwidth=0.27, relheight=0.115)
        self.combobox_meses.bind('<<ComboboxSelected>>', self.mudar_mes)

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
            image=self.notebook.icone_upload,
            command=self.carregar_mensagem
        )
        self.botao_carregar_mensagem.image = self.notebook.icone_upload
        self.botao_carregar_mensagem.place(relx=0.8, rely=0.05)

        # Botão de visualização
        self.botao_mostrar_mensagem = ttk.Button(
            self, 
            image=self.notebook.icone_show,
            command=self.mostrar_mensagem
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
            ('col4', 'Mensagem', 20),
            ('col5', 'Status', 20)
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
        # Verifica se a conexão está ativa
        if self.notebook.frame_conexao.running:
            driver = self.notebook.frame_conexao.driver.driver
            url = f"https://web.whatsapp.com/send?phone={num_valor}"
            driver.get(url)
        else:
            messagebox.showwarning("Erro", "Conexão com o WhatsApp não está ativa!")
    def abrir_arquivo(self):
        caminho = filedialog.askopenfilename(
            filetypes=[("Excel", "*.xlsx")]
        )
        if caminho:
            try:
                self.documento = pd.read_excel(caminho, sheet_name=None)
                self.caminho_planilha = caminho
                messagebox.showinfo('Sucesso', 'Planilha carregada com sucesso!')
                mes = self.mes_selecionado.get()[:3]  # Get only the first three characters
                if mes in self.documento:
                    self.atualizar_treeview(self.documento[mes])
            except Exception as e:
                messagebox.showerror('Erro', f'Erro ao carregar planilha: {str(e)}')

    def mudar_mes(self, event):
        if self.caminho_planilha:
            mes = self.mes_selecionado.get()[:3]  # Get only the first three characters
            if mes in self.documento:
                self.atualizar_treeview(self.documento[mes])
            else:
                messagebox.showerror('Erro', f'Sheet "{mes}" não encontrada na planilha!')
        else:
            messagebox.showwarning('Aviso', 'Por favor, selecione uma planilha primeiro!')

    def atualizar_treeview(self, documento):
        self.treeview_checkin.delete(*self.treeview_checkin.get_children())
        for index, row in documento.iterrows():
            if index >= 11:  # Start from row 12 (index 11)
                data = row.iloc[1]  # Column B
                nome = row.iloc[2]  # Column C
                id_ = row.iloc[3]  # Column D
                mensagem = row.iloc[5]  # Column F
                status = row.iloc[6]  # Column G
                if any([data, nome, id_, mensagem, status]):  # Check if at least one cell has a value
                    self.treeview_checkin.insert('', 'end', values=(data, nome, id_, mensagem, status))

    def carregar_mensagem(self):
        caminho = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt")]
        )
        if caminho:
            try:
                with open(caminho, 'r', encoding='utf-8') as file:
                    self.mensagem = file.read()
                    self.mensagem = self.mensagem.replace('${1}', 'name_var').replace('${2}', 'local_var')
                messagebox.showinfo('Sucesso', 'Mensagem carregada com sucesso!')
            except Exception as e:
                messagebox.showerror('Erro', f'Erro ao carregar mensagem: {str(e)}')

    def mostrar_mensagem(self):
        if hasattr(self, 'mensagem'):
            top = tk.Toplevel(self)
            top.title("Mensagem")
            text = tk.Text(top, wrap='word')
            text.insert('1.0', self.mensagem)
            text.config(state='disabled')
            text.pack(expand=1, fill='both')
        else:
            messagebox.showwarning('Aviso', 'Nenhuma mensagem carregada!')

