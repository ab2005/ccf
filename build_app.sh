#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Build the macOS app
python setup.py py2app

# Make the script executable (if the app was built successfully)
if [ -f "dist/Clipboard Saver.app/Contents/MacOS/Clipboard Saver" ]; then
    chmod +x "dist/Clipboard Saver.app/Contents/MacOS/Clipboard Saver"
    echo "App built successfully! You can find it in the 'dist' folder."
    echo "To add to Applications folder, run:"
    echo "cp -r 'dist/Clipboard Saver.app' /Applications/"
else
    echo "Build failed - app executable not found"
fi