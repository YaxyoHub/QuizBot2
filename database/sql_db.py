import sqlite3
import json

DB_NAME = "quizzes.db"

def create_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            name TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            username TEXT,
            user_id INTEGER UNIQUE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            options TEXT,
            correct_option_id INTEGER
        )
    """)

    conn.commit()
    conn.close()

""" Admin """

def check_admin(admin_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins WHERE user_id = ?;", (admin_id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data

def get_admin():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def add_admin(name, phone, username, user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO admins (name, phone, username, user_id) VALUES (?, ?, ?, ?);", (name, phone, username, user_id,))
    conn.commit()
    cursor.close()
    conn.close()

""" User """
def check_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?;", (user_id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data

def get_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users WHERE user_id = ?;", (user_id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data

def get_users_id():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_user_count():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users;")
        count = cursor.fetchone()[0]
    return count

def add_user(name, user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, user_id) VALUES (?, ?);", (name, user_id,))
    conn.commit()
    cursor.close()
    conn.close()
"""-------------------------------------------------"""


""" Quiz """

def add_quiz(question, options, correct_option_id):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO quizzes (question, options, correct_option_id)
            VALUES (?, ?, ?)
        """, (question, json.dumps(options), correct_option_id))
        conn.commit()

def get_all_quiz():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quizzes ORDER BY RANDOM();")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def delete_quiz(quiz_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM quizzes WHERE id = ?", (quiz_id,))
    conn.commit()
    cursor.close()
    conn.close()
