from typing import List

import streamlit as st
import pandas as pd
from datetime import datetime

from app.assets.data_class import UserInfo
from app.utils.daos.user_db import (
    init_user_db, fetch_users,
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
