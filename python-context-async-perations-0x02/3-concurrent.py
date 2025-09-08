import aiosqlite
import asyncio

async def async_fetch_users():
    db  = await aiosqlite.connect("users.db")
    cursor = await db.execute("select * from users")
    rows = await cursor.fetchall()
    return rows

async def async_fetch_older_users():
    db = await aiosqlite.connect("users.db")
    cursor = await db.execute("select * from users where age > 40")
    rows = await cursor.fetchall()
    return rows

async def fetch_concurrently():
    all, older = await asyncio.gather(async_fetch_users(),async_fetch_older_users())
    print("all",all)
    print("older than 40",older)

asyncio.run(fetch_concurrently())