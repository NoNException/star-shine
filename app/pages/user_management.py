import pandas as pd
import streamlit as st

from app.assets.data_class import UserInfo
from app.utils.daos.user_db import (
    delete_user,
    fetch_users,
    init_user_db,
    insert_user,
    update_user,
)
from app.utils.daos.file_handler import read_uploaded_file

# 初始化数据库
init_user_db()


def load_user_from_excel():
    """从 excel 文件中读取用户信息"""

    st.write("数据库中没有用户信息。请上传数据。")
    uploaded_file = st.file_uploader("上传舰长名单", type=["xlsx"])

    if uploaded_file:
        try:
            # 读取文件并显示
            user_info = read_uploaded_file(
                uploaded_file, date_cols=["birthday", "luna_birthday"]
            )
            st.write("上传的数据预览：")
            st.dataframe(user_info)

            if st.button("保存到数据库"):
                for _, row in user_info.iterrows():
                    row_indict = row.to_dict()
                    insert_user(UserInfo(**row_indict))
                st.success("用户信息已成功保存！")
                st.session_state["refresh"] = True
                st.rerun()
        except Exception as e:
            st.error(f"文件处理出错：{e}")


def user_info_manager():
    # 上传功能

    # 展示和编辑功能
    st.header("👥 舰队", divider=True)
    users = fetch_users()

    if not users.empty:
        # 将用户数据展示为表格
        st.dataframe(users)
        # 编辑功能
        st.subheader("✏️ 编辑用户信息")
        user_id = st.selectbox("选择用户 ID", users["id"])
        selected_user = users[users["id"] == user_id].iloc[0]

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

            submitted = st.form_submit_button("提交修改")
            if submitted:
                update_user(user_id, name, birthday, luna_birthday, address, phone)
                st.success("用户信息已更新！")
                st.session_state["refresh"] = True
                st.rerun()

        # 删除功能
        if st.button("删除用户"):
            delete_user(user_id)
            st.warning("用户已被删除！")
            st.session_state["refresh"] = True
            st.rerun()
    else:
        load_user_from_excel()
