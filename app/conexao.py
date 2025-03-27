"""
Este módulo contém a classe Conexao, que é uma subclasse da classe ttk.Frame.
Ela é responsável por criar a interface de conexão com o WhatsApp Web, permitindo
que o usuário abra o WhatsApp em um navegador e verifique se a conexão foi estabelecida
com sucesso. A classe Conexao contém métodos para iniciar a conexão, verificar a conexão
periodicamente e tentar novamente a conexão em caso de falha.
"""

from tkinter import ttk
from driver import Driver

class Conexao(ttk.Frame):
    def __init__(self, parent):
        """
        Inicializa o objeto Conexao com o pai parent.

        Abre as abas de Conex o, Check-in e Check-out.
        """
        super().__init__(parent)
        self.driver = None
        self.running = False
        self.notebook = parent
        self.criar_widgets_conexao()
    def criar_widgets_conexao(self):
        """
        Cria os widgets da conex o com o WhatsApp Web, incluindo
        o label de status da conex o, o bot o para abrir o WhatsApp,
        o bot o para tentar novamente a conex o e o label com o   cone do WhatsApp.
        """
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
        """
        Inicia a conex o com o WhatsApp Web.

        Se a conex o n o estiver em execu o, atualiza o status da conex o
        para "Conectando...", define a conex o como em execu o e instancia
        um novo objeto Driver que gerencia a conex o.

        :return: None
        """
        if not self.running:
            self.notebook.atualizar_status("Conectando...", "orange")
            self.running = True
            self.driver = Driver(self)
            self.notebook.conexao = self  # Adiciona a conexão ao notebook
    def verificar_conexao_periodicamente(self):
        """
        Verifica periodicamente se a conex o com o WhatsApp Web est  ativa.

        Se a conex o estiver em execu o e o driver estiver dispon vel,
        verifica se a conex o est  ativa e atualiza o status da conex o
        na janela principal. Se a conex o estiver perdida, atualiza
        o status da conex o para "Conex o Perdida!".

        Chama a si mesma a cada 30 segundos.
        """
        if self.running and self.driver:
            if self.driver.is_connected():
                self.notebook.atualizar_status("Conectado!", "green")
            else:
                self.notebook.atualizar_status("Conexão Perdida!", "red")
        self.after(30000, self.verificar_conexao_periodicamente)  # Verifica novamente após 30 segundos
    def tentar_novamente(self):
        """
        Tenta novamente a conex o com o WhatsApp Web.

        Se o driver estiver dispon vel e a conex o estiver perdida,
        atualiza o status da conex o para "Desconectado!" e para a conex o.
        Caso contr rio, atualiza o status da conex o para "Conectado!".

        :return: None
        """
        if self.driver:
            if self.driver.is_connected():
                self.notebook.atualizar_status("Conectado!", "green")
            else:
                self.notebook.atualizar_status("Desconectado!", "red")
                self.driver.parar_conexao()
