import os
import sqlite3

# 🔥 FIXED DB PATH (VERY IMPORTANT)
DB_PATH = os.path.join(os.getcwd(), "mindmate.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS user_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        mood TEXT,
        rumination TEXT,
        emotion TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_full_data(text, mood, rumination, emotion):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "INSERT INTO user_data (text, mood, rumination, emotion) VALUES (?, ?, ?, ?)",
        (text, mood, rumination, emotion)
    )

    conn.commit()
    conn.close()


def get_all_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT * FROM user_data")
    data = c.fetchall()

    conn.close()
    return data