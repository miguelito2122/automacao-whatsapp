"""
Este módulo contém a classe JanelaEnvio, que é uma subclasse da classe tk.Toplevel.
Ela é responsável por criar uma janela secundária para selecionar um intervalo de datas
e enviar mensagens para os check-ins filtrados. A classe JanelaEnvio contém métodos para
carregar os dados do intervalo selecionado, enviar mensagens para os check-ins filtrados e
processar o envio das mensagens. A janela secundária exibe dois calendários para selecionar
a data de início e fim do intervalo, bem como botões para carregar os dados e enviar as mensagens.
"""

import tkinter as tk
from tkinter import ttk, StringVar, messagebox
import datetime
from tkcalendar import DateEntry

class JanelaEnvio(tk.Toplevel):
    def __init__(self, main_app):
        """
        Construtor da classe JanelaEnvio.

        Args:
            main_app (Checkin): Instância da classe Checkin que chama esta janela.

        Atributos:
            main_app (Checkin): Instância da classe Checkin que chama esta janela.
            data_inicio (StringVar): Variável para armazenar a data de início do intervalo.
            data_fim (StringVar): Variável para armazenar a data de fim do intervalo.
            frame_calendarios (ttk.Frame): Frame para os calendários.
            cal_inicio (DateEntry): Calendário para selecionar a data de início.
            cal_fim (DateEntry): Calendário para selecionar a data de fim.
            frame_botoes (ttk.Frame): Frame para os botões.
            botao_carregar (ttk.Button): Botão para carregar os dados do intervalo.
            botao_enviar (ttk.Button): Botão para enviar as mensagens.
            treeview_secundario (ttk.Treeview): Treeview secundário 
                para mostrar os check-ins filtrados.
        """
        super().__init__()
        self.main_app = main_app
        self.driver = None
        self.title("Selecionar Intervalo")
        self.geometry("350x450")
        self.main_app.notebook.parent.centralizar_tela(self)

        # Variáveis para datas
        self.data_inicio = StringVar()
        self.data_fim = StringVar()

        # Widgets de calendário
        self.frame_calendarios = ttk.Frame(self)
        self.frame_calendarios.pack(pady=10)

        self.cal_inicio = DateEntry(self.frame_calendarios, 
                                    textvariable=self.data_inicio, date_pattern='dd/mm/yy')
        self.cal_inicio.pack(side="left", padx=5)

        self.cal_fim = DateEntry(self.frame_calendarios, 
                                 textvariable=self.data_fim, date_pattern='dd/mm/yy')
        self.cal_fim.pack(side="left", padx=5)

        self.frame_botoes = ttk.Frame(self)
        self.frame_botoes.pack(pady=10)

        # Botão para carregar dados
        self.botao_carregar = ttk.Button(
            self.frame_botoes,
            image=self.main_app.notebook.icone_refresh,
            command=self.carregar_dados
        )

        self.botao_enviar = ttk.Button(
            self.frame_botoes,
            image=self.main_app.notebook.icone_send,
            command=self.enviar_mensagem
        )

        self.botao_enviar.pack(side='left', padx=5)
        self.botao_carregar.pack(side='left', padx=5)

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

        self.treeview_secundario.place(relx=0.01, rely=0.25, relheight=0.7, relwidth=0.98)

    def carregar_dados(self):
        # Limpa o treeview secundário
        """
        Limpa o treeview secundário e o repopula com os itens do treeview principal que
        estão dentro do intervalo de datas selecionado.
        """
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
    def enviar_mensagem(self):
        """
        Abre uma janela para coletar informações de nome e local de envio
        e, com base nelas, processa o envio de mensagens.

        :return: None
        """
        top = tk.Toplevel(self)
        top.title("Informações")
        top.geometry("300x100")
        self.main_app.notebook.parent.centralizar_tela(top)

        # Variáveis para armazenar os valores

        nome_var = tk.StringVar()
        local_var = tk.StringVar()

        # Widgets
        label_nome = tk.Label(top, text="Seu Nome:")
        label_nome.place(relx=0.01, rely=0.01)
        entry_nome = tk.Entry(top, textvariable=nome_var)
        entry_nome.place(relx=0.35, rely=0.01)

        label_local = tk.Label(top, text="Local de Envio:")
        label_local.place(relx=0.01, rely=0.35)
        entry_local = tk.Entry(top, textvariable=local_var)
        entry_local.place(relx=0.35, rely=0.35)

        def mandar():
            nome = nome_var.get()
            local = local_var.get()
            self.processar_envio(nome, local)
            top.destroy()

        botao_enviar = tk.Button(top, text="Enviar", command=mandar)
        botao_enviar.place(relx=0.5, rely=0.7, anchor='center')

        top.transient(self)
        top.grab_set()
        self.wait_window(top)

    def processar_envio(self, nome, local):
        """
        Processa o envio de mensagens com base nos dados do treeview.

        Abre uma janela para coletar informações de nome e local de envio
        e, com base nelas, processa o envio de mensagens com base nos dados
        do treeview.

        :param nome: nome da pessoa que está enviando a mensagem
        :param local: local de envio da mensagem
        :return: None
        """
        if hasattr(self.main_app, 'mensagem'): # Verifica se a mensagem foi carregada
            if self.main_app.notebook.frame_conexao.running: # Verifica se a conexão está ativa
                enviadas = 0
                erros = 0
                self.driver = self.main_app.notebook.frame_conexao.driver

                numeros_processados = set() # Armazena os números processados para evitar duplicatas
                numeros_enviados = set() # Armazena os números que foram enviados
                numeros_erros = set() # Armazena os números que deram erro
                for item in self.treeview_secundario.get_children():
                    valores = self.treeview_secundario.item(item, 'values')
                    if len(valores) >= 3:
                        numero = valores[2]  # Índice 2 para a terceira coluna

                        if numero in numeros_processados:
                            enviadas += 1
                            continue

                        cliente = valores[1]
                        mensagem = self.main_app.editar_mensagem(nome, local, cliente)

                        if self.driver.enviar_mensagem(numero, mensagem):
                            self.treeview_secundario.item(item, values=(*valores[:3], "Enviado"))
                            self.main_app.notebook.atualizar_planilha(self.main_app.caminho_planilha,
                                                                      self.main_app.mes, numero, 5, 'Sim')
                            enviadas += 1
                            numeros_enviados.add(numero)
                        else:
                            self.treeview_secundario.item(item, values=(*valores[:3], "Erro"))
                            self.main_app.notebook.atualizar_planilha(self.main_app.caminho_planilha,
                                                                      self.main_app.mes, numero, 5, 'Não')
                            erros += 1
                            numeros_erros.add(numero)

                        numeros_processados.add(numero)
                    else:
                        messagebox.showerror("Erro", "A linha não possui a terceira coluna!")
                messagebox.showinfo("Sucesso", "Mensagens enviadas com sucesso!")
                resumo = (f'Processados: {len(numeros_processados)}\n'
                          f'Enviados: {enviadas} ({", ".join(numeros_enviados)})\n'
                          f'Erros: {erros} ({", ".join(numeros_erros)})')
                messagebox.showinfo("Resumo", resumo)
            else:
                messagebox.showwarning("Erro", "Conexão com o WhatsApp não está ativa!")
        else:
            messagebox.showwarning("Aviso", "Nenhuma mensagem carregada!")
            