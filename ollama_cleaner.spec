# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['ollama_mac_cleaner.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Ollama Cleaner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
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
    name='Ollama Cleaner',
)
app = BUNDLE(
    coll,
    name='Ollama Cleaner.app',
    icon=None,  # We'll set this in the next version if we create an icon
    bundle_identifier='com.ollamacleaner.app',
    info_plist={
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'NSHighResolutionCapable': 'True',
        'LSUIElement': '0',
        'NSHumanReadableCopyright': '© 2025',
        'CFBundleName': 'Ollama Cleaner',
        'CFBundleDisplayName': 'Ollama History Cleaner',
        'CFBundleGetInfoString': 'Easily clean your Ollama history on macOS'
    },
)
