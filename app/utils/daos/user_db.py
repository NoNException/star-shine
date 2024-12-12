import sqlite3
import pandas as pd
from app.config import DATABASE_PATH


# 初始化数据库
def init_user_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            birthday DATE NOT NULL,
            email TEXT,
            phone TEXT
        )
    """)
    conn.commit()
    conn.close()


# 插入数据
def insert_user(name, birthday, email, phone):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO users (name, birthday, email, phone)
        VALUES (?, ?, ?, ?)
    """,
        (name, birthday, email, phone),
    )
    conn.commit()
    conn.close()


# 查询所有用户
def fetch_users():
    conn = sqlite3.connect(DATABASE_PATH)
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()
    return df


# 更新用户信息
def update_user(user_id, name, birthday, email, phone):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE users
        SET name = ?, birthday = ?, email = ?, phone = ?
        WHERE id = ?
    """,
        (name, birthday, email, phone, user_id),
    )
    conn.commit()
    conn.close()


# 删除用户
def delete_user(user_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
