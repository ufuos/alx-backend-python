# File: 0-databaseconnection.py
import sqlite3

class DatabaseConnection:
    """Custom context manager for handling database connections."""

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        # Open the connection and create a cursor
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Commit if no exception, rollback otherwise
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        # Close connection
        self.conn.close()


if __name__ == "__main__":
    # Demo usage
    with DatabaseConnection("example.db") as cursor:
        # Ensure table exists
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        # Insert sample data (only if empty)
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO users (name, age) VALUES (?, ?)",
                [("Alice", 30), ("Bob", 22), ("Charlie", 28)]
            )
        # Query
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print("Users:", results)
