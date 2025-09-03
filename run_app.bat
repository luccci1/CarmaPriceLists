@echo off
REM Price List Converter Launcher Script for Windows
REM This script activates the virtual environment and runs the application

echo Starting Price List Converter...

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Installing dependencies...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

echo Launching application...
python main.py

pause
