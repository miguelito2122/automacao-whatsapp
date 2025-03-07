import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from checkin import AppCheckin
from conexao import Conexao
from checkout import AppCheckout
from PIL import ImageTk, Image

class Notebook(ttk.Notebook):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill='both', expand=True)
        self.carregar_imagens()
        self.abrir_abas(self)
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
        self.icone_whatsapp = ImageTk.PhotoImage(imagem_whats)

        # Carrega e redimensiona a imagem de upload (arquivo PNG)
        imagem_upload = Image.open('data/upload.png')
        imagem_upload = imagem_upload.resize((24, 24), Image.Resampling.LANCZOS)
        self.icone_upload = ImageTk.PhotoImage(imagem_upload)

        # Carrega e redimensiona a imagem de visualização (arquivo PNG)
        imagem_show = Image.open('data/show.png')
        imagem_show = imagem_show.resize((24, 24), Image.Resampling.LANCZOS)
        self.icone_show = ImageTk.PhotoImage(imagem_show)

        # Carrega e redimensiona a imagem de visualização (arquivo PNG)
        imagem_refresh = Image.open('data/refresh.png')
        imagem_refresh = imagem_refresh.resize((24, 24), Image.Resampling.LANCZOS)
        self.icone_refresh = ImageTk.PhotoImage(imagem_refresh)

        # Carrega e redimensiona a imagem de visualização (arquivo PNG)
        imagem_send = Image.open('data/send.png')
        imagem_send = imagem_send.resize((24, 24), Image.Resampling.LANCZOS)
        self.icone_send = ImageTk.PhotoImage(imagem_send)
    def abrir_arquivo(self):
        caminho = filedialog.askopenfilename(
            filetypes=[("Excel", "*.xlsx")]
        )

        if caminho:
            try:
                self.df = pd.read_excel(caminho)
                self.caminho_planilha = caminho
                messagebox.showinfo('Sucesso', 'Planilha carregada com sucesso!')
            except Exception as e:
                messagebox.showerror('Erro', f'Erro ao carregar planilha: {str(e)}')