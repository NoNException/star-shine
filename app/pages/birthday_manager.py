import streamlit as st
import pandas as pd
from datetime import datetime
from app.utils.daos.user_db import (
    init_user_db,
)
from app.utils.daos.reminder_db import (
    init_reminder_db,
    fetch_reminder_time,
    set_reminder_time,
)

# 初始化数据库
init_reminder_db()
init_user_db()


def save_reminder_time():
    """save reminder time"""
    time_picker = st.session_state.reminder_time
    time_str = time_picker.strftime("%H:%M")
    set_reminder_time(time_str)


def birthday_notify():
    st.header("🎂 生日提醒", divider=True)

    time_seeting_bar = st.columns((3, 1))
    with time_seeting_bar[0]:
        # 功能 1：显示每日发送生日提醒的时间
        reminder_time = fetch_reminder_time()
        if reminder_time:
            st.write(f"当前提醒时间为：**{reminder_time}**")
        else:
            st.warning("尚未设置提醒时间！请设置提醒时间。")
    with time_seeting_bar[1]:
        change_alert_time = st.button("修改时间")
    if change_alert_time:
        with st.form("set_reminder_time"):
            st.time_input("设置新的提醒时间", key="reminder_time")
            st.form_submit_button(
                "保存时间",
                on_click=save_reminder_time,
            )
    # 功能 2：展示 1/3/7 天内即将过生日的用户
    st.header("即将过生日的用户", divider=True)
    users = []
    # users = fetch_users()

    if not users.empty:

        def days_to_birthday(birthday):
            today = datetime.today()
            if not birthday:
                return -1
            if birthday.month < today.month:
                return (birthday.replace(year=today.year + 1) - today).days + 1
            else:
                return (birthday.replace(year=today.year) - today).days + 1

        try:
            users["birthday"] = pd.to_datetime(users["birthday"], format="%Y-%m-%d")
            users["days_to_birthday"] = users["birthday"].apply(
                lambda x: days_to_birthday(x)
            )
        except Exception as e:
            st.write(e)

        for days in [7]:
            upcoming_users = users[users["days_to_birthday"] <= days][
                ["name", "birthday", "days_to_birthday"]
            ]
            st.markdown(f"未来 {days} 天内过生日的用户")
            upcoming_users.sort_values(by="days_to_birthday")
            st.dataframe(upcoming_users)
    else:
        st.write("暂无用户数据，请先添加用户信息。")

    # 功能 3：选择日期展示周围过生日的用户
    st.markdown("按日期查看生日用户")
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
