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
            address_detail TEXT,
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
        INSERT INTO t_user (id, name, bilibili_user_id, avatar_url, birthday, luna_birthday, address,address_detail, phone)
        VALUES (:id, :name, :bilibili_user_id ,:avatar_url, :birthday, :luna_birthday, :address, :address_detail, :phone)
    """,
        asdict(user_info),
    )
    conn.commit()
    conn.close()


# 查询所有用户
@app_log
def fetch_users(order_by="id", desc=True,
                limit=5,
                query_all=False,
                fuzz_query=None) -> List[UserInfo]:
    """
     获取全部的用户
    :param order_by:
    :param desc: 是否倒序排列
    :param limit: 数量限制
    :param query_all: 是否获取全部
    :param fuzz_query: 查询条件
    :return: List[UserInfo]
    """

    conn = sqlite3.connect(DATABASE_PATH)
    where_condition = (f"WHERE name like '%{fuzz_query}%' or address like '%{fuzz_query}%' "
                       f"or phone like '%{fuzz_query}%' or bilibili_user_id like '%{fuzz_query}%' "
                       f"group by bilibili_user_id ") \
        if fuzz_query else ""

    sql = f"SELECT * FROM t_user {where_condition}" if query_all else \
        f"SELECT * FROM t_user {where_condition}  order by {order_by} {'desc' if desc else ''} limit {limit}"
    df = pd.read_sql_query(sql, conn)
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
        address_detail = :address_detail,
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
