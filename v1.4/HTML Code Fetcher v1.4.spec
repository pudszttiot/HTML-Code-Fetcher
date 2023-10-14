# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:/Users/pudszTTIOT/Desktop/py/Python Creations/Completed/Projects/HTML Code Fetcher/Version 1.4/homepage.py', 'C:/Users/pudszTTIOT/Desktop/py/Python Creations/Completed/Projects/HTML Code Fetcher/Version 1.4/HTML Code Fetcher v1.4.py', 'C:/Users/pudszTTIOT/Desktop/py/Python Creations/Completed/Projects/HTML Code Fetcher/Version 1.4/main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='HTML Code Fetcher v1.4',
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
    icon=['C:\\Users\\pudszTTIOT\\Desktop\\py\\Python Creations\\Completed\\Projects\\HTML Code Fetcher\\Images\\htmlcodeftechericon.ico'],
)
