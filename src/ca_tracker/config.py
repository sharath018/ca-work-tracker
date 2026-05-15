"""Configuration and constants for CA Work Tracker."""

import os
import sys

# Application metadata
APP_NAME = "CA Work Tracker"
APP_VERSION = "1.0.0"

# Window configuration
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 700

# Database configuration
DB_FILENAME = "ca_work_tracker.db"
BACKUP_FOLDER = "backups"

# Work categories
CATEGORIES = [
    "GST Notice",
    "Income Tax Notice",
    "Agreement Drafting",
    "Contract Review",
    "ROC Work",
    "Bank Documentation",
    "Advisory",
    "Payroll Support",
    "Audit Support",
    "Other"
]

# Work status options
STATUS_OPTIONS = [
    "Pending",
    "In Progress",
    "Completed",
    "Billed",
    "Closed"
]

# Billable options
BILLABLE_OPTIONS = ["Yes", "No"]

# Date format
DATE_FORMAT = "%d-%b-%Y"

# Target platforms
SUPPORTED_PLATFORMS = ["Windows 10", "Windows 11"]

# Database connection configuration
DB_TIMEOUT = 10  # seconds
DB_CHECK_SAME_THREAD = False

# Backup configuration
BACKUP_MAX_FILES = 30  # Keep max 30 daily backups


def get_db_path():
    """Get the path to the database file."""
    return os.path.join(get_app_data_path(), DB_FILENAME)


def get_backup_path():
    """Get the path to the backups folder."""
    return os.path.join(get_app_data_path(), BACKUP_FOLDER)


def get_app_data_path():
    """
    Get the application data path.
    For PyInstaller bundled apps, this is next to the .exe.
    For development, this is the current directory.
    """
    if hasattr(sys, '_MEIPASS'):
        # Running as compiled PyInstaller executable
        return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.path.abspath(".")


def get_resource_path(relative_path):
    """
    Get the absolute path to a resource.
    Handles PyInstaller bundling correctly.
    """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller sets _MEIPASS to the bundle directory
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
