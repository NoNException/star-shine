import requests

GIFTTYPE_API = "https://api.live.bilibili.com/gift/v1/master/getGiftTypes"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
REVENUE_API = "https://api.live.bilibili.com/xlive/revenue/v1/giftStream/getReceivedGiftStreamNextList"


def get_gitft_types():
    """获取到礼物类型
    return: 礼物类型
    """
    headers = {
        "origin": "https://link.bilibili.com",
        "referer": "https://link.bilibili.com/p/center/index",
        "user-gent": UA,
    }
    rep = requests.get(GIFTTYPE_API, headers=headers)
    if rep.status_code != 200:
        print(rep.content)
    return rep.json()


def query_revenue_list(date, gift_type: int):
    """
    获取指定天数,指定类型的礼物列表
    :param date: 需要查询的日期
    :param gift_type: 礼物类型
    return: 礼物列表
    """
    param = {
        "limit": 20,
        "coin_type": gift_type,
        "gift_id": "",
        "begin_time": date.strftime("%Y-%m-%d"),
        "uname": "",
    }

    headers = {
        "origin": "https://link.bilibili.com",
        "referer": "https://link.bilibili.com/p/center/index",
        "user-agent": UA,
    }

    rep = requests.get(REVENUE_API, params=param, headers=headers)
    if rep.status_code != 200:
        print(rep.content)
    return rep.json()
