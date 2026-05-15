"""Version information for CA Work Tracker."""

__version__ = "1.0.0"
__author__ = "CA Firm"
__release_date__ = "2025-01-15"
__app_name__ = "CA Work Tracker"

def get_version():
    """Return the current application version."""
    return __version__

def get_full_version():
    """Return full version info."""
    return f"{__app_name__} v{__version__}"
