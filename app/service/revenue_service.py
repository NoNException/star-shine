from datetime import datetime, timedelta
from typing import List

from app.utils.app_utils.common_utils import app_log
from app.utils.bilibili_apis.revenue_fetcher import query_revenue_list

from app.utils.daos.login_db import get_token
from app.utils.daos.revenue_db import save_revenues, query_revenues


@app_log
def bilibili_sync(start_date, end_date, day_callback=None, page_callback=None):
    """
    从 bilibili 中同步每日的收益记录
    :param start_date: 搜索的时间范围
    :param end_date: 搜索的时间范围
    :param day_callback: 每天同步完成后的回调函数
    :param page_callback: 每页同步完成后的回调函数
    """
    token, _ = get_token()
    revenues = []
    for day in days_gap(start_date, end_date):
        day_revenue = query_revenue_list(day, str(token), page_callback)
        if len(day_revenue) == 0:
            continue
        if day_callback is not None:
            day_callback(day, day_revenue)
        revenues.extend(day_revenue)
        save_revenues(day_revenue)


@app_log
def days_gap(start_date, end_date) -> List[datetime]:
    """
    返回两个时间字符串的天数, 默认date_range[0]  早于 date_range[1]
    :param start_date: 开始时间
    :param end_date: 结束时间
    return:  日期
    """
    days = [end_date.date()]
    while start_date < end_date:
        end_date -= timedelta(days=1)
        days.append(end_date)
    return days


def query_miss_day():
    """计算数据库中最近的一条数据距今的天数, 如果数据库中没有数据, 从月初开始计算;"""
    rows, _ = query_revenues(None, 1, 0, order_by="time", order_direction="DESC")
    last_day = (
        rows[0]["time"] if rows else datetime.strftime(datetime.now(), "%Y-%m-%d")
    )
    current_day = datetime.strftime(datetime.now(), "%Y-%m-%d")
    return days_gap([last_day, current_day])
