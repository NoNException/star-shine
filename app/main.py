import streamlit as st

from app.pages import revenue_manager
from app.pages import user_management
from app.pages import birthday_manager


# 页面映射
pages = {
    "系统管理": [
        st.Page(user_management.page_render, title="😊舰长信息"),
        st.Page(birthday_manager.page_render, title="🎂生日提醒"),
        st.Page(revenue_manager.page_render, title="🎁直播收益"),
    ]
}
pg = st.navigation(pages)
pg.run()
