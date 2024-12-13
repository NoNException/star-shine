import streamlit as st
from app.utils.login_utils import require_login

# 收益管理


@require_login
def revenue_lister():
    st.title("this is revenue demo. ")
