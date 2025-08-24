# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

# ---------- GUI BUILD ----------
a_gui = Analysis(
    ['src\\imagetools_gui.py'],
    pathex=['.'],
    binaries=[],
    datas=[('src/ui/resources/appicon.ico', 'ui/resources')],
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
pyz_gui = PYZ(a_gui.pure, a_gui.zipped_data, cipher=block_cipher)
exe_gui = EXE(
    pyz_gui,
    a_gui.scripts,
    [],
    exclude_binaries=True,
    name='imagetools_gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src/ui/resources/appicon.ico',
)

# ---------- CLI BUILD -----------
a_cli = Analysis(
    ['src\\imagetools_cli.py'],
    pathex=['.'],
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
pyz_cli = PYZ(a_cli.pure, a_cli.zipped_data, cipher=block_cipher)
exe_cli = EXE(
    pyz_cli,
    a_cli.scripts,
    [],
    exclude_binaries=True,
    name='imagetools_cli',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src/ui/resources/appicon.ico',
)


coll = COLLECT(
    exe_gui,
    exe_cli,
    a_gui.binaries + a_cli.binaries,
    a_gui.zipfiles + a_cli.zipfiles,
    a_gui.datas + a_cli.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='imagetools',
)