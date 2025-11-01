import sqlite3

def connect():
    db = sqlite3.connect("data.db", check_same_thread=False)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = connect()
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            balance REAL DEFAULT 0,
            card TEXT
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS channels (
            channel_id INTEGER PRIMARY KEY
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            admin_id INTEGER PRIMARY KEY
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id INTEGER,
            reward REAL,
            limit_count INTEGER,
            done INTEGER DEFAULT 0
        )
    """)
    db.commit()
    db.close()

def add_user(user_id, username=None):
    db = connect()
    db.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    db.commit()
    db.close()

def get_users():
    db = connect()
    result = db.execute("SELECT * FROM users").fetchall()
    db.close()
    return [dict(r) for r in result]

def get_random_user():
    db = connect()
    result = db.execute("SELECT user_id FROM users ORDER BY RANDOM() LIMIT 1").fetchone()
    db.close()
    return result["user_id"] if result else None

def add_balance(user_id, amount):
    db = connect()
    db.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
    db.commit()
    db.close()

def update_card(user_id, card):
    db = connect()
    db.execute("UPDATE users SET card = ? WHERE user_id = ?", (card, user_id))
    db.commit()
    db.close()

def get_channels():
    db = connect()
    result = db.execute("SELECT * FROM channels").fetchall()
    db.close()
    return [r["channel_id"] for r in result]

def add_channel(channel_id):
    db = connect()
    db.execute("INSERT OR IGNORE INTO channels (channel_id) VALUES (?)", (channel_id,))
    db.commit()
    db.close()

def remove_channel(channel_id):
    db = connect()
    db.execute("DELETE FROM channels WHERE channel_id = ?", (channel_id,))
    db.commit()
    db.close()

def add_admin(admin_id):
    db = connect()
    db.execute("INSERT OR IGNORE INTO admins (admin_id) VALUES (?)", (admin_id,))
    db.commit()
    db.close()

def get_admins():
    db = connect()
    result = db.execute("SELECT * FROM admins").fetchall()
    db.close()
    return [r["admin_id"] for r in result]

def remove_admin(admin_id):
    db = connect()
    db.execute("DELETE FROM admins WHERE admin_id = ?", (admin_id,))
    db.commit()
    db.close()

def add_task(channel_id, reward, limit_count):
    db = connect()
    db.execute(
        "INSERT INTO tasks (channel_id, reward, limit_count, done) VALUES (?, ?, ?, 0)",
        (channel_id, reward, limit_count)
    )
    db.commit()
    db.close()

def get_tasks():
    db = connect()
    result = db.execute("SELECT * FROM tasks").fetchall()
    db.close()
    return [dict(r) for r in result]

def delete_task(task_id):
    db = connect()
    db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    db.close()

init_db()
