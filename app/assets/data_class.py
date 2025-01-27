from calendar import month
from dataclasses import dataclass
from datetime import datetime, timedelta

from docutils.nodes import target
from lunar_python import Lunar

from app.utils.app_utils.common_utils import app_log


@dataclass
class UserInfo:
    id: int = None
    name: str = None
    bilibili_user_id: int = None
    # 头像名称
    avatar_url: str = None
    birthday: str = None
    luna_birthday: str = None
    address: str = None
    address_detail: str = None
    phone: str = None
    days_to_birthday: int = None
    showing_birthday: str = None

    @staticmethod
    @app_log
    def lua_date2solar_date(date: datetime):
        if date is None:
            return None
        lunar_date = UserInfo.to_luna_date(date)
        solar_date = lunar_date.getSolar()
        solar_year = solar_date.getYear()
        solar_month = solar_date.getMonth()
        solar_day = solar_date.getDay()
        return datetime(solar_year, solar_month, solar_day)

    @staticmethod
    def to_luna_date(date):
        today_luna = Lunar.fromDate(datetime.today())
        luna_year = today_luna.getYear()
        if date.month <= abs(today_luna.getMonth()) and date.day < abs(today_luna.getDay()):
            luna_year = today_luna.getYear() + 1
        # 设置今年的农历
        lunar_date = Lunar.fromYmd(lunar_year=luna_year, lunar_month=date.month, lunar_day=date.day)
        return lunar_date

    def str2date(self, date_str):
        """
        将日期字符串转换为 datetime 对象
        """
        today = datetime.today()
        if date_str is None:
            return None
        try:
            date = datetime.strptime(date_str, "%Y/%m/%d")
        except Exception as e:
            try:
                date = datetime.strptime(date_str, "%m/%d")
            except Exception as e:
                raise Exception(f"Error format of birthday: {self}")

        date = date.replace(year=today.year)
        return date

    def cal_days_to_birthday(self):
        """
       判断是否在生日前后7天
       :param pass_day: 当前日期距离生日多少天
       """
        solar_date = self.str2date(self.birthday)
        birthday_gaps = days_to_date(solar_date)
        luna_date = self.str2date(self.luna_birthday)
        luna_birthday_gaps = days_to_date(self.lua_date2solar_date(luna_date))

        target_date = min(birthday_gaps or luna_birthday_gaps, luna_birthday_gaps or birthday_gaps)
        if target_date == luna_birthday_gaps:
            lunar_date = self.to_luna_date(luna_date)
            self.showing_birthday = (f"{lunar_date.getYearInChinese()}/{lunar_date.getMonthInChinese()}月"
                                     f"/{lunar_date.getDayInChinese()}日")
        else:
            self.showing_birthday = solar_date.strftime("%Y/%m/%d")
        self.days_to_birthday = target_date

    def birthday_in_range(self, pass_day):
        return pass_day >= self.days_to_birthday >= 0

    def __lt__(self, other):
        return self.days_to_birthday <= other.days_to_birthday


def days_to_date(date):
    today = datetime.today()
    if date is None:
        return None
    if date.month <= today.month and date.day < today.day:
        return (date.replace(year=today.year + 1) - today).days + 1.1
    else:
        return (date.replace(year=today.year) - today).days + 1.1


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
