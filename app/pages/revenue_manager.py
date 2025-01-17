import streamlit as st

from app.service.revenue_service import bilibili_sync, query_miss_day
from app.utils.daos.revenue_db import query_revenues
from app.utils.login_utils import require_login
from datetime import datetime, timedelta


# 收益管理


@require_login
def revenue_lister():
    st.title("")
    # 导出选项
    if miss_day := query_miss_day():
        st.write(f"还差{miss_day}的数据未同步,点击同步")
        st.button(label="同步数据")

        export_panel = st.form("ExportPanel")
        export_panel.write("选择范围")
        query_date_start = export_panel.date_input("查询日期(开始)", datetime.now())
        query_date_end = export_panel.date_input("查询日期(结束)", datetime.now())
        click = export_panel.form_submit_button(
            label="Search",
            on_click=bilibili_sync,
            args=(query_date_start, query_date_end),
        )
        if click:
            rows, count = query_revenues(limit=20, offset=0)
            st.dataframe(rows)
            print(count)

        st.button("导出查询内容")
    date_start = st.date_input("查询日期(开始)", datetime.now() - timedelta(7))
    date_end = st.date_input("查询日期(结束)", datetime.now())
    amt_start = st.number_input("金额S", 0)
    amt_end = st.number_input("金额E", None)
    user_name = st.text_input("舰长名称")
    gift_name = st.selectbox("礼物搜索", options=["1", "2", "3"])
    query_click = st.button("查询")
    if query_click:
        rows, revenue_count = query_revenues(
            {
                "start_time": date_start,
                "unmae": user_name,
                "min_gold": amt_start,
                "max_gold": amt_end,
                "end_time": date_end,
                "gift_name": gift_name,
            },
            limit=10,
            offset=0,
        )
        st.dataframe(rows)
    else:
        st.dataframe(query_revenues())
    st.title("收益明细")
