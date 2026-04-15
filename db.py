import sqlite3

conn = sqlite3.connect("app.db", check_same_thread=False)
c = conn.cursor()

def create_tables():
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT,
        password TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        username TEXT,
        source TEXT,
        destination TEXT,
        price INTEGER,
        date TEXT
    )
    """)
    conn.commit()