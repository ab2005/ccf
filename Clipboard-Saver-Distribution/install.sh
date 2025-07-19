#!/bin/bash

echo "🔧 Clipboard Saver Installer"
echo "============================="

# Check requirements
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required. Install from python.org or: brew install python"
    exit 1
fi

if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "❌ Python tkinter required. Install with: brew install python-tk"
    exit 1
fi

# Create installation directory
INSTALL_DIR="$HOME/Applications/ClipboardSaver"
mkdir -p "$INSTALL_DIR"

# Copy files
cp clipboard_saver.py "$INSTALL_DIR/"
cp clipboard_saver "$INSTALL_DIR/"

# Create symlink in PATH
sudo ln -sf "$INSTALL_DIR/clipboard_saver" /usr/local/bin/clipboard-saver 2>/dev/null

echo "✅ Installation complete!"
echo "🚀 Run 'clipboard-saver' from Terminal or double-click '$INSTALL_DIR/clipboard_saver'"
