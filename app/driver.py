from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from tkinter import messagebox
import threading
import time
import urllib.parse
import random

class Driver():
    def __init__(self, parent):
        super().__init__()
        self.running = False
        self.parent = parent
        self.driver = None
        self.parent.notebook.conexao = self
        threading.Thread(target=self.abrir_whatsapp, daemon=True).start()
    def abrir_whatsapp(self):
        try:
            self.chrome_options = ChromeOptions()
            self.chrome_options.add_argument('--start-maximized')
            self.chrome_options.add_argument("--disable-gpu")  # Pode ser necessário em alguns ambientes Linux
            self.chrome_options.add_argument("--no-sandbox")  # Pode ser necessário em contêineres Docker ou ambientes restritos
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.driver.get("https://web.whatsapp.com/")
            self.parent.notebook.atualizar_status(f"Aguardando QR Code","orange")
            self.verificar_conexao()
        except Exception as e:
            self.parent.notebook.atualizar_status(f"Desconectado","red")
            messagebox.showerror('Erro', f'Erro ao abrir o Chrome: {str(e)}')
            self.parar_conexao()
    def verificar_conexao(self):
        try:
            WebDriverWait(self.driver, 120).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]'))
            )
            self.parent.notebook.atualizar_status("Conectado!", "green")
            self.iniciar_monitoramento()
        except Exception as e:
            self.parent.notebook.atualizar_status("Desconectado!", "red")
            messagebox.showerror('Erro', f'Tempo Expirado: {str(e)}')
            self.parar_conexao()
    def enviar_mensagem(self, numero, mensagem):
        try:
            print(f"Iniciando o envio de mensagem para {numero}")
            mensagem_url = urllib.parse.quote(mensagem)
            self.driver.get(f"https://web.whatsapp.com/send?phone={numero}&text={mensagem_url}&app_absent=0")
            print("Navegou para a URL de envio de mensagem")

            # Espera o campo de mensagem estar pronto
            input_box = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@contenteditable="true"][@role="textbox"]'))
            )
            print("Campo de mensagem pronto!")
            time.sleep(1)

            # Clica no botão de enviar
            send_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
            )
            send_button.click()
            print("Mensagem enviada!")
            
            time.sleep(random.uniform(1, 2.8))  # Tempo aleatório para evitar bloqueios
            return True
        except Exception as e:
            print(f"Erro ao enviar mensagem: {str(e)}")
            return False
    def iniciar_monitoramento(self):
        # Iniciar monitoramento em thread separada
        self.running = True
        threading.Thread(target=self.parent.verificar_conexao_periodicamente, daemon=True).start()
    def parar_conexao(self):
        if self.running:
            self.running = False
        if self.parent.running:
            self.parent.running = False
        if self.driver:
            self.driver.quit()
        self.parent.notebook.atualizar_status("Desconectado", "red")
        self.parent.notebook.conexao = None
    def is_connected(self):
        try:
            self.driver.find_element(By.XPATH, '//div[@contenteditable="true"]')
            return True
        except:
            return False
