import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from app.utils.daos.user_db import (
    init_db,
    fetch_users,
)
from app.utils.daos.reminder_db import (
    init_reminder_db,
    fetch_reminder_time,
    set_reminder_time,
)

# 初始化数据库
init_reminder_db()
init_db()


def page_render():
    st.header("🎂 生日提醒", divider=True)

    # 功能 1：显示每日发送生日提醒的时间
    reminder_time = fetch_reminder_time()
    if reminder_time:
        st.write(f"当前提醒时间为：**{reminder_time}**")
    else:
        st.warning("您尚未设置提醒时间！请设置提醒时间。")

    with st.form("set_reminder_time"):
        new_time = st.time_input(
            "设置新的提醒时间",
        )
        submitted = st.form_submit_button("保存时间")
        if submitted:
            time_str = new_time.strftime("%H:%M:00")
            set_reminder_time(time_str)
            st.success(f"提醒时间已设置为：{time_str}")
            st.rerun()

    # 功能 2：展示 1/3/7 天内即将过生日的用户
    st.header("即将过生日的用户", divider=True)
    users = fetch_users()

    if not users.empty:
        today = datetime.today()
        try:
            users["birthday"] = pd.to_datetime(users["birthday"], errors="coerce")
            users["days_to_birthday"] = users["birthday"].apply(
                lambda x: (x.replace(year=today.year) - today).days
                if pd.notnull(x)
                else None
            )
            users["days_to_birthday"] = users["days_to_birthday"].apply(
                lambda x: x if x >= 0 else x + 365
            )
        except Exception as e:
            st.write(e)

        for days in [1, 3, 7]:
            upcoming_users = users[users["days_to_birthday"] <= days]
            st.subheader(f"未来 {days} 天内过生日的用户")
            st.dataframe(upcoming_users[["name", "birthday", "days_to_birthday"]])
    else:
        st.write("暂无用户数据，请先添加用户信息。")

    # 功能 3：选择日期展示周围过生日的用户
    st.header("按日期查看生日用户")
    selected_date = st.date_input("选择日期", value=datetime.today())
    selected_range = st.slider("选择日期范围（天）", min_value=1, max_value=15, value=7)

    if not users.empty:
        selected_users = users[
            users["days_to_birthday"].between(-selected_range, selected_range)
        ]
        st.write(f"在 {selected_date} 的前后 {selected_range} 天内过生日的用户：")
        st.dataframe(selected_users[["name", "birthday", "days_to_birthday"]])

    else:
        st.write("暂无用户数据，请先添加用户信息。")
