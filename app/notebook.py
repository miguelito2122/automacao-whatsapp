from tkinter import ttk
from openpyxl import load_workbook
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
        # Carrega e redimensiona a imagem de conexão (arquivo PNG)
        imagem_agente = Image.open('data/agent.png')
        imagem_agente = imagem_agente.resize((24, 24), Image.Resampling.LANCZOS)
        self.icone_agente = ImageTk.PhotoImage(imagem_agente)

        # Carrega e redimensiona a imagem de upload (arquivo PNG)
        imagem_calendario = Image.open('data/calendar.png')
        imagem_calendario = imagem_calendario.resize((12, 12), Image.Resampling.LANCZOS)
        self.icone_calendario = ImageTk.PhotoImage(imagem_calendario)

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
    def atualizar_status(self, texto, cor):
        self.frame_conexao.label_conexao.config(text=f"Conexão: {texto}", foreground=cor)
        if texto == "Conectado!":
            for tab_id in range(1, self.index("end")):
                self.tab(tab_id, state="normal")
        else:
            for tab_id in range(1, self.index("end")):
                self.tab(tab_id, state="disabled")
            self.select(0)
    def atualizar_planilha(self, caminho, mes, telefone, status):
        try:
            wb = load_workbook(caminho)

            if mes not in wb.sheetnames:
                print(f"Sheet {mes} não encontrada na planilha.")
                return False

            ws = wb[mes]

            for row in ws.iter_rows(min_row=12, max_row=ws.max_row, min_col=2, max_col=ws.max_column):
                valor_telefone = str(row[2].value)
                if telefone in valor_telefone:
                    row[8].value = status
                    print(f"Status atualizado para {telefone} na planilha.")

            wb.save(caminho)                
            return True
        except Exception as e:
            print(f"Erro ao atualizar status na planilha: {str(e)}")
            return False
        