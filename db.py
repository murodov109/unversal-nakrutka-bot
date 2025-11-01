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
    CREATE TABLE IF NOT EXISTS channels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_id INTEGER UNIQUE
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_id INTEGER UNIQUE
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT,
        description TEXT
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


def get_users():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users")
    users = [row[0] for row in cur.fetchall()]
    conn.close()
    return users


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


def update_card(user_id, card_number):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET card = ? WHERE user_id = ?", (card_number, user_id))
    conn.commit()
    conn.close()


def add_task(task_name, description):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (task_name, description) VALUES (?, ?)", (task_name, description))
    conn.commit()
    conn.close()


def get_random_user():
    users = get_users()
    if users:
        return random.choice(users)
    return None


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


class Database:
    @staticmethod
    def add_user(user_id, username=None):
        return add_user(user_id, username)

    @staticmethod
    def get_users():
        return get_users()

    @staticmethod
    def add_balance(user_id, amount):
        return add_balance(user_id, amount)

    @staticmethod
    def get_balance(user_id):
        return get_balance(user_id)

    @staticmethod
    def update_card(user_id, card_number):
        return update_card(user_id, card_number)

    @staticmethod
    def add_task(task_name, description):
        return add_task(task_name, description)

    @staticmethod
    def get_random_user():
        return get_random_user()

    @staticmethod
    def add_channel(channel_id):
        return add_channel(channel_id)

    @staticmethod
    def get_channels():
        return get_channels()

    @staticmethod
    def remove_channel(channel_id):
        return remove_channel(channel_id)

    @staticmethod
    def add_admin(admin_id):
        return add_admin(admin_id)

    @staticmethod
    def get_admins():
        return get_admins()

create_tables()

def load_db():
    create_tables()
    return True

def save_db():
    return True
create_tables()
