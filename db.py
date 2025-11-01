import sqlite3

class Database:
    def __init__(self, db_file="database.db"):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    balance INTEGER DEFAULT 0,
                    referrer_id INTEGER,
                    last_bonus TEXT
                )
            """)

    def add_user(self, user_id, referrer_id=None):
        with self.connection:
            self.cursor.execute(
                "INSERT OR IGNORE INTO users (user_id, referrer_id) VALUES (?, ?)",
                (user_id, referrer_id)
            )

    def get_balance(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,)).fetchone()
            return res[0] if res else 0

    def update_balance(self, user_id, amount):
        with self.connection:
            self.cursor.execute(
                "UPDATE users SET balance = balance + ? WHERE user_id=?",
                (amount, user_id)
            )

    def get_all_users(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM users").fetchall()

    def set_last_bonus(self, user_id, date):
        with self.connection:
            self.cursor.execute("UPDATE users SET last_bonus=? WHERE user_id=?", (date, user_id))

    def get_last_bonus(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT last_bonus FROM users WHERE user_id=?", (user_id,)).fetchone()
            return res[0] if res else None
