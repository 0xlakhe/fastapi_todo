# import json

# def read_todos():
#     try:
#         with open("todos.json") as file:
#             return json.load(file)
#     except FileNotFoundError:
#         return []

# def save_todos(todos):
#     with open("todos.json","w") as file:
#         file.write(json.dumps(todos))


import sqlite3
from fastapi import HTTPException


def get_connection():
    conn = sqlite3.connect("todos.db", check_same_thread=False, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS todos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            done BOOLEAN DEFAULT FALSE,
            created_at TEXT,
            user_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id) 
            )
    """)

    conn.commit()
    conn.close()


def create_user(username: str, email: str, password: str):
    conn = get_connection()
    conn.execute(
        "INSERT INTO users (username, email, password) VALUES(?, ?, ?)",
        (username, email, password),
    )
    conn.commit()
    conn.close()


def get_user(identifier: str):
    conn = get_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ? OR username = ?", (identifier, identifier)
    ).fetchone()
    conn.close()
    return dict(user) if user else None


def get_all_todos(user_id: int):
    conn = get_connection()
    todos = conn.execute("SELECT * FROM todos WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()
    return [dict(todo) for todo in todos]


def create_todo(task: str, done: bool, created_at: str, user_id: int):
    conn = get_connection()
    conn.execute(
        "INSERT  INTO todos (task, done, created_at, user_id) VALUES(?, ?, ?, ?)",
        (task, done, created_at, user_id),
    )
    conn.commit()
    conn.close()


def check_id(id: int) -> bool:
    conn = get_connection()
    check = conn.execute("SELECT * FROM todos WHERE id=?", (id,))
    todo = check.fetchone()
    conn.close()
    if todo is None:
        return False
    return True


def delete_todo(id: int):
    conn = get_connection()
    conn.execute("DELETE FROM todos WHERE id=?", (id,))
    conn.commit()
    conn.close()


def update_todo(id: int, task: str, done: bool):
    conn = get_connection()
    conn.execute("UPDATE todos SET task = ?, done=? WHERE id=?", (task, done, id))
    conn.commit()
    conn.close()
