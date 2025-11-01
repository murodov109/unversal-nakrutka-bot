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
        bonus_date TEXT DEFAULT ''
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS channels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_username TEXT UNIQUE
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_id INTEGER UNIQUE
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        link TEXT,
        amount INTEGER,
        done INTEGER DEFAULT 0
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

def get_balance(user_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else 0

def update_balance(user_id, amount):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()

def set_bonus_date(user_id, date):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET bonus_date = ? WHERE user_id = ?", (date, user_id))
    conn.commit()
    conn.close()

def get_bonus_date(user_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT bonus_date FROM users WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else ''

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

def add_channel(username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO channels (channel_username) VALUES (?)", (username,))
    conn.commit()
    conn.close()

def get_channels():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT channel_username FROM channels")
    channels = [row[0] for row in cur.fetchall()]
    conn.close()
    return channels

def remove_channel(username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM channels WHERE channel_username = ?", (username,))
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
    orders = cur.fetchall()
    conn.close()
    return orders

def update_order_done(order_id, done):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE orders SET done = ? WHERE id = ?", (done, order_id))
    conn.commit()
    conn.close()

create_tables()
