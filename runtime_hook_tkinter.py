"""
Runtime hook for tkinter to set TCL_LIBRARY environment variable.
This ensures tkinter can find its tcl/tk libraries on Windows.
"""

import os
import sys
from pathlib import Path

# Try to locate tcl library in the bundled application
if getattr(sys, 'frozen', False):
    # Running as a PyInstaller bundle
    bundle_dir = Path(sys._MEIPASS)
else:
    bundle_dir = Path(__file__).parent

# Common locations for tcl data in bundled apps
tcl_paths = [
    bundle_dir / "tcl",
    bundle_dir / "tcl8.6",
    bundle_dir / "_internal" / "tcl",
]

for tcl_path in tcl_paths:
    if tcl_path.exists():
        os.environ['TCL_LIBRARY'] = str(tcl_path / "tcl8.6")
        break

# Also set TK_LIBRARY for completeness
for tcl_path in tcl_paths:
    if tcl_path.exists():
        os.environ['TK_LIBRARY'] = str(tcl_path / "tk8.6")
        break
