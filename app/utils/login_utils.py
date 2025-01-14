# 登录状态检查

from datetime import datetime
import streamlit as st

from app.utils.bilibili_apis.bilibili_token_manager import (
    is_token_expired,
    is_token_near_expiry,
)
from app.utils.daos.login_db import get_token, init_login_db

init_login_db()


def require_login(render_function):
    """检查登录态装饰器, 在相应页面的渲染方法中可以要求状态校验"""

    def wrapper(*args, **kwargs):
        # 初始化登录状态
        if "logged_in" not in st.session_state:
            st.session_state["logged_in"] = False
            st.session_state["user_token"] = None
            st.session_state["token_expires_at"] = None

        if not st.session_state["logged_in"]:
            token, expire_at = get_token()
            if token and expire_at and datetime.now().timestamp() < float(expire_at):
                st.session_state["logged_in"] = True
                st.session_state["user_token"] = token
                st.session_state["token_expires_at"] = expire_at

            # 检查登录状态
            if not st.session_state["logged_in"] or is_token_expired():
                from app.pages.login import page_render

                st.warning("登录状态失效，请重新登录！")
                page_render()
                return  # 阻止加载其他页面

        # 提醒 Token 即将过期
        if is_token_near_expiry():
            st.warning("Token 即将过期，请尽快重新登录！")

        # 如果登录状态正常，加载原页面
        return render_function(*args, **kwargs)

    return wrapper






