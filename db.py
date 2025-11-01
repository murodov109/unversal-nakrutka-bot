import sqlite3
import random

def connect():
    return sqlite3.connect("data.db", check_same_thread=False)

def create_tables():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        username TEXT,
        balance REAL DEFAULT 0,
        card TEXT DEFAULT ''
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_id INTEGER UNIQUE
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS channels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_id TEXT UNIQUE
    )
    """)
    conn.commit()
    conn.close()

def add_user(user_id, username=None):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cur.fetchone()
    conn.close()
    return user

def add_balance(user_id, amount):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()

def get_balance(user_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else 0

def add_channel(channel_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO channels (channel_id) VALUES (?)", (channel_id,))
    conn.commit()
    conn.close()

def get_channels():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT channel_id FROM channels")
    channels = [row[0] for row in cur.fetchall()]
    conn.close()
    return channels

def remove_channel(channel_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM channels WHERE channel_id = ?", (channel_id,))
    conn.commit()
    conn.close()

def add_admin(admin_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO admins (admin_id) VALUES (?)", (admin_id,))
    conn.commit()
    conn.close()

def get_admins():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT admin_id FROM admins")
    admins = [row[0] for row in cur.fetchall()]
    conn.close()
    return admins

create_tables()
