"""Database package for CA Work Tracker."""

from .manager import DatabaseManager
from .schema import create_schema

__all__ = ['DatabaseManager', 'create_schema']
