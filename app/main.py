import streamlit as st

from app.pages import revenue_manager
from app.pages import user_management
from app.pages import birthday_manager


# pages navigation
pages = {
    "Home Page": [
        st.Page(user_management.user_info_manager, title="😊舰长信息"),
        st.Page(birthday_manager.birthday_notify, title="🎂生日提醒"),
        st.Page(revenue_manager.revenue_lister, title="🎁直播收益"),
    ]
}
pg = st.navigation(pages)
pg.run()
