import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.id = None

        widget.bind("<Enter>", self.on_enter)
        widget.bind("<Leave>", self.on_leave)
        widget.bind("<Motion>", self.on_motion)

    def on_enter(self, event=None):
        self.schedule(event)

    def on_motion(self, event):
        # Atualiza a posição do tooltip conforme o mouse se move
        if self.tipwindow:
            x = event.x_root + 10
            y = event.y_root + 10
            self.tipwindow.wm_geometry(f"+{x}+{y}")

    def on_leave(self, event=None):
        self.unschedule()
        self.hide_tip()

    def schedule(self, event=None):
        # Pode-se definir um delay antes de mostrar o tooltip
        self.unschedule()
        self.id = self.widget.after(500, lambda: self.show_tip(event.x_root, event.y_root))

    def unschedule(self):
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def show_tip(self, x, y):
        # Cria uma janela Toplevel sem bordas que funciona como tooltip
        if self.tipwindow or not self.text:
            return
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # Remove a barra de título e bordas
        tw.wm_geometry(f"+{x + 10}+{y + 10}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
def carregar_imagens():
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
def centralizar_tela(tela):
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