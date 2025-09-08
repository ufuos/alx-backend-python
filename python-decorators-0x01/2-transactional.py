#!/usr/bin/env python3
import sqlite3
import functools

# --- with_db_connection decorator from previous task ---
def with_db_connection(func):
    """Decorator that opens and closes a SQLite connection for the wrapped function"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("my_database.db")  # or your DB file
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

# --- transactional decorator ---
def transactional(func):
    """Decorator that wraps DB operations in a transaction (commit/rollback)."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()   # commit if no error
            return result
        except Exception as e:
            conn.rollback()  # rollback on error
            raise e
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """Update user's email with automatic transaction handling"""
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


# Example usage
if __name__ == "__main__":
    update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com")
