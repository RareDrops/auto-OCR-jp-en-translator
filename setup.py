import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--onedir',
    '-w',
    '--add-data=Assets/mashiro.ico;Assets',
    '--add-data=chromedriver.exe;.',
    '--add-data=easyocr;easyocr',
    '--add-data=config.ini;.',
    '--icon=mashiro.ico'
])