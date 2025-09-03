#!/usr/bin/python3
import mysql.connector

def stream_users():
    """
    Generator that streams rows from the user_data table one by one.
    Yields each row as a dictionary.
    """
    # Connect to the database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",          # update with your MySQL username
        password="password",  # update with your MySQL password
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)

    # Execute the query
    cursor.execute("SELECT * FROM user_data")

    # Yield rows one by one
    for row in cursor:
        yield row

    # Cleanup
    cursor.close()
    conn.close()
