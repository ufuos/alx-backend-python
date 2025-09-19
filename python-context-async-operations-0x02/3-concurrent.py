#!/usr/bin/env python3
"""
Concurrent Asynchronous Database Queries using aiosqlite
"""

import asyncio
import aiosqlite


# Async function to fetch ALL users
async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:  # connect to SQLite db
        db.row_factory = aiosqlite.Row  # return rows as dict-like objects
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]  # convert each row to dict


# Async function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


# Run both queries concurrently
async def fetch_concurrently():
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("✅ All Users:")
    print(users)
    print("\n✅ Users older than 40:")
    print(older_users)


# Entry point
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
