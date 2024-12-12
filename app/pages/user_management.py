import pandas as pd
import streamlit as st

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


def page_render1():
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
            email = st.text_input("邮箱", value=selected_user["email"])
            phone = st.text_input("电话", value=selected_user["phone"])

            submitted = st.form_submit_button("提交修改")
            if submitted:
                update_user(user_id, name, birthday, email, phone)
                st.success("用户信息已更新！")
                st.session_state["refresh"] = True

        # 删除功能
        if st.button("删除用户"):
            delete_user(user_id)
            st.warning("用户已被删除！")
            st.session_state["refresh"] = True
    else:
        st.write("数据库中没有用户信息。请上传数据。")
        uploaded_file = st.file_uploader("上传舰长名单", type=["xlsx"])

        if uploaded_file:
            try:
                # 读取文件并显示
                data = read_uploaded_file(uploaded_file)
                st.write("上传的数据预览：")
                st.dataframe(data)

                if st.button("保存到数据库"):
                    for _, row in data.iterrows():
                        insert_user(
                            row["name"], row["birthday"], row["email"], row["phone"]
                        )
                    st.success("用户信息已成功保存！")
                    st.session_state["refresh"] = True
            except Exception as e:
                st.error(f"文件处理出错：{e}")
