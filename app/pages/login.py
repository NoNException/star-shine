# 搜码登录页面
#
from urllib.parse import quote
import streamlit as st
import time
from app.utils.login_utils import generate_qr_code, poll_qr_code
from app.utils.daos.login_db import init_login_db, save_token

init_login_db()


def page_render():
    st.title("📲 用户扫码登录")
    st..

    # 请求二维码
    try:
        img, qrcode_key = generate_qr_code()
        st.image(
            image=img,
            caption="请使用 Bilibili App 扫码登录",
        )
        st.write("正在等待扫码...")

        while True:
            response_data = poll_qr_code(qrcode_key)
            status_code = response_data["data"]["code"]

            if status_code == 86101:  # 未扫码
                st.info("等待用户扫码...")
            elif status_code == 86090:  # 已扫码未确认
                st.warning("用户已扫码，请在手机上确认登录。")
            elif status_code == 0:  # 登录成功
                st.success("登录成功！")
                login_url = response_data["data"]["url"]
                tokens = parse_login_url(login_url)
                st.write(tokens)
                session_data = quote(tokens["SESSDATA"])
                save_token(session_data, tokens["Expires"])

                # 更新登录状态
                st.session_state["logged_in"] = True
                st.session_state["user_token"] = session_data
                st.session_state["token_expires_at"] = tokens["Expires"]
                st.rerun()
            elif status_code == 86038:  # 二维码失效
                st.error("二维码已失效，请重新获取。")
                break

            time.sleep(10)  # 轮询间隔
    except Exception as e:
        st.error(f"登录失败：{e}")
        st.write(e)
        print(e)


# 解析登录 URL，提取 Token
def parse_login_url(url):
    from urllib.parse import parse_qs, urlparse

    query = parse_qs(urlparse(url).query)
    return {
        "SESSDATA": query.get("SESSDATA", [None])[0],
        "Expires": int(query.get("Expires", [0])[0]),
    }
