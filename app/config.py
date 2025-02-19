import tkinter as tk
from tkinter import ttk
from checkin import AppCheckin
from conexao import Conexao
from checkout import AppCheckout

def abrir_abas(notebook):
    # Frames
    frame_conexao = Conexao(notebook)
    frame_checkin = AppCheckin(notebook)
    frame_checkout = AppCheckout(notebook)

    # Abrindo Notebook
    notebook.add(frame_conexao, text='Conexão')
    notebook.add(frame_checkin, state='normal', text='Check-in')
    notebook.add(frame_checkout, state='normal', text='Check-out')