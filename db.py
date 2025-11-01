import sqlite3
import random

def connect():
    return sqlite3.connect("data.db", check_same_thread=False)

def create_tables():
    conn = connect()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER UNIQUE, username TEXT, balance REAL DEFAULT 0, last_bonus TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS admins (id INTEGER PRIMARY KEY AUTOINCREMENT, admin_id INTEGER UNIQUE)")
    cur.execute("CREATE TABLE IF NOT EXISTS channels (id INTEGER PRIMARY KEY AUTOINCREMENT, channel_id TEXT UNIQUE)")
    cur.execute("CREATE TABLE IF NOT EXISTS payments (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, amount REAL, status TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, link TEXT, amount INTEGER, done INTEGER DEFAULT 0)")
    conn.commit()
    conn.close()

def add_user(user_id, username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()

def get_balance(user_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    data = cur.fetchone()
    conn.close()
    return data[0] if data else 0

def update_balance(user_id, amount):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
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
    data = [r[0] for r in cur.fetchall()]
    conn.close()
    return data

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
    data = [r[0] for r in cur.fetchall()]
    conn.close()
    return data

def remove_channel(channel_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM channels WHERE channel_id = ?", (channel_id,))
    conn.commit()
    conn.close()

def add_order(user_id, link, amount):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO orders (user_id, link, amount) VALUES (?, ?, ?)", (user_id, link, amount))
    conn.commit()
    conn.close()

def get_orders():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    data = cur.fetchall()
    conn.close()
    return data

create_tables()
