# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for CA Work Tracker

Build command:
  pyinstaller ca_tracker.spec

To add an application icon:
  1. Create or obtain a .ico file (256x256 or larger)
  2. Place it in the assets/ folder (e.g., assets/app_icon.ico)
  3. Uncomment/update the icon= line in the EXE() section below
  4. Rebuild: pyinstaller ca_tracker.spec

For code signing:
  1. Obtain a code signing certificate (.pfx file)
  2. Sign the executable after building with signtool
  3. Example: signtool sign /f cert.pfx /p password /fd SHA256 dist/CA_Work_Tracker/main.exe
"""

import sys
from pathlib import Path
import tkinter as tk

block_cipher = None

# Get the directory where this spec file is located
spec_dir = Path.cwd()
src_dir = spec_dir / "src"

# Determine icon path (optional)
icon_path = str(spec_dir / "assets" / "app_icon.ico")
if not Path(icon_path).exists():
    icon_path = None  # No icon if file doesn't exist

# Get tkinter's tcl/tk data directory
try:
    tk_root = Path(tk.__file__).parent
    tcl_lib = tk_root / "tcl8.6"
    if tcl_lib.exists():
        tcl_data = (str(tcl_lib), "tcl")
    else:
        # Fallback for different Python/tcl versions
        tcl_data = None
except:
    tcl_data = None

datas = [
    (str(spec_dir / "version.txt"), "."),
]

# Add tcl/tk data if found
if tcl_data:
    datas.append(tcl_data)

assets_dir = spec_dir / "assets"
if assets_dir.exists():
    datas.append((str(assets_dir), "assets"))

a = Analysis(
    [str(src_dir / "main.py")],
    pathex=[str(src_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=[
        "tkinter",
        "tkinter.ttk",
        "reportlab",
        "reportlab.platypus",
        "reportlab.lib",
        "matplotlib",
        "packaging",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=["runtime_hook_tkinter.py"] if Path("runtime_hook_tkinter.py").exists() else [],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="main",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,  # Application icon for .exe
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="CA_Work_Tracker",
)
