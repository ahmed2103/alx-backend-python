#!/usr/bin/env python3
"""
Class-based context manager to handle opening and closing and query
a SQLite database connection automatically.
"""

import sqlite3


class ExecuteQuery:
    """Custom context manager for SQLite database connection."""

    def __init__(self, query, param):
        self.param = param
        self.connection = None
        self.cursor = None
        self.query = query

    def __enter__(self):
        """Open database connection and return cursor."""
        self.connection = sqlite3.connect("users.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query,(self.param,))
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close cursor and connection. Commit if no exception occurred."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
            self.connection.close()


if __name__ == "__main__":
    with ExecuteQuery("SELECT * FROM users WHERE age > ?",25) as results:
        for row in results:
            print(row)
