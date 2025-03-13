import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import datetime
from tkinter import StringVar

class JanelaEnvio(tk.Toplevel):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.title("Selecionar Intervalo")
        self.geometry("350x450")
        self.main_app.notebook.parent.centralizar_tela(self)

        # Variáveis para datas
        self.data_inicio = StringVar()
        self.data_fim = StringVar()

        # Widgets de calendário
        self.frame_calendarios = ttk.Frame(self)
        self.frame_calendarios.pack(pady=10)
        
        self.cal_inicio = DateEntry(self.frame_calendarios, textvariable=self.data_inicio, date_pattern='dd/mm/yy')
        self.cal_inicio.pack(side="left", padx=5)
        
        self.cal_fim = DateEntry(self.frame_calendarios, textvariable=self.data_fim, date_pattern='dd/mm/yy')
        self.cal_fim.pack(side="left", padx=5)

        # Botão para carregar dados
        self.botao_carregar = ttk.Button(
            self, 
            image=self.main_app.notebook.icone_refresh,
            command=self.carregar_dados
        )
        self.botao_carregar.pack(pady=5)

        # Treeview secundário (lista de check-ins filtrados)
        self.treeview_secundario = ttk.Treeview(
            self, 
            columns=('col1', 'col2', 'col3', 'col4'), 
            show='headings'
        )
        
        # Configurar colunas (mesmo formato do treeview_checkin principal)
        colunas = [
            ('col1', 'Data', 50),
            ('col2', 'Nome', 50),
            ('col3', 'ID', 50),
            ('col4', 'Status', 50)
        ]
        
        for col, cab, larg in colunas:
            self.treeview_secundario.column(col, width=larg)
            self.treeview_secundario.heading(col, text=cab)
        
        self.treeview_secundario.place(relx=0.01, rely=0.2, relheight=0.7, relwidth=0.98)

    def carregar_dados(self):
        # Limpa o treeview secundário
        self.treeview_secundario.delete(*self.treeview_secundario.get_children())
        
        # Filtra os dados do treeview principal
        for item in self.main_app.treeview_checkin.get_children():
            valores = self.main_app.treeview_checkin.item(item, 'values')
            data_str = valores[0]  # Data está na primeira coluna
            
            try:
                data = datetime.datetime.strptime(data_str, "%d/%m/%y")
            except ValueError:
                continue  # Ignora dados inválidos
            
            # Verifica se está dentro do intervalo
            if (
                (datetime.datetime.strptime(self.data_inicio.get(), "%d/%m/%y") <= data) 
                and 
                (data <= datetime.datetime.strptime(self.data_fim.get(), "%d/%m/%y"))
            ):
                self.treeview_secundario.insert('', 'end', values=valores)