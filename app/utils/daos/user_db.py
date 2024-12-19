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
            luna_birthday DATE NOT NULL,
            address TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# 插入数据
def insert_user(name, birthday, luna_birthday, address, phone):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO users (name, birthday, luna_birthday, address, phone)
        VALUES (?, ?, ?, ?, ? )
    """,
        (name, birthday, luna_birthday, address, phone),
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
def update_user(user_id, name, birthday, luna_birthday, address, phone):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE users
        SET name = ?, birthday = ?,luna_birthday=?, address = ?, phone = ?
        WHERE id = ?
    """,
        (name, birthday, luna_birthday, address, phone, user_id),
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
