from datetime import datetime

import flet as ft
from docutils.nodes import label
from flet.core.types import CrossAxisAlignment
from lunar_python import Lunar

from app.assets.data_class import UserInfo
from app.utils.bilibili_apis.user_info_fetcher import get_user_details
from app.utils.daos.login_db import get_token
from app.utils.daos.user_db import delete_user, update_user, insert_user


class UserModifier(ft.Container):
    """用户添加 panel"""

    def __init__(self, app, page: ft.Page, user_info: UserInfo = None):
        super().__init__()
        self.padding = ft.padding.only(left=20, right=20, top=20, bottom=20)
        self.date_picker_mode = "birthday"
        self.page = page
        self.app = app
        self.update_mode = user_info is not None
        self.date_picker = ft.DatePicker(
            first_date=datetime(year=2023, month=10, day=1),
            last_date=datetime(year=2025, month=10, day=1),
            date_picker_entry_mode=ft.DatePickerEntryMode.INPUT,
            on_change=lambda e: self.handle_birthday_change(e),
        )

        self.user_info = user_info if user_info else UserInfo()

        user_form = self.build_user_form()
        # 是否是更新模式, 更新模式下, 支持用户删除
        self.content = user_form

    @property
    def user_avatar(self):
        return ft.CircleAvatar(background_image_src=self.user_info.avatar_url, radius=30, max_radius=100)

    @user_avatar.setter
    def user_avatar(self, url):
        self.user_info.avatar_url = url

    @property
    def user_nick_name(self):
        def _setter(name):
            self.user_info.name = name.control.value

        return ft.TextField(label='昵称', value=self.user_info.name, on_blur=lambda e: _setter(e.data))

    @user_nick_name.setter
    def user_nick_name(self, name):
        self.user_info.name = name

    @property
    def user_bilibili_id(self):
        return ft.TextField(label='MID',
                            value=str(self.user_info.bilibili_user_id), hint_text="输入 MID, 回车确认",
                            on_submit=lambda e: self.fetch_user_bilibili_info(e))

    @user_bilibili_id.setter
    def user_bilibili_id(self, mid):
        self.user_info.bilibili_user_id = mid

    @property
    def user_birthday(self):
        today_str = f"格式:{datetime.today().strftime("%m/%d")}"

        def _setter(birthday):
            birthday_str = birthday.control.value
            try:
                datetime.strptime(birthday_str, "%m/%d")
                birthday_tf.error_text = None
                self.user_birthday = birthday_str
                birthday_tf.update()
            except Exception as e:
                birthday_tf.error_text = "日期格式错误, 请输入 MM/DD"
                birthday_tf.value = ""
                birthday_tf.update()

        birthday_tf = ft.TextField(value=self.user_info.birthday,
                                   label="生日(阳历)", hint_text=today_str,
                                   on_blur=lambda e: _setter(e))
        return birthday_tf

    @user_birthday.setter
    def user_birthday(self, birthday):
        self.user_info.birthday = birthday

    @property
    def user_luna_birthday(self):
        luna_str = self.default_luna_str()

        def _setter(luna_birthday):
            luna_birthday_str = luna_birthday.control.value
            try:
                luna_birthday_showing = str4luna(luna_birthday_str)
                if luna_birthday_showing is None:
                    raise Exception()
                luna_birthday_tf.value = luna_birthday_showing
                luna_birthday_tf.update()
                self.user_luna_birthday = luna_birthday_str
            except Exception as e:
                luna_birthday_tf.helper_text = "日期格式错误, 请输入01/02或2000/01/02. 即闰2月=-2。"
                luna_birthday_tf.value = str4luna(self.user_info.luna_birthday)
                luna_birthday_tf.update()

        def str4luna(luna_birthday_str):
            try:
                date_time = luna_birthday_str.split("/")
                time_year = datetime.today().year if len(date_time) == 2 else int(date_time[0])
                time_month = int(date_time[1 if len(date_time) == 3 else 0])
                time_day = int(date_time[2 if len(date_time) == 3 else 1])
                luna_date = Lunar.fromYmd(time_year, time_month, time_day)
                return (f"{f'{luna_date.getYearInChinese()}年/' if len(date_time) == 3 else ""}"
                        f"{luna_date.getMonthInChinese()}月/{luna_date.getDayInChinese()}")
            except Exception as e:
                print(e)
                # TODO 统一异常报错显示
                return None

        def show_luna_number():
            luna_birthday_tf.value = self.user_info.luna_birthday
            luna_birthday_tf.update()

        luna_birthday_tf_value = str4luna(self.user_info.luna_birthday)
        luna_birthday_tf = ft.TextField(label="生日(农历)",
                                        hint_text=self.default_luna_str(),
                                        helper_text="月份农历为1到12，闰月为负，即闰2月=-2。" if luna_birthday_tf_value is None else None,
                                        on_focus=lambda e: show_luna_number(),
                                        value=luna_birthday_tf_value, on_blur=lambda e: _setter(e))
        return luna_birthday_tf

    @staticmethod
    def default_luna_str():
        today_luna = Lunar.fromDate(datetime.now())
        year_luna = today_luna.getYear()
        month_luna = today_luna.getMonth()
        day_luna = today_luna.getDay()
        luna_str = f"格式: {year_luna}(可选)/{month_luna}/{day_luna}"
        return luna_str

    @user_luna_birthday.setter
    def user_luna_birthday(self, luna_birthday):
        self.user_info.luna_birthday = luna_birthday

    @property
    def user_address(self):
        def _setter(address):
            self.user_address = address.control.value

        return ft.TextField(label="地址(省市区)", value=self.user_info.address if self.user_info.address else "",
                            on_blur=lambda e: _setter(e))

    @user_address.setter
    def user_address(self, address):
        self.user_info.address = address

    @property
    def user_phone(self):
        def _setter(phone):
            self.user_phone = phone.control.value

        return ft.TextField(label="电话", value=self.user_info.phone if self.user_info.phone else "",
                            on_blur=lambda e: _setter(e))

    @user_phone.setter
    def user_phone(self, phone):
        self.user_info.phone = phone

    def build_user_form(self):
        """
        构建用户表单,
        """
        # options
        user_deleter = ft.ElevatedButton(text="删除用户", on_click=self.delete_user)
        user_deleter.visible = self.update_mode
        # 提交用户信息
        user_submitter = ft.ElevatedButton(text="Submit", on_click=self.submit_user)
        ft_form = ft.Column(horizontal_alignment=CrossAxisAlignment.CENTER,
                            controls=[self.user_avatar, self.user_nick_name, self.user_bilibili_id,
                                      self.user_birthday, self.user_luna_birthday, self.user_address, self.user_phone,
                                      # 删除用户
                                      user_deleter,
                                      user_submitter])
        return ft_form

    def delete_user(self, e):
        """
        删除用户
        """
        delete_user(self.user_info.id)
        self.app.close_end_drawer(e)

    def submit_user(self, e):
        """
        提交用户信息
        """
        if self.update_mode:
            # 如果用户存在, 则更新数据库中
            update_user(self.user_info)
        else:
            # 点击了新增用户, 用户信息可以添加
            insert_user(self.user_info)
        self.app.close_end_drawer(e)

    def fetch_user_bilibili_info(self, e):
        """
        从 Bilibili 链接拉取头像与昵称
        """
        m_user_id = e.data
        self.user_bilibili_id = int(m_user_id)
        token, _ = get_token()
        user_infos = get_user_details([m_user_id], session_data=str(token))
        if user_infos and len(user_infos) > 0:
            self.user_nick_name = user_infos[0][1]
            self.user_avatar = user_infos[0][2]
            self.content = self.build_user_form()
            self.update()
            return
        # TODO 提示用户 id 不存在
        print("用户 id 不存在")

    def handle_birthday_change(self, e):
        """
        处理日期选择器的变化
        """
        date_str = e.data.split("T")[0]
        if self.date_picker_mode == "birthday":
            self.user_info.birthday = date_str
            form = self.build_user_form(self.user_info)
            self.content = form
        else:
            self.user_info.luna_birthday = date_str
            form = self.build_user_form(self.user_info)
            self.content = form
        self.update()

    def open_date_picker(self, mode="birthday"):
        """
        打开日期选择器
        mode: birthday 公历日期
              luna_birthday 阴历日期

        """
        self.date_picker_mode = mode
        self.page.open(self.date_picker)
