import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import threading
from config import ToolTip

class Conexao(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.notebook = parent
        self.driver = None
        self.running = False
        self.criar_widgets_conexao()

    def criar_widgets_conexao(self):
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

        self.label_icone_upload = ttk.Label(
            self, 
            image=self.notebook.icone_whatsapp
        )
        self.label_icone_upload.image = self.notebook.icone_whatsapp
        self.label_icone_upload.place(rely=0.45, relx=0.415)

    def iniciar_conexao(self):
        if not self.running:
            self.running = True
            self.atualizar_status("Conectando...", "orange")
            threading.Thread(target=self.abrir_whatsapp, daemon=True).start()

    def abrir_whatsapp(self):
        try:
            self.atualizar_status('Aguardando QRCode...', 'orange')
            chrome_options = ChromeOptions()
            chrome_options.add_argument('--start-maximized')
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.get("https://web.whatsapp.com/")
            self.verificar_conexao()
        except Exception as e:
            self.atualizar_status(f"Erro: {str(e)}", "red")
            self.running = False
            if self.driver:
                self.driver.quit()

    def verificar_conexao(self):
        try:
            WebDriverWait(self.driver, 120).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]'))
            )
            self.atualizar_status("Conectado!", "green")
            self.monitorar_conexao()
        except Exception as e:
            self.atualizar_status("Conexão falhou!", "red")
            self.running = False
            if self.driver:
                self.driver.quit()

    def monitorar_conexao(self):
        if self.running:
            try:
                self.driver.title  # Acessa um atributo para verificar se o driver ainda está ativo
                self.after(3000, self.monitorar_conexao)  # Verifica novamente após 5 segundos
            except:
                self.atualizar_status("Desconectado!", "red")
                self.running = False

    def atualizar_status(self, texto, cor):
        self.label_conexao.config(text=f"Conexão: {texto}", foreground=cor)

    def __del__(self):
        self.running = False
        if self.driver:
            self.driver.quit()
