#!/usr/bin/env python3
"""
Script to create a distribution package for the Price List Converter app.
This creates a standalone executable that doesn't require Python installation.
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

def create_executable():
    """Create standalone executable"""
    print("Creating standalone executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Create single executable file
        "--windowed",  # Hide console window (GUI app)
        "--name=PriceListConverter",
        "--add-data=configs:configs",  # Include configs directory
        "--add-data=README.md:.",
        "--add-data=QUICKSTART.md:.",
        "main.py"
    ]
    
    subprocess.check_call(cmd)
    print("Executable created in 'dist' folder!")

def create_installer_script():
    """Create a simple installer script"""
    installer_content = '''#!/bin/bash
# Price List Converter Installer

echo "Installing Price List Converter..."

# Create application directory
APP_DIR="$HOME/PriceListConverter"
mkdir -p "$APP_DIR"

# Copy files
cp PriceListConverter "$APP_DIR/"
cp -r configs "$APP_DIR/"
cp README.md "$APP_DIR/"
cp QUICKSTART.md "$APP_DIR/"

# Make executable
chmod +x "$APP_DIR/PriceListConverter"

echo "Installation complete!"
echo "Run the app with: $APP_DIR/PriceListConverter"
'''
    
    with open("install.sh", "w") as f:
        f.write(installer_content)
    
    os.chmod("install.sh", 0o755)
    print("Created install.sh script")

if __name__ == "__main__":
    print("=== Price List Converter Distribution Setup ===")
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Create executable
    create_executable()
    
    # Create installer script
    create_installer_script()
    
    print("\n=== Distribution Package Ready ===")
    print("Files created:")
    print("- dist/PriceListConverter (executable)")
    print("- install.sh (installer script)")
    print("\nTo distribute:")
    print("1. Zip the 'dist' folder and 'install.sh'")
    print("2. Send to users")
    print("3. Users run: ./install.sh")
