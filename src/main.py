"""Entry point for CA Work Tracker application."""

import sys
import os
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
