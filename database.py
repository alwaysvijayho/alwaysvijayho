import sqlite3

conn = sqlite3.connect(
    "userprotect.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    message_count INTEGER DEFAULT 0,
    protection INTEGER DEFAULT 1,
    last_reply INTEGER DEFAULT 0
)
""")

conn.commit()


def add_user(user_id, username="", first_name=""):
    cursor.execute("""
        INSERT OR IGNORE INTO users
        (user_id, username, first_name)
        VALUES (?, ?, ?)
    """, (user_id, username, first_name))
    conn.commit()


def get_user(user_id):
    cursor.execute(
        "SELECT * FROM users WHERE user_id=?",
        (user_id,)
    )
    return cursor.fetchone()


def update_count(user_id, count):
    cursor.execute(
        "UPDATE users SET message_count=? WHERE user_id=?",
        (count, user_id)
    )
    conn.commit()


def reset_count(user_id):
    cursor.execute(
        "UPDATE users SET message_count=0 WHERE user_id=?",
        (user_id,)
    )
    conn.commit()


def enable_protection(user_id):
    cursor.execute(
        "UPDATE users SET protection=1 WHERE user_id=?",
        (user_id,)
    )
    conn.commit()


def disable_protection(user_id):
    cursor.execute(
        "UPDATE users SET protection=0 WHERE user_id=?",
        (user_id,)
    )
    conn.commit()


def update_reply_time(user_id, timestamp):
    cursor.execute(
        "UPDATE users SET last_reply=? WHERE user_id=?",
        (timestamp, user_id)
    )
    conn.commit()


def delete_user(user_id):
    cursor.execute(
        "DELETE FROM users WHERE user_id=?",
        (user_id,)
    )
    conn.commit()


def close():
    conn.close()
