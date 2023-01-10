# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['snakegame.py'],
    pathex=['C:\\Programming\\python files\\Pycharm\\venv\\Lib\\site-packages\\pygame'],
    binaries=[],
    datas=[('food.jpg', 'images'), ('game_over4.png','images'), ('game_over5.png','images'), ('simsun.ttc','images'),('whitebackground.png','images'), ('win.png','images'), ('restart3.png','images')
    ,('snakebodyHori.jpg', 'images'),('snakebodyVer.png', 'images'),('snakeheadDown.png', 'images'),('snakeheadLeft.png', 'images'),('snakeheadUp.jpg', 'images'),('snakeheadRight.png', 'images')
    ,('snaketurnLeftDown.png', 'images'),('snaketurnLeftUp.png', 'images'),('snaketurnRightDown.jpg', 'images'),('snaketurnRightUp.png', 'images'), ('sound.wav', 'sounds'),
    ('colors/blue.png', 'colors'),('colors/cyan.png', 'colors'),('colors/green.png', 'colors'),('colors/lime.png', 'colors'),('colors/pink.png', 'colors'), ('colors/purple.png', 'colors'),
    ('colors/red.png', 'colors'),('colors/white.png', 'colors'),('colors/yellow.png', 'colors'),],
    hiddenimports=['pygame'],
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
    name='snakegame',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='snakegame',
)
