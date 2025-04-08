# -*- mode: python ; coding: utf-8 -*-

with open('updaterversion.txt', 'r') as f:
    version = f.read().strip()


a = Analysis(
    ['app/update.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['config', 'security'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Updater',
    version=version,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)


