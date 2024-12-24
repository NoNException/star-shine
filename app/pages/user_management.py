import pandas as pd
import time
import streamlit as st
from typing import List
from app.assets.data_class import UserInfo
from app.utils.daos.user_db import (
    fetch_users,
    init_user_db,
    insert_user,
    update_user,
)
from app.utils.daos.file_handler import read_uploaded_file

# 初始化数据库
init_user_db()


def load_user_from_excel(user_exists: List[UserInfo]):
    """从 excel 文件中读取用户信息"""
    uploaded_file = st.file_uploader("上传舰长名单", type=["xlsx"])
    if uploaded_file and (
        "refresh" not in st.session_state.keys() or not st.session_state["refresh"]
    ):
        user_dict = [u.id for u in user_exists]
        # 读取文件并显示
        user_info = read_uploaded_file(
            uploaded_file, date_cols=["birthday", "luna_birthday"]
        )
        total_len = len(user_info)
        sync_bar = st.progress(0, "数据同步中...")
        for index, row in user_info.iterrows():
            user_id = int(row["id"])
            row_indict = row.to_dict()
            if user_id in user_dict:
                update_user(UserInfo(**row_indict))
            else:
                insert_user(UserInfo(**row_indict))
            sync_bar.progress(
                int(index + 1) / total_len * 1.0, text=f"{index + 1} / {total_len}"
            )
            time.sleep(0.1)
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
    if not users.empty:
        # 将用户数据展示为表格
        st.write("数据不存在, 请上传用户文件 ")
    st.data_editor(users, num_rows="dynamic")
    user_infos = [UserInfo(**u.to_dict()) for _, u in users.iterrows()]
    bt = st.button(" 保存当前页")
    if bt:
        print("anna ")
    load_user_from_excel(user_infos)
