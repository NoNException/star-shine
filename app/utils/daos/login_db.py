import sqlite3
from typing import Tuple
from app.config import DATABASE_PATH


# 初始化用户登录表
def init_login_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bilibili_token (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT NOT NULL,
            expires_at INTEGER NOT NULL  -- Unix 时间戳
        )
    """)
    conn.commit()
    conn.close()


# 保存用户 Token
def save_token(token, expires_at):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO bilibili_token (token, expires_at)
        VALUES (?, ?)
    """,
        (token, expires_at),
    )
    conn.commit()
    conn.close()


# 获取 Token
def get_token():
    """获取用户的 Token :param user_id: 用户 Id"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT token, expires_at FROM bilibili_token ORDER BY id DESC LIMIT 1"
    )
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0], result[1]
    return None, None
