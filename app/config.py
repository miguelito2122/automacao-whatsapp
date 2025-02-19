import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

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
def abrir_abas(notebook):
    # Frames
    frame_conexao = ttk.Frame(notebook)
    frame_checkin = ttk.Frame(notebook)
    frame_checkout = ttk.Frame(notebook)

    # Abrindo Notebook
    notebook.add(frame_conexao, text='Conexão')
    notebook.add(frame_checkin, state='normal', text='Check-in')
    notebook.add(frame_checkout, state='normal', text='Check-out')

    # Widgets Conexão
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

    label_conexao = ttk.Label(frame_conexao, text='Conexão: Desconectado.', font=('Courier', 16, 'bold'))
    label_conexao.place(rely=0.1, relx=0.16)

    botao_conectar = ttk.Button(frame_conexao, text='Abrir Whatsapp')
    botao_conectar.place(rely=0.25, relx=0.345)

    label_icone_upload = ttk.Label(frame_conexao, image=icone_whatsapp)
    label_icone_upload.image = icone_whatsapp  # Mantém a referência para que a imagem não seja descartada
    label_icone_upload.place(rely=0.45, relx=0.415)

    # Widgets Check-In
    botao_abrir_arquivo = ttk.Button(frame_checkin, text='Escolher Planilha')
    botao_abrir_arquivo.place(relx=0.05, rely=0.05)

    botao_carregar_mensagem = ttk.Button(frame_checkin, image=icone_upload)
    botao_carregar_mensagem.image = icone_upload  # Mantém a referência
    botao_carregar_mensagem.place(relx=0.75, rely=0.05)

    botao_mostrar_mensagem = ttk.Button(frame_checkin, image=icone_show)
    botao_mostrar_mensagem.image = icone_show  # Mantém a referência
    botao_mostrar_mensagem.place(relx=0.85, rely=0.05)

    botao_atualizar_mensagens = ttk.Button(frame_checkin, image=icone_refresh)
    botao_atualizar_mensagens.image = icone_refresh
    botao_atualizar_mensagens.place(relx=0.65, rely=0.05)

    treeview_checkin = ttk.Treeview(frame_checkin, columns=('col1', 'col2', 'col3', 'col4', 'col5', 'col6'), show='headings')
    treeview_checkin.place(relx=0.05, rely=0.15, relheight=0.75, relwidth=0.85)

    # Configurando a largura das colunas
    treeview_checkin.column('col1', width=20)  # Largura de 100 pixels e centralizado
    treeview_checkin.column('col2', width=20)  # Largura de 150 pixels e alinhado à esquerda
    treeview_checkin.column('col3', width=20)
    treeview_checkin.column('col4', width=20)
    treeview_checkin.column('col5', width=20)
    treeview_checkin.column('col6', width=20)  # Alinhado à direita

    # Configurando os cabeçalhos das colunas
    treeview_checkin.heading('col1', text='Data')
    treeview_checkin.heading('col2', text='Nome')
    treeview_checkin.heading('col3', text='ID')
    treeview_checkin.heading('col4', text='Status')
    treeview_checkin.heading('col5', text='Valor')
    treeview_checkin.heading('col6', text='Observação')

    ToolTip(botao_carregar_mensagem, 'Carregar Mensagem (.txt)')
    ToolTip(botao_abrir_arquivo, 'Planilhas (.xlsx)')
    ToolTip(botao_mostrar_mensagem, 'Pré-Visualizar Mensagem')

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
