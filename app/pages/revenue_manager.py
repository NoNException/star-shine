import streamlit as st
from app.utils.bilibili_apis.revenue_fetcher import query_revenue_list
from app.utils.daos.login_db import get_token
from app.utils.login_utils import require_login
from datetime import datetime
# 收益管理


@require_login
def revenue_lister():
    st.title("直播收益")
    token, _ = get_token()
    revenues = query_revenue_list(datetime.now(), str(token))
    st.dataframe(revenues)
    # TODO
