"""Entry point for CA Work Tracker application."""

import sys
import os
from pathlib import Path

# Fix tkinter TCL_LIBRARY on Windows for PyInstaller bundles
if getattr(sys, 'frozen', False):
    # Running as a PyInstaller bundle
    bundle_dir = Path(sys._MEIPASS)
    tcl_lib_paths = [
        bundle_dir / "tcl" / "tcl8.6",
        bundle_dir / "tcl8.6",
        bundle_dir / "_internal" / "tcl" / "tcl8.6",
    ]
    for tcl_path in tcl_lib_paths:
        if tcl_path.exists():
            os.environ['TCL_LIBRARY'] = str(tcl_path)
            break

import tkinter as tk
import logging

# Add src to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from ca_tracker.utils import setup_logging, get_logger
from ca_tracker.ui import MainWindow

# Setup logging first
setup_logging()
logger = get_logger()

def main():
    """Main entry point for the application."""
    logger.info("Starting CA Work Tracker")
    
    root = tk.Tk()
    app = MainWindow(root)
    
    root.mainloop()

if __name__ == "__main__":
    import os
    main()
