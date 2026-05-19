import sqlite3

conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS premium_users (
    user_id INTEGER PRIMARY KEY
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS memories (
    user_id INTEGER,
    role TEXT,
    content TEXT
)
''')

conn.commit()


def add_premium(user_id):
    cursor.execute(
        "INSERT OR IGNORE INTO premium_users VALUES (?)",
        (user_id,)
    )
    conn.commit()


def is_premium(user_id):
    cursor.execute(
        "SELECT * FROM premium_users WHERE user_id=?",
        (user_id,)
    )

    return cursor.fetchone() is not None


def save_memory(user_id, role, content):
    cursor.execute(
        "INSERT INTO memories VALUES (?, ?, ?)",
        (user_id, role, content)
    )

    conn.commit()


def get_memory(user_id):
    cursor.execute(
        "SELECT role, content FROM memories WHERE user_id=? ORDER BY rowid DESC LIMIT 10",
        (user_id,)
    )

    rows = cursor.fetchall()

    rows.reverse()

    return [
        {
            "role": role,
            "content": content
        }
        for role, content in rows
    ]
