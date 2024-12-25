from numpy import save
import pandas as pd
from pandas import DataFrame
import time
import streamlit as st
from typing import List
from app.assets.data_class import UserInfo
from app.assets.data_in_pagination import pagination_container
from app.utils.daos.user_db import (
    fetch_users,
    init_user_db,
    insert_user,
    update_user,
)
from app.utils.daos.file_handler import read_uploaded_file

# 初始化数据库
init_user_db()


def save_func(base_ids: List[int], users: DataFrame):
    total_len = len(users)
    sync_bar = st.progress(0, "数据同步中...")
    for index, row in users.iterrows():
        user_id = int(row["id"])
        row_indict = row.to_dict()
        if user_id in base_ids:
            update_user(UserInfo(**row_indict))
        else:
            insert_user(UserInfo(**row_indict))
        sync_bar.progress(
            int(index + 1) / total_len * 1.0, text=f"{index + 1} / {total_len}"
        )
        time.sleep(0.3)
    time.sleep(1)


def load_user_from_excel(exists_user_id: List[int]):
    """从 excel 文件中读取用户信息
    :param exists_user_id: 存在的用户 ID 列表
    """
    uploaded_file = st.file_uploader("上传舰长名单", type=["xlsx"])
    if uploaded_file and (
        "refresh" not in st.session_state.keys() or not st.session_state["refresh"]
    ):
        # 读取文件并显示
        user_info = read_uploaded_file(
            uploaded_file, date_cols=["birthday", "luna_birthday"]
        )
        save_func(exists_user_id, user_info)
        st.warning("用户信息更新成功!")
        time.sleep(1)
        st.session_state["refresh"] = True
        uploaded_file = False
        st.rerun()
    else:
        st.session_state["refresh"] = False


def update_user_info(user_id, selected_user):
    """根据 user_id 更新 用户信息"""
    with st.form("edit_form"):
        name = st.text_input("姓名", value=selected_user["name"])
        birthday = st.date_input(
            "生日", value=pd.to_datetime(selected_user["birthday"])
        )
        luna_birthday = st.date_input(
            "生日(农历)", value=pd.to_datetime(selected_user["luna_birthday"])
        )
        address = st.text_input("地址", value=selected_user["address"])
        phone = st.text_input("电话", value=selected_user["phone"])
        user_info = UserInfo(
            user_id,
            str(name),
            str(birthday),
            str(luna_birthday),
            str(address),
            str(phone),
        )
        submitted = st.form_submit_button("提交修改")
        if submitted:
            update_user(user_info)
            st.success("用户信息已更新！")
            st.session_state["refresh"] = True
            st.rerun()


def user_info_manager():
    # 上传功能
    # 展示和编辑功能
    st.header("👥 舰队", divider=True)
    users = fetch_users()
    if users.empty:
        # 将用户数据展示为表格
        st.write(" 舰长数据不存在, 请上传用户文件 ")
    pagination_container(users, save_func, data_editor=True)
    load_user_from_excel([int(u["id"]) for _, u in users.iterrows()])
