# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app.py', '.'),
        ('azure', 'azure'),
        ('azure.tcl', '.'),
        ('build.sh', '.'),
        ('EntityExtract Pro build script.txt', '.'),
        ('EntityExtract Pro packaging.py', '.'),
        ('gui.py', '.'),
        ('gui1.py', '.'),
        ('highlighted', 'highlighted'),
        ('light.tcl', '.'),
        ('logs', 'logs'),
        ('requirements.txt', '.'),
        ('results', 'results'),
        ('test', 'test'),
        ('text_analysis.py', '.'),
        ('utils.py', '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AI_Text_Analysis',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True if you want a console window
    disable_windowed_traceback=False,
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
    name='AI_Text_Analysis',
)
