# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['GameGUI.py'],
    pathex=[],
    binaries=[],
    datas=[('more_button.png', '.'), ('buy_button.png', '.'), ('sell_button.png', '.'), ('exit_button.png', '.'), ('SG Picture', 'SG Picture')],
    hiddenimports=['PIL', 'PIL.Image'],
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
    name='GameGUI',
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
