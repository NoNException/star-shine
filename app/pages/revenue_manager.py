import streamlit as st
from app.utils.login_utils import require_login


@require_login
def page_render():
    return None
