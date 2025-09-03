#!/bin/bash
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
