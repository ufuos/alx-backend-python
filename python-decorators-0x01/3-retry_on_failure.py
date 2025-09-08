#!/usr/bin/env python3
import time
import sqlite3
import functools
import random

DB_NAME = "users.db"

# --------------------------
# Retry decorator
# --------------------------
def retry_on_failure(retries=3, delay=2):
    """Retries a function if it raises an exception (simulate transient DB errors)."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    # Artificial random failure simulation (30% chance)
                    if random.random() < 0.3:
                        raise sqlite3.OperationalError("Simulated transient failure")

                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"[Retry {attempts}/{retries}] Error: {e}")
                    if attempts >= retries:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

# --------------------------
# DB connection decorator
# --------------------------
def with_db_connection(func):
    """Provide a SQLite connection to the wrapped function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(DB_NAME)
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

# --------------------------
# Setup script: create table + dummy data
# --------------------------
def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    # Insert dummy data if table is empty
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.executemany("INSERT INTO users (name) VALUES (?)",
                        [("Alice",), ("Bob",), ("Charlie",)])
        conn.commit()
    conn.close()

# --------------------------
# Example query function
# --------------------------
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# --------------------------
# Main Execution
# --------------------------
if __name__ == "__main__":
    setup_database()  # Ensure DB + table exists
    users = fetch_users_with_retry()
    print("\nFetched users:", users)
