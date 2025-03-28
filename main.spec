# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app/main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        # ✅ Inclui todos os arquivos .png da pasta data
        ('data/*.png', 'data'),  # Alteração aqui
        
        # Arquivos Python e estrutura do app
        ('app/*.py', 'app'),
        ('app/utils/*.py', 'app/utils'),
        
        # Versionamento
        ('version.txt', '.'),
        
        # Adicione esta linha se precisar da pasta docs:
        # ('docs/*', 'docs')
    ],
    hiddenimports=[
        'PIL._tkinter_finder'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    exclude_binaries=True,
    name='automacao-whatsapp',
    debug=False,  # ✅ Altere para False para build de produção
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Altere para False se for uma aplicação GUI
    icon='data/whatsapp.ico',  # ✅ Use arquivo .ico (converta seu GIF para ICO)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='automacao-whatsapp'
)