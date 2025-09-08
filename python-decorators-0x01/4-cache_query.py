
#!/usr/bin/env python3
import time
import sqlite3
import functools

# Global cache dictionary
query_cache = {}

def cache_query(func):
    """Decorator to cache query results for 10 seconds"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query")  # Extract query string from kwargs
        if query in query_cache:
            result, timestamp = query_cache[query]
            # Check if cached result is still valid
            if time.time() - timestamp < 10:
                print("✅ Using cached result")
                return result
            else:
                # Expired, remove from cache
                del query_cache[query]

        # Execute the function and cache the result
        result = func(*args, **kwargs)
        query_cache[query] = (result, time.time())
        print("🔄 Query executed and cached")
        return result
    return wrapper


def with_db_connection(func):
    """Decorator to manage DB connection automatically"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("my_database.db")  # open DB connection
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()  # ensure connection is closed
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    # Example usage
    users = fetch_users_with_cache(query="SELECT * FROM users")
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    
    time.sleep(11)  # wait for cache to expire
    users_after_expiry = fetch_users_with_cache(query="SELECT * FROM users")
