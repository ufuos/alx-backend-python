#!/usr/bin/python3
"""
Memory-Efficient Aggregation with Generators
Compute average age of users without loading the full dataset into memory.
"""

import mysql.connector


def stream_user_ages():
    """
    Generator that yields user ages one by one from the user_data table
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ALX_prodev"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:
        yield age

    cursor.close()
    conn.close()


def calculate_average_age():
    """
    Calculates average age using the generator without loading all rows into memory
    """
    total = 0
    count = 0

    for age in stream_user_ages():
        total += age
        count += 1

    average = total / count if count > 0 else 0
    print(f"Average age of users: {average}")


if __name__ == "__main__":
    calculate_average_age()
