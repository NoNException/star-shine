from itertools import count
import streamlit as st
from app.utils.bilibili_apis.revenue_fetcher import query_revenue_list
from app.utils.daos.login_db import get_token
from app.utils.daos.revenue_db import query_revenues, save_revenues
from app.utils.login_utils import require_login
from typing import List
from datetime import datetime, timedelta


# 收益管理
def days_gap(date_range: List[str]):
    """
    返回两个时间字符串的天数, 默认date_range[0]  早于 date_range[1]
    TODO 将这部分内容添加到 snippet 中
    :param date_range: 时间范围
    return:  日期
    """
    date_format = "%Y-%m-%d"

    start_date = datetime.strptime(date_range[0], date_format)
    if len(date_range) != 2 and not date_range[1]:
        end_date = datetime.today() - timedelta(1)
    else:
        end_date = datetime.strptime(date_range[0], date_format)
    return abs((end_date - start_date).days)


def bilibili_sync(start_date, end_date):
    """
    从 bilibili 中同步每日的收益记录
    :param user_name: 用户名称
    :param query_date_range: 搜索的时间范围
    :param query_amt: 查询的金额范围
    """
    token, _ = get_token()
    revenues = []
    for day in range(days_gap([start_date, end_date])):
        day_revenue = query_revenue_list(
            day,
            str(token),
        )
        revenues.extend(day_revenue)
        save_revenues(day_revenue)


def query_miss_day():
    """计算数据库中最近的一条数据距今的天数, 如果数据库中没有数据, 从月初开始计算;"""
    rows, _ = query_revenues(None, 1, 0, order_by="time", order_direction="DESC")
    last_day = (
        rows[0]["time"] if rows else datetime.strftime(datetime.now(), "%Y-%m-%d")
    )
    current_day = datetime.strftime(datetime.now(), "%Y-%m-%d")
    return days_gap([last_day, current_day])


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
        rows, count = query_revenues(
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
