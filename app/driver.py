"""
    Módulo responsável por gerenciar a conexão com o WhatsApp Web.
    - Abre o navegador Chrome
    - Navega até o WhatsApp Web
    - Aguarda o usuário escanear o QR Code
    - Verifica se a conexão está ativa
    - Envia mensagens
    - Monitora a conexão
    - Encerra a conexão
"""

from tkinter import messagebox
import threading
import time
import urllib.parse
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException


class Driver():
    """ Classe responsável por gerenciar a conexão com o WhatsApp Web """
    def __init__(self, parent):
        super().__init__()
        self.running = False
        self.parent = parent
        self.driver = None
        self.parent.notebook.conexao = self
        self.chrome_options = None
        threading.Thread(target=self.abrir_whatsapp, daemon=True).start()
    def abrir_whatsapp(self):
        """ Abre o navegador Chrome e navega até o WhatsApp Web """
        try:
            self.chrome_options = ChromeOptions()
            self.chrome_options.add_argument('--start-maximized')
            self.chrome_options.add_argument("--disable-gpu")
            self.chrome_options.add_argument("--no-sandbox")
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.driver.get("https://web.whatsapp.com/")
            self.parent.notebook.atualizar_status("Aguardando QR Code","orange")
            self.verificar_conexao()
        except (ConnectionError, TimeoutError) as e:
            self.parent.notebook.atualizar_status("Desconectado","red")
            messagebox.showerror('Erro', f'Erro ao abrir o Chrome: {str(e)}')
            self.parar_conexao()
    def verificar_conexao(self):
        """
        Verifica se a conexão com o WhatsApp Web está ativa.

        Espera 2 minutos para que o elemento de edição de mensagem esteja presente na página,
        indicando que a conexão está ativa. Caso contrário, lança um erro.

        Se a conexão estiver ativa, atualiza o status da conexão e inicia o monitoramento.

        Se o tempo expirar, lança um erro e para a conexão.
        """
        try:
            WebDriverWait(self.driver, 120).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]'))
            )
            self.parent.notebook.atualizar_status("Conectado!", "green")
            self.iniciar_monitoramento()
        except (TimeoutError, ConnectionError, WebDriverException) as e:
            self.parent.notebook.atualizar_status("Desconectado!", "red")
            messagebox.showerror('Erro', f'Tempo Expirado: {str(e)}')
            self.parar_conexao()
    def enviar_mensagem(self, numero, mensagem):
        """
        Envia uma mensagem para um número de WhatsApp especificado utilizando o WhatsApp Web.

        Navega para a URL do WhatsApp Web com o número de telefone e a mensagem especificados,
        espera o campo de entrada de mensagem estar pronto e, em seguida, envia a mensagem.

        Args:
            numero (str): O número de telefone para o qual a mensagem será enviada, 
                no formato internacional.
            mensagem (str): O conteúdo da mensagem a ser enviada.

        Retorna:
            bool: True se a mensagem foi enviada com sucesso, False se houver um erro.

        Lança:
            Exception: Se houver um erro durante o processo de envio da mensagem.
        """

        try:
            print(f"Iniciando o envio de mensagem para {numero}")
            mensagem_url = urllib.parse.quote(mensagem)
            url = f'https://web.whatsapp.com/send?phone={numero}&text={mensagem_url}&app_absent=0'
            self.driver.get(url)
            print("Navegou para a URL de envio de mensagem")

            # Espera o campo de mensagem estar pronto
            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH,
                                            '//div[@contenteditable="true"][@role="textbox"]'))
            )
            time.sleep(1)

            # Clica no botão de enviar
            send_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
            )
            send_button.click()
            time.sleep(random.uniform(1, 2.8))  # Tempo aleatório para evitar bloqueios
            return True
        except (TimeoutError, ConnectionError, WebDriverException) as e:
            print(f"Erro ao enviar mensagem: {str(e)}")
            return False
    def iniciar_monitoramento(self):
        """
        Inicia o monitoramento de conex o em uma thread separada.

        Chama o método verificar_conexao_periodicamente em uma thread separada,
        que verifica periodicamente se a conex o est  ativa e atualiza o status
        da conex o na janela principal.

        Returns:
            None
        """
        self.running = True
        threading.Thread(target=self.parent.verificar_conexao_periodicamente, daemon=True).start()
    def parar_conexao(self):
        """
        Para a conex o com o WhatsApp Web.

        Fecha a conexão atual, seta o status da conexão como "Desconectado"
        na janela principal e redefine a conexão na janela principal.

        Returns:
            None
        """
        if self.running:
            self.running = False
        if self.parent.running:
            self.parent.running = False
        if self.driver:
            self.driver.quit()
        self.parent.notebook.atualizar_status("Desconectado", "red")
        self.parent.notebook.conexao = None
    def is_connected(self):
        """
        Verifica se a conex o com o WhatsApp Web est  ativa.

        Retorna:
            bool: True se a conex o estiver ativa, False caso contr rio.
        """
        try:
            self.driver.find_element(By.XPATH, '//div[@contenteditable="true"]')
            return True
        except (NoSuchElementException, WebDriverException):
            return False
