@echo off
pip install pyinstaller
echo Installed pyinstaller
copy dxs.pyw dxs.py
python -m PyInstaller dxs.py --onefile
echo Check your dist folder for the .exe
