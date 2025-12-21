import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB = "database.db"

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """)

def create_user(username, email, password):
    hashed = generate_password_hash(password)
    with sqlite3.connect(DB) as conn:
        conn.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed)
        )

def get_user_by_username(username):
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cur.fetchone()

def verify_user(username, password):
    user = get_user_by_username(username)
    if user and check_password_hash(user[3], password):
        return user
    return None
