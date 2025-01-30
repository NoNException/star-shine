from datetime import datetime
from typing import List, Tuple

from app.assets.data_class import Revenue
from app.config import DATABASE_PATH
import sqlite3

from app.utils.app_utils.common_utils import app_log


def init_db():
    """初始化数据表"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS t_revenue (
            id INTEGER PRIMARY KEY,
            uid INTEGER,
            uname TEXT,
            time TEXT,
            is_empty BOOLEAN,
            gift_id INTEGER,
            gift_name TEXT,
            gift_img TEXT,
            gift_num INTEGER,
            hamster INTEGER,
            gold INTEGER,
            silver INTEGER,
            ios_hamster INTEGER,
            normal_hamster INTEGER,
            ios_gold INTEGER,
            normal_gold INTEGER,
            is_hybrid BOOLEAN,
            is_open_platfrom INTEGER,
            open_platfrom_rate REAL,
            receive_title TEXT,
            room_id INTEGER
        )
    """)
    conn.commit()
    conn.close()


# 初始化数据库
init_db()


# 插入直播数据
@app_log
def save_revenues(data):
    """插入数据"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.executemany(
        """
        INSERT INTO t_revenue (
            id, uid, uname, time, is_empty, gift_id, gift_name, gift_img, gift_num,
            hamster, gold, silver, ios_hamster, normal_hamster,
            ios_gold, normal_gold, is_hybrid, is_open_platfrom,
            open_platfrom_rate, receive_title, room_id
        ) VALUES (
            :id, :uid, :uname, :time, 0, :gift_id, :gift_name, :gift_img, :gift_num,
            :hamster, :gold, :silver, :ios_hamster, :normal_hamster,
            :ios_gold, :normal_gold, :is_hybrid, :is_open_platfrom,
            :open_platfrom_rate, :receive_title, :room_id
        )
    """, data)
    conn.commit()
    conn.close()


@app_log
def query_revenues(limit=10, offset=0, order_by="time", order_direction="DESC",
                   query_all=0, **filters) -> tuple[
    List[Revenue], int]:
    """
    按照条件组合查询直播数据，支持分页和自定义排序。

    :param filters: 字典格式查询条件，例如：
        {
            "start_time": "2024-12-13 00:00:00",
            "end_time": "2024-12-15 23:59:59",
            "gift_name": "花",
            "uid": 27292944,
            "uname": "摸鱼",
            "min_gold": 50,
            "max_gold": 200,
            "gift_id": 31036,
        }
    :param limit: 每页条数（默认 10 条）
    :param offset: 偏移量（默认 0，表示第一页）
    :param order_by: 排序字段（默认按 `time` 排序）
    :param query_all: 1= 全部导出, 忽略分页参数
    :param order_direction: 排序方向，`ASC` 或 `DESC`（默认 `ASC`）
    :return: 查询结果列表
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # 使结果以字典格式返回
    cursor = conn.cursor()

    # 构建查询条件
    query = "SELECT * FROM t_revenue WHERE 1=1"
    params = {}
    conditions = ""
    # 添加过滤条件
    if filters:
        if "start_time" in filters and filters["start_time"] is not None:
            conditions += " AND time >= :start_time"
            params["start_time"] = filters["start_time"]
        if "end_time" in filters and filters["end_time"] is not None:
            conditions += " AND time < :end_time"
            params["end_time"] = filters["end_time"]
        if "gift_name" in filters and filters["gift_name"] is not None:
            conditions += " AND gift_name LIKE :gift_name"
            params["gift_name"] = f"%{filters['gift_name']}%"
        if "uid" in filters and filters["uid"] is not None:
            conditions += " AND uid = :uid"
            params["uid"] = filters["uid"]
        if "uname" in filters and filters["uname"] is not None:
            conditions += " AND uname LIKE :uname"
            params["uname"] = f"%{filters['uname']}%"
        if "min_gold" in filters and filters["min_gold"] is not None:
            conditions += " AND gold >= :min_gold"
            params["min_gold"] = filters["min_gold"]
        if "max_gold" in filters and filters["max_gold"] is not None:
            conditions += " AND gold <= :max_gold"
            params["max_gold"] = filters["max_gold"]
        if "gift_id" in filters and filters["gift_id"] is not None:
            conditions += " AND gift_id = :gift_id"
            params["gift_id"] = filters["gift_id"]

    # 添加排序条件
    query = query + conditions + f" ORDER BY {order_by} {order_direction}"

    if query_all == 0:
        # 添加分页条件
        query += " LIMIT :limit OFFSET :offset"
        params["limit"] = limit
        params["offset"] = offset

    # 执行查询
    cursor.execute(query, params)
    rows = cursor.fetchall()
    count_query = " select count(1) from t_revenue WHERE 1=1 "
    count_query += conditions
    cursor.execute(count_query, params)
    count = cursor.fetchone()

    conn.close()
    return [Revenue(**dict(row)) for row in rows], count[0]


def query_miss_days():
    """
    查询最近一次同步收益的时间
    """
    sql = "select max(time) from t_revenue"
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.close()
    if result[0] is None:
        return 0
    latest_days = datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')
    return (datetime.now() - latest_days).days
