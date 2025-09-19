# File: 1-execute.py
import sqlite3

class ExecuteQuery:
    """Context manager that executes a query with parameters and returns results."""

    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params else ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        # Open connection
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        # Execute query
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Commit changes if safe
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        # Close
        self.conn.close()


if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    with ExecuteQuery("example.db", query, (25,)) as results:
        print("Users older than 25:", results)
