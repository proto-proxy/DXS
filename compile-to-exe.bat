@echo off
pip install pyinstaller
echo Installed pyinstaller!
copy dxs.pyw dxs.py
echo Created a copy of dxs.pyw -> renamed to dxs.py!
python -m PyInstaller dxs.py --onefile
echo Compiled dxs.py to a .exe!
echo Check your dist folder for the .exe!
pause
