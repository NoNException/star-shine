from datetime import datetime
import streamlit as st


def is_token_expired():
    """检查 Token 是否已过期"""

    expires_at = st.session_state.get("token_expires_at")
    if not expires_at:
        return True

    now = datetime.now().timestamp()
    return now > expires_at


def is_token_near_expiry(threshold=300):
    """
    检查 Token 是否即将过期
    - threshold: 时间阈值（秒），默认 300 秒（5 分钟）
    """
    expires_at = st.session_state.get("token_expires_at")
    if not expires_at:
        return True

    now = datetime.now().timestamp()
    return expires_at - now <= threshold
