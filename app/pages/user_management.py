import pandas as pd
import os
from pathlib import Path
from pandas import DataFrame
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


def save_func(base_ids: List[int], users: DataFrame, mode):
    for index, row in users.iterrows():
        user_id = int(row["id"])
        row_indict = row.to_dict()
        if user_id in base_ids and mode == "override":
            update_user(UserInfo(**row_indict))
        else:
            insert_user(UserInfo(**row_indict))


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
    # load_user_from_excel([int(u["id"]) for _, u in users.iterrows()])
