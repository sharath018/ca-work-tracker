"""Logging setup for CA Work Tracker."""

import logging
import os
from ca_tracker.utils.path_utils import get_app_data_path


_logger = None


def setup_logging(log_level=logging.DEBUG):
    """Set up logging to both file and console."""
    global _logger
    
    log_dir = get_app_data_path()
    log_file = os.path.join(log_dir, "ca_work_tracker.log")
    
    _logger = logging.getLogger("CAWorkTracker")
    _logger.setLevel(log_level)
    
    # Remove any existing handlers to avoid duplicates
    _logger.handlers = []
    
    # File handler
    try:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        _logger.addHandler(file_handler)
    except Exception as e:
        print(f"Failed to set up file logging: {e}")
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    _logger.addHandler(console_handler)
    
    return _logger


def get_logger():
    """Get the configured logger."""
    global _logger
    if _logger is None:
        setup_logging()
    return _logger
