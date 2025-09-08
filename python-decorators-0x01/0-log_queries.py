#!/usr/bin/env python3
import sqlite3
import functools
from datetime import datetime  # added

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract query from arguments (positional or keyword)
        query = None
        if 'query' in kwargs:
            query = kwargs['query']
        elif len(args) > 0:
            query = args[0]

        # Log the SQL query
        if query:
            print(f"[{datetime.now()}] Executing SQL Query: {query}")

        # Execute the original function
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Example: fetch users while logging the query
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
