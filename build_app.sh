#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Build the macOS app
python setup.py py2app

# Make the script executable
chmod +x dist/Clipboard\ Saver.app/Contents/MacOS/Clipboard\ Saver

echo "App built successfully! You can find it in the 'dist' folder."
echo "To add to Applications folder, run:"
echo "cp -r 'dist/Clipboard Saver.app' /Applications/"