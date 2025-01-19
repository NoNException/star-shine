from dataclasses import dataclass, field
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
class Revenue():
    id: int = None
    uid: int = None
    uname: str = None
    time: str = None
    is_empty: bool = None
    gift_id: int = None
    gift_name: str = None
    gift_img: str = None
    gift_num: int = None
    gold: int = None
    silver: int = None
    hamster: int = None
    ios_hamster: int = None
    normal_hamster: int = None
    ios_gold: int = None
    normal_gold: int = None
    is_hybrid: bool = None
    is_open_platfrom: int = None
    open_platfrom_rate: float = None
    receive_title: str = None
    room_id: int = None


if __name__ == '__main__':
    revenue = Revenue(id=12)
    print(revenue.__dict__)
