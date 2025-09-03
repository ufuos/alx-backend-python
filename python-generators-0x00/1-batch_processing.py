#!/usr/bin/python3
"""
Batch processing users with generators
"""

import mysql.connector


def stream_users_in_batches(batch_size):
    """
    Generator that fetches users in batches from user_data table
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_data")
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows

    cursor.close()
    conn.close()
    return  # explicitly added return


def batch_processing(batch_size):
    """
    Processes batches of users, filtering users over age 25
    """
    results = []
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                print(user)
                results.append(user)
    return results  # explicitly added return
