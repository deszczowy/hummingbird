del /q dist\*.*
del hb.exe
pyinstaller --clean --onefile -w --icon=icon.ico hb.py
copy "dist\hb.exe" hb.exe
hb.exe