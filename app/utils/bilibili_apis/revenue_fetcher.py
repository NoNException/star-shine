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


def query_revenue_list(date, session_data: str):
    """
    获取指定天数,指定类型的礼物列表
    :param date: 需要查询的日期
    :param gift_type: 礼物类型
    return: 礼物列表
    """
    param = {
        "limit": 20,
        "coin_type": "",
        "gift_id": "",
        "begin_time": date.strftime("%Y-%m-%d"),
        "uname": "",
    }

    print(f"session_data,0000000000 {session_data}")
    cookie = {"SESSDATA": session_data}

    rep = request_session.get(REVENUE_API, params=param, cookies=cookie)
    print(f"return,-0000000000- {rep}")
    if rep.status_code != 200:
        print(rep.content)
    rep_json = rep.json()
    return rep_json["data"]["list"]
