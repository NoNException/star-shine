from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserInfo:
    id: int = None
    name: str = None
    birthday: str = None
    luna_birthday: str = None
    address: str = None
    phone: str = None
    days_to_birthday: int = None

    def birthday_in_range(self, pass_day):
        days = datetime.strptime(self.birthday, "%Y-%m-%d")
        day_gaps = days_to_birthday(days)
        self.days_to_birthday = day_gaps
        return pass_day >= day_gaps >= 0

    def __lt__(self, other):
        return self.days_to_birthday <= other.days_to_birthday


def days_to_birthday(birthday):
    today = datetime.today()
    if not birthday:
        return -1
    if birthday.month < today.month:
        return (birthday.replace(year=today.year + 1) - today).days + 1
    else:
        return (birthday.replace(year=today.year) - today).days + 1


@dataclass
class Revenue:
    id: int
    # Revenue ID
    uid: int
    # 用户名称
    uname: str
    # 例如提交时间 日期
    time: str
    # 是否空数据
    is_empty: bool
    # 礼物 ID
    gift_id: int
    # 礼物名称
    gift_name: str
    # 礼物图片
    gift_img: str
    # 礼物数量
    gift_num: int
    hamster: int
    gold: int
    silver: int
    ios_hamster: int
    normal_hamster: int
    ios_gold: int
    normal_gold: int
    is_hybrid: bool
    is_open_platfrom: int
    open_platfrom_rate: float
    receive_title: str
    room_id: int
