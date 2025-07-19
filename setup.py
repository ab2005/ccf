from setuptools import setup

APP = ['clipboard_saver.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': None,
    'plist': {
        'CFBundleName': 'Clipboard Saver',
        'CFBundleDisplayName': 'Clipboard Saver',
        'CFBundleIdentifier': 'com.local.clipboardsaver',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSUIElement': False,  # Set to True to hide from dock, False to show
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=['pyperclip'],
)