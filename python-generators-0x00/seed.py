#!/usr/bin/python3
"""
seed.py - Setup MySQL database ALX_prodev and user_data table,
and insert data from user_data.csv
"""

import mysql.connector
from mysql.connector import errorcode
import csv
import uuid


def connect_db():
    """Connects to the MySQL server (not to a specific database)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",      # update if your MySQL username is different
            password=""       # update if your MySQL password is set
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_database(connection):
    """Creates ALX_prodev database if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")


def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",      # update if your MySQL username is different
            password="",      # update if your MySQL password is set
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None


def create_table(connection):
    """Creates the user_data table if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX(user_id)
            )
        """)
        connection.commit()
        print("Table user_data created successfully")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")


def insert_data(connection, csv_file):
    """Inserts data from CSV into user_data table if not already present."""
    try:
        cursor = connection.cursor()
        with open(csv_file, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Generate a UUID if not provided
                user_id = str(uuid.uuid4())

                # Check if record already exists
                cursor.execute(
                    "SELECT * FROM user_data WHERE email = %s",
                    (row["email"],)
                )
                exists = cursor.fetchone()

                if not exists:
                    cursor.execute(
                        "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                        (user_id, row["name"], row["email"], row["age"])
                    )
        connection.commit()
        cursor.close()
    except FileNotFoundError:
        print(f"CSV file {csv_file} not found.")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
