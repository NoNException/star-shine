from dataclasses import asdict
import sqlite3
import pandas as pd
from app.assets.data_class import UserInfo
from app.config import DATABASE_PATH
from typing import List


# 初始化数据库
def init_user_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS t_user (
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
def insert_user(user_info: UserInfo):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO t_user (id, name, birthday, luna_birthday, address, phone)
        VALUES (:id, :name, :birthday, :luna_birthday, :address, :phone)
    """,
        asdict(user_info),
    )
    conn.commit()
    conn.close()


# 查询所有用户
def fetch_users():
    """
     获取全部的用户
    :param parser: 是否进行类型转换, True 则转换成 List[UserInfo]

    :return: List[UserInfo]
    """

    conn = sqlite3.connect(DATABASE_PATH)
    df = pd.read_sql_query("SELECT * FROM t_user", conn)
    conn.close()
    return df


# 更新用户信息
def update_user(user_info: UserInfo):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE t_user
        SET name = :name,
        birthday = :birthday,
        luna_birthday= :luna_birthday, 
        address = :address, 
        phone = :phone
        WHERE id = :id
    """,
        asdict(user_info),
    )
    conn.commit()
    conn.close()


# 删除用户
def delete_user(user_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM t_user WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
