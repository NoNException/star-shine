from dataclasses import asdict
import sqlite3
from typing import List

import pandas as pd
from app.assets.data_class import UserInfo
from app.config import DATABASE_PATH
from app.utils.app_utils.common_utils import app_log


# 初始化数据库
def init_user_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS t_user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            bilibili_user_id INT, 
            avatar_url TEXT,
            birthday TEXT ,
            luna_birthday TEXT ,
            address TEXT,
            phone TEXT 
        )
    """)
    conn.commit()
    conn.close()


# 插入数据
@app_log
def insert_user(user_info: UserInfo):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO t_user (id, name, bilibili_user_id, avatar_url, birthday, luna_birthday, address, phone)
        VALUES (:id, :name, :bilibili_user_id ,:avatar_url, :birthday, :luna_birthday, :address, :phone)
    """,
        asdict(user_info),
    )
    conn.commit()
    conn.close()


# 查询所有用户
@app_log
def fetch_users() -> List[UserInfo]:
    """
     获取全部的用户
    :param parser: 是否进行类型转换, True 则转换成 List[UserInfo]

    :return: List[UserInfo]
    """

    conn = sqlite3.connect(DATABASE_PATH)
    df = pd.read_sql_query("SELECT * FROM t_user", conn)
    conn.close()
    users = [UserInfo(**(row)) for row in df.to_dict(orient='records')]
    return users


# 更新用户信息
@app_log
def update_user(user_info: UserInfo):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE t_user
        SET name = :name, 
        bilibili_user_id = :bilibili_user_id, 
        avatar_url = :avatar_url,
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
