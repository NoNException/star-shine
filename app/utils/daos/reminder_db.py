import sqlite3
from app.config import DATABASE_PATH


# 初始化提醒表
def init_reminder_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reminder_time TEXT
        )
    """)
    conn.commit()
    conn.close()


# 获取提醒时间
def fetch_reminder_time():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT reminder_time FROM reminders ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


# 设置提醒时间
def set_reminder_time(reminder_time):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reminders (reminder_time) VALUES (?)", (reminder_time,))
    conn.commit()
    conn.close()
