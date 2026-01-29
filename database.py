"""Database connection and initialization."""

import sqlite3
import os
from contextlib import contextmanager
from typing import Generator, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "employees.db")


class Database:
    """SQLite database manager for Employee Management System."""

    def __init__(self, db_path: str = DB_PATH):
        """Initialize database connection."""
        self.db_path = db_path
        self._init_schema()

    def _init_schema(self) -> None:
        """Create employees table if it doesn't exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    position TEXT NOT NULL,
                    salary REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Get database connection with context manager."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def execute_query(self, query: str, params: tuple = ()) -> list:
        """Execute SELECT query and return all results."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def execute_single(self, query: str, params: tuple = ()) -> Optional[dict]:
        """Execute SELECT query and return single result."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None

    def execute_insert(self, query: str, params: tuple = ()) -> int:
        """Execute INSERT query and return last inserted id."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid

    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute UPDATE query and return number of affected rows."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount

    def execute_delete(self, query: str, params: tuple = ()) -> int:
        """Execute DELETE query and return number of affected rows."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount


# Global database instance
db = Database()