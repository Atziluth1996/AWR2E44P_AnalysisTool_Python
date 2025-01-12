cd /d %~dp0
rmdir /s /q build
rmdir /s /q dist
pyinstaller --onefile --add-binary "EGE_Decompression_Lib\EGE_Decompression.dll;." MainFunction.py