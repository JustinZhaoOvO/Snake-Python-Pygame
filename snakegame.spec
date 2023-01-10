# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['snakegame.py'],
    pathex=['C:\\Programming\\python files\\Pycharm\\venv\\Lib\\site-packages\\pygame'],
    binaries=[],
    datas=[('images/food.jpg', 'images'), ('images/game_over4.png','images'), ('images/game_over5.png','images'), ('font/simsun.ttc','font'),('images/whitebackground.png','images'), ('images/win.png','images'), ('images/restart3.png','images')
    ,('images/snakebodyHori.jpg', 'images'),('images/snakebodyVer.png', 'images'),('images/snakeheadDown.png', 'images'),('images/snakeheadLeft.png', 'images'),('images/snakeheadUp.jpg', 'images'),('images/snakeheadRight.png', 'images')
    ,('images/snaketurnLeftDown.png', 'images'),('images/snaketurnLeftUp.png', 'images'),('images/snaketurnRightDown.jpg', 'images'),('images/snaketurnRightUp.png', 'images'), ('sounds/sound.wav', 'sounds'),
    ('colors/blue.png', 'colors'),('colors/cyan.png', 'colors'),('colors/green.png', 'colors'),('colors/lime.png', 'colors'),('colors/pink.png', 'colors'), ('colors/purple.png', 'colors'),
    ('colors/red.png', 'colors'),('colors/white.png', 'colors'),('colors/yellow.png', 'colors'),('settings.txt','.')],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='snakegame',
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
    icon=['icon.ico'],
)
