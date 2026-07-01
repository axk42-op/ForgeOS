@echo off
cd /d "%~dp0"
echo.
echo  Forge OS Launcher
echo  =================
echo.
if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo.
        echo ERROR: Python not found.
        echo Install Python 3.10+ from https://python.org
        echo.
        pause
        exit /b 1
    )
    echo Installing dependencies...
    .venv\Scripts\python.exe -m pip install -r requirements.txt
)
echo Starting Forge OS desktop...
echo.
.venv\Scripts\python.exe boot.py
echo.
pause
