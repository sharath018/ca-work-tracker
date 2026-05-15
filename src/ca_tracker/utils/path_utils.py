"""Path utilities for PyInstaller compatibility."""

import os
import sys
from ca_tracker.config import DB_FILENAME, BACKUP_FOLDER


def get_app_data_path():
    """
    Get the application data path.
    For PyInstaller bundled apps, this is next to the .exe.
    For development, this is the project root.
    """
    if hasattr(sys, '_MEIPASS'):
        # Running as compiled PyInstaller executable
        return os.path.dirname(sys.executable)
    else:
        # Running as script - go up from src/ca_tracker to project root
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Navigate up: utils -> ca_tracker -> src -> root
        return os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))


def get_resource_path(relative_path):
    """Get the absolute path to a resource file."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(get_app_data_path(), relative_path)


def get_db_path():
    """Get the full path to the database file."""
    return os.path.join(get_app_data_path(), DB_FILENAME)


def get_backup_path():
    """Get the full path to the backups folder."""
    backup_path = os.path.join(get_app_data_path(), BACKUP_FOLDER)
    os.makedirs(backup_path, exist_ok=True)
    return backup_path


def ensure_app_data_path_exists():
    """Ensure the app data path exists."""
    path = get_app_data_path()
    os.makedirs(path, exist_ok=True)
    return path
