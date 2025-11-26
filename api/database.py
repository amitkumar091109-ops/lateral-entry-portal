"""
Database Connection Management
Provides database connection utilities
"""

import sqlite3
from contextlib import contextmanager
from typing import Optional
from .config import get_config

config = get_config()


class Database:
    """Database connection manager"""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or config.DATABASE_PATH

    @contextmanager
    def get_connection(self):
        """Get database connection with automatic cleanup"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        try:
            yield conn
        finally:
            conn.close()

    def execute(self, query: str, params: tuple = ()):
        """Execute a query and return results"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.fetchall()

    def execute_one(self, query: str, params: tuple = ()):
        """Execute a query and return single result"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()

    def execute_many(self, query: str, params_list: list):
        """Execute query with multiple parameter sets"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
            return cursor.rowcount

    def insert(self, query: str, params: tuple = ()):
        """Insert and return last row ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid


# Global database instance
db = Database()


def row_to_dict(row) -> dict:
    """Convert SQLite Row to dictionary"""
    if row is None:
        return None
    return dict(zip(row.keys(), row))


def rows_to_dict_list(rows) -> list:
    """Convert list of SQLite Rows to list of dictionaries"""
    return [row_to_dict(row) for row in rows]
