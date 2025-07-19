#!/bin/bash

echo "📦 Creating Clipboard Saver Distribution Package..."

# Create distribution directory
DIST_DIR="Clipboard-Saver-Distribution"
rm -rf "$DIST_DIR"
mkdir "$DIST_DIR"

# Copy the working Python script
cp simple_clipboard_saver.py "$DIST_DIR/clipboard_saver.py"

# Create launcher script
cat > "$DIST_DIR/clipboard_saver" << 'EOF'
#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "📥 Please install Python 3 from python.org or using Homebrew: brew install python"
    exit 1
fi

# Check if tkinter is available
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "❌ Python tkinter is required but not installed."
    echo "📥 Please install it using: brew install python-tk"
    exit 1
fi

# Run the clipboard saver
cd "$SCRIPT_DIR"
python3 clipboard_saver.py
EOF

chmod +x "$DIST_DIR/clipboard_saver"

# Create simple installer
cat > "$DIST_DIR/install.sh" << 'EOF'
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
EOF

chmod +x "$DIST_DIR/install.sh"

# Create README
cat > "$DIST_DIR/README.md" << 'EOF'
# Clipboard Saver

A simple macOS application to save clipboard content to files.

## Quick Start

1. Run `./install.sh` to install
2. Launch with `clipboard-saver` command or double-click the launcher

## Requirements

- Python 3: `brew install python`
- Tkinter: `brew install python-tk`

## Features

- Auto-generates filename from clipboard content
- Remembers last save location
- Customizable file extensions
- Simple GUI interface

## Manual Usage

```bash
python3 clipboard_saver.py
```
EOF

# Create ZIP archive
zip -r "Clipboard-Saver-v1.0.zip" "$DIST_DIR"

echo "✅ Distribution package created: Clipboard-Saver-v1.0.zip"
echo "📁 Contents available in: $DIST_DIR/"