@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Run boot.bat first to set up the environment.
    pause
    exit /b 1
)
.venv\Scripts\python.exe boot.py
