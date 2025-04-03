import os
import sys

from cryptography.fernet import Fernet
from config import ensure_directory, read_file_bytes, log

def gerar_chave(base_path, console, key_type):
    """Gera e salva uma nova chave de criptografia"""
    if base_path is None:
        log(console, "Caminho não válido")
        raise ValueError("Caminho inválido")
    
    folder = 'keys' if getattr(sys, 'frozen', False) else 'docs'
    chave_dir = os.path.join(base_path, folder)
    ensure_directory(chave_dir, console)

    chave_path = os.path.join(chave_dir, f'{key_type}.key')
    log(console, f"Chave salva em {chave_path}")

    chave = Fernet.generate_key()
    with open(chave_path, 'wb') as arquivo_chave:
        arquivo_chave.write(chave)
    print(f'Chave salva em {chave_dir}')

    return chave

def criptografar_credencial(api_key, chave):
    fernet = Fernet(chave)
    return fernet.encrypt(api_key.encode('utf-8'))

def descriptografar_credencial(api_key_criptografada, chave):
    fernet = Fernet(chave)
    return fernet.decrypt(api_key_criptografada).decode('utf-8')

def obter_chave(app_path: str, id: str, console=None) -> bytes:
    """
    Obtém a chave de criptografia para o identificador fornecido.
    Procura o arquivo {id}.key na pasta 'keys' (release) ou 'docs' (debug).
    Retorna a chave em bytes ou None se não encontrada.
    """
    folder = 'keys' if getattr(sys, 'frozen', False) else 'docs'
    chave_dir = os.path.join(app_path, folder)
    ensure_directory(chave_dir, console)
    chave_path = os.path.join(chave_dir, f'{id}.key')
    log(console, f"Caminho da chave: {chave_path}")

    if not os.path.exists(chave_path):
        log(console, f"Chave para '{id}' não encontrada.")
        return None

    chave = read_file_bytes(chave_path, console)
    if chave is not None:
        log(console, f"Chave atual para '{id}': {chave}\nGuarde-a em local seguro!")
    return chave

def obter_documento_crypto(app_path: str, id: str, console=None) -> bytes:
    """
    Obtém um documento criptografado (.crypto) a partir do caminho padrão.
    O arquivo é {id}.crypto na pasta 'keys' (release) ou 'docs' (debug).
    Se o arquivo não existir, retorna None.
    """
    folder = 'keys' if getattr(sys, 'frozen', False) else 'docs'
    doc_dir = os.path.join(app_path, folder)
    ensure_directory(doc_dir, console)
    doc_path = os.path.join(doc_dir, f'{id}.crypto')
    log(console, f"Caminho do documento criptografado: {doc_path}")

    if not os.path.exists(doc_path):
        log(console, f"Documento '{id}.crypto' não encontrado.")
        return None
    
    return doc_path