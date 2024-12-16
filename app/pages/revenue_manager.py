import streamlit as st
from app.utils.bilibili_apis.revenue_fetcher import query_revenue_list
from app.utils.daos.login_db import get_token
from app.utils.login_utils import require_login
from typing import List
from datetime import datetime
# 收益管理


def revenue_search(user_name: str, query_date_range: List[str], query_amt: int):
    """
    按照用户名称, 时间范围, 金额范围查询收益数据
    :param user_name: 用户名称
    :param query_date_range: 搜索的时间范围
    :param query_amt: 查询的金额范围
    """
    token, _ = get_token()

    revenues = query_revenue_list(None, str(token), date_str="2024-12-13")
    return revenues


@require_login
def revenue_lister():
    st.title("直播收益")
    # 导出选项
    revenues = []
    with st.form("ExportPanel"):
        st.write("选择范围")
        user_name = st.text_input(
            "用户名称",
        )
        query_date_start = st.date_input("查询日期(开始)", datetime.now())
        query_date_end = st.date_input("查询日期(结束)", datetime.now())
        query_amt = st.number_input(" 电池范围", -1)

        revenues = st.form_submit_button(
            label="Search",
            on_click=revenue_search,
            args=(user_name, query_date_start, query_date_end, query_amt),
        )

    st.write("收益明细")
    if revenues:
        st.dataframe(revenues)
        st.button("导出查询内容")
