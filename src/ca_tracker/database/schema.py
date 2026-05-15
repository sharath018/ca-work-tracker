"""Database schema definition and management."""

import sqlite3
import logging

logger = logging.getLogger("CAWorkTracker")

# Schema version for future migrations
SCHEMA_VERSION = 1


def create_schema(cursor):
    """Create the database schema."""
    try:
        # Main work_log table with improved data types
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS work_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                client TEXT NOT NULL,
                category TEXT NOT NULL,
                summary TEXT,
                hours REAL DEFAULT 0.0,
                billable INTEGER DEFAULT 0,
                amount REAL DEFAULT 0.0,
                status TEXT DEFAULT 'Pending',
                requested_by TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes for frequently queried columns
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_work_log_status 
            ON work_log(status)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_work_log_client 
            ON work_log(client)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_work_log_date 
            ON work_log(date)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_work_log_requested_by 
            ON work_log(requested_by)
        """)
        
        # Schema version tracking table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER PRIMARY KEY,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Check if this is a fresh install
        cursor.execute("SELECT version FROM schema_version WHERE version = ?", (SCHEMA_VERSION,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO schema_version (version) VALUES (?)", (SCHEMA_VERSION,))
        
        logger.info("Database schema created/verified successfully")
        
    except sqlite3.Error as e:
        logger.error(f"Error creating database schema: {e}")
        raise


def convert_billable_to_bool(value):
    """Convert billable field to integer (0 or 1)."""
    if isinstance(value, str):
        return 1 if value.lower() in ['yes', 'true', '1'] else 0
    return int(value) if value else 0
