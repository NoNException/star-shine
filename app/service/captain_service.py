from pathlib import Path
from typing import List

import streamlit as st
import pandas as pd
from datetime import datetime

from pandas import DataFrame

from app.assets.data_class import UserInfo
from app.utils.daos.file_handler import read_uploaded_file
from app.utils.daos.user_db import (
    init_user_db, fetch_users, update_user, insert_user,
)
from app.utils.daos.reminder_db import (
    fetch_reminder_time,
    set_reminder_time,
)

init_user_db()


def user_to_birthday(days: int) -> List[UserInfo]:
    """
    获取未来 days 天内过生日的用户
    """
    users = fetch_users()
    # 日期格式转换
    upcoming_users: List[UserInfo] = [u for u in users if u.birthday_in_range(days)]
    return upcoming_users


def load_user_from_excel(excel_file_path: str, mode: str = "override"):
    """从 excel 文件中读取用户信息
    :param excel_file_path: 存在的用户 ID 列表
    :param mode: 模式, override 覆盖, append 追加
    """
    home = str(Path.home())
    user_info = read_uploaded_file(
        f"{home}{excel_file_path.split(home)[-1]}",
        date_cols=["birthday", "luna_birthday"],
    )
    exists_user_id = []
    save_func(exists_user_id, user_info, mode)


def save_func(base_ids: List[int], users: DataFrame, mode):
    for index, row in users.iterrows():
        user_id = int(row["id"]) if "id" in row.keys() else None
        row_indict = row.to_dict()
        if user_id in base_ids and mode == "override":
            update_user(UserInfo(**row_indict))
        else:
            insert_user(UserInfo(**row_indict))
