@echo off
pip install pyinstaller
echo Installed pyinstaller
copy dxs.pyw dxs.py
pyinstaller --onefile dxs.py
echo Check your dist folder for the .exe
