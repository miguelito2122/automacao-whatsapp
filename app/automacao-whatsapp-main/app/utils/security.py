from cryptography.fernet import Fernet
import os

def gerar_chave():
    return Fernet.generate_key()

def criptografar_credencial(api_key, chave):
    fernet = Fernet(chave)
    return fernet.encrypt(api_key.encode())

def descriptografar_credencial(api_key_criptografada, chave):
    fernet = Fernet(chave)
    return fernet.decrypt(api_key_criptografada).decode()