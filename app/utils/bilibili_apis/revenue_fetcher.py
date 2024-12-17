from logging import raiseExceptions
from sqlite3 import Error
from pandas.core.frame import itertools
import requests
import streamlit as st
from streamlit.runtime.state import session_state

GIFTTYPE_API = "https://api.live.bilibili.com/gift/v1/master/getGiftTypes"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
REVENUE_API = "https://api.live.bilibili.com/xlive/revenue/v1/giftStream/getReceivedGiftStreamNextList"

request_session = requests.Session()
request_session.headers.update(
    {
        "origin": "https://link.bilibili.com",
        "referer": "https://link.bilibili.com/p/center/index",
        "user-agent": UA,
    }
)


def get_gitft_types():
    """获取到礼物类型
    return: 礼物类型
    """
    rep = requests.get(GIFTTYPE_API)
    if rep.status_code != 200:
        print(rep.content)
    return rep.json()


def query_revenue_list(date, session_data: str, page_size=20):
    """
    调取 bilibil 的接口, 获取指定天数
    :param date: 需要查询的日期
    :param page_size: 每页查询数量
    return: 礼物列表
    """
    param = {
        "limit": page_size,
        "coin_type": "",  # 礼物类型, 电池礼物, 银瓜子礼物
        "gift_id": "",  # 礼物 ID
        "begin_time": date.strftime("%Y-%m-%d"),
        "uname": "",
    }
    cookie = {"SESSDATA": session_data}
    entries = []
    for pn in itertools.count():
        try:
            rep = request_session.get(REVENUE_API, params=param, cookies=cookie)
            if rep.status_code != 200:
                raise Error(f"Query error {pn} with param:{param}, resp:{rep.content}")
            data = rep.json()["data"]
            entries.extend(data["list"])
            if not data["list"] or not data.get("has_more"):
                # 未查到数据
                break
            param["last_id"] = data["list"][-1]["id"]
        except Error as e:
            raise Error(f"Query exception at {pn}, cuz {e}")
    return entries
