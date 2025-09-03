#!/bin/bash

# Price List Converter Launcher Script
# This script activates the virtual environment and runs the application

echo "Starting Price List Converter..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo "Launching application..."
python main.py
