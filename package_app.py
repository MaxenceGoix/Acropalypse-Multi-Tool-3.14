"""Build a standalone desktop executable with PyInstaller.

Run after installing requirements and, if desired, the native GIF extension:
    python -m pip install pyinstaller
    python package_app.py
"""
import PyInstaller.__main__

PyInstaller.__main__.run([
    "gui.py",
    "--name=Acropalypse-Multi-Tool",
    "--onefile",
    "--windowed",
    "--clean",
    "--collect-submodules=gif_lib",
])
