# -*- mode: python ; coding: utf-8 -*-
# Build command
# pyinstaller server.spec

a = Analysis(
    ['control_app.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['pkg_resources', 'plyer', 'plyer.platforms','plyer.platforms.win','plyer.platforms.win.notification'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['info'],
    noarchive=True,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='limitedmediaserver_control',
	bundle_identifier='Limited Media Server Control',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
	icon='logo.ico',
	hide_console='hide-late',
)
