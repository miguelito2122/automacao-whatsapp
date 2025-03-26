import os
import pytest
from app.update import check_version, show_update_window

def testar_check_version():
    show_update_window()