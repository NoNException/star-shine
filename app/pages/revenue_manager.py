import streamlit as st
from app.utils.login_utils import require_login

# 收益管理


@require_login
def page_render3():
    st.title("this is revenue demo. ")
