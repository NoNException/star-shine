import sqlite3
from app.config import DATABASE_PATH


# 初始化用户登录表
def init_login_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            token TEXT NOT NULL,
            expires_at INTEGER NOT NULL  -- Unix 时间戳
        )
    """)
    conn.commit()
    conn.close()


# 保存用户 Token
def save_token(user_id, token, expires_at):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO user_tokens (user_id, token, expires_at)
        VALUES (?, ?, ?)
    """,
        (user_id, token, expires_at),
    )
    conn.commit()
    conn.close()


# 获取 Token
def get_token(user_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT token, expires_at FROM user_tokens WHERE user_id = ? ORDER BY id DESC LIMIT 1",
        (user_id,),
    )
    result = cursor.fetchone()
    conn.close()
    return result if result else (None, None)
