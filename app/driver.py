from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tkinter import messagebox
import threading
import time

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
