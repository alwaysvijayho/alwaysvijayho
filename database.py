import sqlite3

# Database connection
db = sqlite3.connect("users.db", check_same_thread=False)
cursor = db.cursor()

# Table create karna
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    msg_count INTEGER DEFAULT 0,
    protection INTEGER DEFAULT 0
)
""")
db.commit()

def add_user(user_id):
    cursor.execute("INSERT OR IGNORE INTO users(user_id) VALUES(?)", (user_id,))
    db.commit()

def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchone()

def update_count(user_id, count):
    cursor.execute("UPDATE users SET msg_count=? WHERE user_id=?", (count, user_id))
    db.commit()

def set_protection(user_id, value):
    cursor.execute("UPDATE users SET protection=? WHERE user_id=?", (value, user_id))
    db.commit()

def reset_user(user_id):
    cursor.execute("UPDATE users SET msg_count=0, protection=0 WHERE user_id=?", (user_id,))
    db.commit()