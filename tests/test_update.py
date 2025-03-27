"""Testes para o módulo update."""

import os
from app.update import check_version

def test_check_version():
    """Testa a fun o check_version."""
    repo_url = 'https://github.com/miguelito2122/automacao-whatsapp/archive/refs/heads/main.zip'
    app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    console = None
    branch = 'main'
    assert not check_version(repo_url, app_path, console, branch)
