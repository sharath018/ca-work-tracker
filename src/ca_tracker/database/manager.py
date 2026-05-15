"""Database connection manager with error recovery."""

import sqlite3
import logging
import os
import shutil
from datetime import datetime
from pathlib import Path
from ca_tracker.config import DB_TIMEOUT, DB_CHECK_SAME_THREAD
from ca_tracker.database.schema import create_schema

logger = logging.getLogger("CAWorkTracker")


class DatabaseManager:
    """Manages database connections with error recovery and reconnection logic."""
    
    def __init__(self, db_path, backup_path):
        """
        Initialize the database manager.
        
        Args:
            db_path: Path to the SQLite database file
            backup_path: Path to the backups folder
        """
        self.db_path = db_path
        self.backup_path = backup_path
        self.conn = None
        self.cursor = None
        self._ensure_paths_exist()
        self.connect()
    
    def _ensure_paths_exist(self):
        """Ensure database and backup paths exist."""
        db_dir = os.path.dirname(self.db_path)
        os.makedirs(db_dir, exist_ok=True)
        os.makedirs(self.backup_path, exist_ok=True)
    
    def connect(self):
        """
        Connect to the database with error handling.
        Creates a new database if it doesn't exist.
        """
        try:
            self.conn = sqlite3.connect(
                self.db_path,
                timeout=DB_TIMEOUT,
                check_same_thread=DB_CHECK_SAME_THREAD
            )
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            
            # Enable foreign keys
            self.cursor.execute("PRAGMA foreign_keys = ON")
            
            # Create schema if new database
            if not self._table_exists("work_log"):
                logger.info("Creating new database schema")
                create_schema(self.cursor)
                self.conn.commit()
            
            logger.info(f"Successfully connected to database: {self.db_path}")
            return True
            
        except sqlite3.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            self.conn = None
            self.cursor = None
            return False
    
    def _table_exists(self, table_name):
        """Check if a table exists in the database."""
        try:
            if self.cursor is None:
                return False
            self.cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table_name,)
            )
            return self.cursor.fetchone() is not None
        except sqlite3.Error:
            return False
    
    def reconnect(self):
        """Reconnect to the database."""
        logger.warning("Attempting to reconnect to database...")
        if self.conn:
            try:
                self.conn.close()
            except Exception as e:
                logger.warning(f"Error closing previous connection: {e}")
        
        return self.connect()
    
    def execute(self, query, params=None):
        """
        Execute a query with automatic reconnection on failure.
        
        Args:
            query: SQL query to execute
            params: Query parameters (tuple or list)
        
        Returns:
            Cursor object or None if failed
        """
        try:
            if self.cursor is None:
                self.reconnect()
            
            if params:
                return self.cursor.execute(query, params)
            else:
                return self.cursor.execute(query)
                
        except sqlite3.DatabaseError as e:
            logger.error(f"Database error during query execution: {e}")
            if self.reconnect():
                # Retry once after reconnect
                try:
                    if params:
                        return self.cursor.execute(query, params)
                    else:
                        return self.cursor.execute(query)
                except sqlite3.Error as retry_error:
                    logger.error(f"Query failed after reconnect: {retry_error}")
                    return None
            return None
        except sqlite3.Error as e:
            logger.error(f"Error executing query: {e}")
            return None
    
    def fetchall(self):
        """Fetch all rows from the last query."""
        try:
            return self.cursor.fetchall() if self.cursor else []
        except sqlite3.Error as e:
            logger.error(f"Error fetching all rows: {e}")
            return []
    
    def fetchone(self):
        """Fetch one row from the last query."""
        try:
            return self.cursor.fetchone() if self.cursor else None
        except sqlite3.Error as e:
            logger.error(f"Error fetching one row: {e}")
            return None
    
    def commit(self):
        """Commit the current transaction."""
        try:
            if self.conn:
                self.conn.commit()
                return True
        except sqlite3.Error as e:
            logger.error(f"Error committing transaction: {e}")
            return False
        return False
    
    def rollback(self):
        """Rollback the current transaction."""
        try:
            if self.conn:
                self.conn.rollback()
                return True
        except sqlite3.Error as e:
            logger.error(f"Error rolling back transaction: {e}")
            return False
        return False
    
    def backup_database(self, max_backups=30):
        """
        Create a backup of the database.
        
        Args:
            max_backups: Maximum number of backup files to keep
        
        Returns:
            Path to the backup file or None if failed
        """
        try:
            if not os.path.exists(self.db_path):
                logger.warning("Database file does not exist, skipping backup")
                return None
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}.db"
            backup_file = os.path.join(self.backup_path, backup_name)
            
            # Create backup
            shutil.copy2(self.db_path, backup_file)
            logger.info(f"Database backed up to: {backup_file}")
            
            # Clean up old backups, keeping only the newest max_backups files
            self._cleanup_old_backups(max_backups)
            
            return backup_file
            
        except Exception as e:
            logger.error(f"Error backing up database: {e}")
            return None
    
    def _cleanup_old_backups(self, max_backups):
        """Remove old backup files, keeping only the most recent ones."""
        try:
            backup_files = sorted(
                Path(self.backup_path).glob("backup_*.db"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )
            
            # Remove files beyond max_backups
            for backup_file in backup_files[max_backups:]:
                backup_file.unlink()
                logger.info(f"Removed old backup: {backup_file}")
                
        except Exception as e:
            logger.warning(f"Error cleaning up old backups: {e}")
    
    def close(self):
        """Close the database connection."""
        try:
            if self.conn:
                self.conn.close()
                logger.info("Database connection closed")
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")
        finally:
            self.conn = None
            self.cursor = None
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
