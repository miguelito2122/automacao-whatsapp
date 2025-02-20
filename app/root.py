import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from checkin import AppCheckin
from conexao import Conexao
from checkout import AppCheckout

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Automação de Avaliações")
        self.geometry('400x300')
        self.resizable(False, False)
        self.centralizar_tela(self)
        # Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.parent = self
        self.notebook.pack(fill='both', expand=True)
        self.abrir_abas(self.notebook)
    def abrir_abas(self, notebook):
        # Frames
        self.frame_conexao = Conexao(notebook)
        self.frame_checkin = AppCheckin(notebook)
        self.frame_checkout = AppCheckout(notebook)
        # Abrindo Notebook
        notebook.add(self.frame_conexao, text='Conexão')
        notebook.add(self.frame_checkin, state='normal', text='Check-in')
        notebook.add(self.frame_checkout, state='normal', text='Check-out')
    def carregar_imagens(self):
        # Carrega e redimensiona a imagem do WhatsApp (arquivo GIF)
        imagem_whats = Image.open('data/whatsapp.gif')
        imagem_whats = imagem_whats.resize((48, 48), Image.Resampling.LANCZOS)
        icone_whatsapp = ImageTk.PhotoImage(imagem_whats)

        # Carrega e redimensiona a imagem de upload (arquivo PNG)
        imagem_upload = Image.open('data/upload.png')
        imagem_upload = imagem_upload.resize((24, 24), Image.Resampling.LANCZOS)
        icone_upload = ImageTk.PhotoImage(imagem_upload)

        # Carrega e redimensiona a imagem de visualização (arquivo PNG)
        imagem_show = Image.open('data/show.png')
        imagem_show = imagem_show.resize((24, 24), Image.Resampling.LANCZOS)
        icone_show = ImageTk.PhotoImage(imagem_show)

        # Carrega e redimensiona a imagem de visualização (arquivo PNG)
        imagem_refresh = Image.open('data/refresh.png')
        imagem_refresh = imagem_refresh.resize((24, 24), Image.Resampling.LANCZOS)
        icone_refresh = ImageTk.PhotoImage(imagem_refresh)

        # Carrega e redimensiona a imagem de visualização (arquivo PNG)
        imagem_send = Image.open('data/send.png')
        imagem_send = imagem_send.resize((24, 24), Image.Resampling.LANCZOS)
        icone_send = ImageTk.PhotoImage(imagem_send)

        return icone_refresh, icone_show, icone_upload, icone_whatsapp, icone_send
    def centralizar_tela(self, tela):
        tela.update_idletasks()

        # Calcula as coordenadas para centralização
        largura_janela = tela.winfo_width()
        altura_janela = tela.winfo_height()
        largura_tela = tela.winfo_screenwidth()
        altura_tela = tela.winfo_screenheight()

        x = (largura_tela // 2) - (largura_janela // 2)
        y = (altura_tela // 2) - (altura_janela // 2)

        # Aplica a nova posição sem alterar o tamanho
        return tela.geometry(f'+{x}+{y}')