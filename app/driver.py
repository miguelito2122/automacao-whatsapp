from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import threading


class Driver():
    def __init__(self, parent):
        super().__init__()
        self.running = False
        self.parent = parent
        self.driver = None
        print(self.parent)
        threading.Thread(target=self.abrir_whatsapp, daemon=True).start()

    def abrir_whatsapp(self):
        try:
            self.chrome_options = ChromeOptions()
            self.chrome_options.add_argument('--start-maximized')
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.driver.get("https://web.whatsapp.com/")
            self.parent.atualizar_status("Aguardando QR Code...", "orange")
            self.verificar_conexao()
        except Exception as e:
            self.parent.atualizar_status(f"Erro: {str(e)}", "red")
            self.parent.running = False
            self.running = False
            if self.parent.driver:
                self.driver.quit()

    def verificar_conexao(self):
        try:
            WebDriverWait(self.driver, 120).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]'))
            )
            self.parent.atualizar_status("Conectado!", "green")
            self.iniciar_monitoramento()
        except Exception as e:
            self.parent.atualizar_status("Conexão falhou!", "red")
            self.parent.running = False
            self.running = False
            if self.parent.driver:
                self.driver.quit()

    def monitorar_conexao(self):
        if self.running:
            try:
                # Verifica se a barra de pesquisa está presente
                self.driver.find_element(By.XPATH, '//div[@contenteditable="true"]')
                self.parent.after(3000, self.monitorar_conexao)  # Verifica novamente após 3 segundos
            except:
                try:
                    # Verifica se o QR code ainda está presente
                    self.driver.find_element(By.XPATH, '//canvas[@aria-label="Scan me!"]')
                    self.parent.after(3000, self.monitorar_conexao)  # Verifica novamente após 3 segundos
                except:
                    self.parent.atualizar_status("Desconectado!", "red")
                    self.parent.running = False
                    self.running = False

    def __del__(self):
        self.running = False
        self.parent.running = False
        if self.driver:
            self.driver.quit()

    def iniciar_monitoramento(self):
        # Iniciar monitoramento em thread separada
        self.running = True
        thread = threading.Thread(target=self.monitorar_conexao)
        thread.start()