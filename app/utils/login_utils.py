# 登录状态检查

import streamlit as st
import requests

from app.utils.bilibili_apis.bilibili_token_manager import (
    is_token_expired,
    is_token_near_expiry,
)


def require_login(render_function):
    """检查登录态装饰器"""

    def wrapper(*args, **kwargs):
        # 初始化登录状态
        if "logged_in" not in st.session_state:
            st.session_state["logged_in"] = False
            st.session_state["user_token"] = None
            st.session_state["token_expires_at"] = None

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


def generate_qr_code():
    url = "https://passport.bilibili.com/x/passport-login/web/qrcode/generate"
    response = requests.get(url)
    response_data = response.json()
    if response_data["code"] == 0:
        return response_data["data"]["url"], response_data["data"]["qrcode_key"]
    raise Exception("Failed to generate QR code.")


# 查询二维码状态
def poll_qr_code(qrcode_key):
    url = "https://passport.bilibili.com/x/passport-login/web/qrcode/poll"
    response = requests.get(url, params={"qrcode_key": qrcode_key})
    response_data = response.json()
    return response_data
