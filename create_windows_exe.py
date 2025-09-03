#!/usr/bin/env python3
"""
Script to create a Windows executable for the Price List Converter app.
Note: This needs to be run on a Windows machine or in a Windows environment.
"""

import subprocess
import sys
import os
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("PyInstaller already installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def create_windows_executable():
    """Create Windows executable"""
    print("Creating Windows executable...")
    
    # PyInstaller command for Windows
    cmd = [
        "pyinstaller",
        "--onefile",  # Create single executable file
        "--windowed",  # Hide console window (GUI app)
        "--name=PriceListConverter",
        "--add-data=configs;configs",  # Include configs directory (Windows uses ;)
        "--add-data=README.md;.",
        "--add-data=QUICKSTART.md;.",
        "main.py"
    ]
    
    subprocess.check_call(cmd)
    print("Windows executable created in 'dist' folder!")

def create_windows_installer():
    """Create a Windows installer script"""
    installer_content = '''@echo off
REM Price List Converter Windows Installer

echo Installing Price List Converter...

REM Create application directory
set APP_DIR=%USERPROFILE%\\PriceListConverter
if not exist "%APP_DIR%" mkdir "%APP_DIR%"

REM Copy files
copy PriceListConverter.exe "%APP_DIR%\\"
xcopy configs "%APP_DIR%\\configs\\" /E /I
copy README.md "%APP_DIR%\\"
copy QUICKSTART.md "%APP_DIR%\\"

echo Installation complete!
echo Run the app with: "%APP_DIR%\\PriceListConverter.exe"
pause
'''
    
    with open("install_windows.bat", "w") as f:
        f.write(installer_content)
    
    print("Created install_windows.bat script")

if __name__ == "__main__":
    print("=== Price List Converter Windows Distribution Setup ===")
    print("NOTE: This script must be run on a Windows machine!")
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Create executable
    create_windows_executable()
    
    # Create installer script
    create_windows_installer()
    
    print("\n=== Windows Distribution Package Ready ===")
    print("Files created:")
    print("- dist/PriceListConverter.exe (Windows executable)")
    print("- install_windows.bat (Windows installer script)")
    print("\nTo distribute:")
    print("1. Zip the 'dist' folder and 'install_windows.bat'")
    print("2. Send to Windows users")
    print("3. Users run: install_windows.bat")
