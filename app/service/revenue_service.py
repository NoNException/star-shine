from datetime import datetime, timedelta
from typing import List

from app.utils.app_utils.common_utils import app_log
from app.utils.bilibili_apis.revenue_fetcher import query_revenue_list

from app.utils.daos.login_db import get_token
from app.utils.daos.revenue_db import save_revenues, query_revenues


@app_log
def bilibili_sync(start_date, end_date):
    """
    从 bilibili 中同步每日的收益记录
    :param start_date: 用户名称
    :param end_date: 搜索的时间范围
    """
    token, _ = get_token()
    revenues = []
    for day in days_gap([start_date, end_date]):
        day_revenue = query_revenue_list(day, str(token), )
        if len(day_revenue) == 0:
            continue
        revenues.extend(day_revenue)
        save_revenues(day_revenue)


@app_log
def days_gap(date_range: List[str]):
    """
    返回两个时间字符串的天数, 默认date_range[0]  早于 date_range[1]
    :param date_range: 时间范围
    return:  日期
    """
    date_format = "%Y-%m-%d"

    start_date = datetime.strptime(date_range[0], date_format)
    end_date = datetime.strptime(date_range[1], date_format) if date_range[1] else datetime.today()
    date_lists = [end_date.date()]
    while start_date < end_date:
        end_date -= timedelta(days=1)
        date_lists.append(end_date)
    return date_lists


def query_miss_day():
    """计算数据库中最近的一条数据距今的天数, 如果数据库中没有数据, 从月初开始计算;"""
    rows, _ = query_revenues(None, 1, 0, order_by="time", order_direction="DESC")
    last_day = (
        rows[0]["time"] if rows else datetime.strftime(datetime.now(), "%Y-%m-%d")
    )
    current_day = datetime.strftime(datetime.now(), "%Y-%m-%d")
    return days_gap([last_day, current_day])
