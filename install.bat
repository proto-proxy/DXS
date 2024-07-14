@echo off

rem Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Installing Python...
    REM Download Python installer
    bitsadmin /transfer "PythonInstaller" https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe %TEMP%\python-3.12.4-amd64.exe

    REM Install Python
    start /wait %TEMP%\python-3.12.4-amd64.exe /quiet InstallAllUsers=1 PrependPath=1

    REM Check if installation was successful
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Failed to install Python. Exiting.
        exit /b 1
    )
    echo Python installation successful.
)

rem Install required Python packages
echo Installing required Python packages...
pip install customtkinter
pip install pywinstyles
pip install Pillow
pip install requests

echo All required packages installed successfully.
echo Done. Press Enter to exit.
pause >nul
