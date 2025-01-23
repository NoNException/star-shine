import datetime

import flet as ft
from flet.core.types import CrossAxisAlignment

from app.assets.data_class import UserInfo
from app.utils.bilibili_apis.user_info_fetcher import get_user_details
from app.utils.daos.login_db import get_token
from app.utils.daos.user_db import delete_user, update_user, insert_user


class UserAdder(ft.Container):
    """用户添加 panel"""

    def __init__(self, app, page: ft.Page, user_info: UserInfo = None):
        super().__init__()
        self.padding = ft.padding.only(left=20, right=20, top=20, bottom=20)
        self.date_picker_mode = "birthday"
        self.page = page
        self.app = app
        self.update_mode = user_info is not None
        self.date_picker = ft.DatePicker(
            first_date=datetime.datetime(year=2023, month=10, day=1),
            last_date=datetime.datetime(year=2025, month=10, day=1),
            date_picker_entry_mode=ft.DatePickerEntryMode.INPUT,
            on_change=lambda e: self.handle_birthday_change(e),
        )


        self.user_info = user_info if user_info else UserInfo()
        self.m_user_id = ft.TextField(label="MID")
        self.bilibili_sync_sub = ft.ElevatedButton(text='从 BiliBili 同步',
                                                   on_click=lambda e: self.fetch_user_bilibili_info())
        user_form = self.build_user_form(self.user_info)
        # 是否是更新模式, 更新模式下, 支持用户删除
        self.content = user_form

    def build_user_form(self, user_info: UserInfo):
        """
        构建用户表单,
        """
        # options
        user_deleter = ft.ElevatedButton(text="删除用户", on_click=self.delete_user)
        user_deleter.visible = self.update_mode
        # 获取用户信息

        bilibili_form = ft.Column([self.m_user_id, self.bilibili_sync_sub])

        # 提交用户信息
        user_submitter = ft.ElevatedButton(text="Submit", on_click=self.submit_user)

        # data's
        avatar = ft.CircleAvatar(background_image_src=user_info.avatar_url, radius=30, max_radius=100)
        nick_name = ft.TextField(label="昵称", value=user_info.name if user_info.name else "")
        address = ft.TextField(label="地址", value=user_info.address if user_info.address else "")
        phone = ft.TextField(label="电话", value=user_info.phone if user_info.phone else "")
        birthday = ft.TextButton(
            user_info.birthday if user_info.birthday else "Setting Birthday",
            on_click=lambda e: self.open_date_picker(mode="birthday"),
        )
        luna_birthday = ft.TextButton(
            user_info.birthday if user_info.luna_birthday else "Setting Luna Birthday",
            on_click=lambda e: self.open_date_picker(mode="luna_birthday"),
        )
        ft_form = ft.Column(horizontal_alignment=CrossAxisAlignment.CENTER,
                            controls=[avatar, birthday, luna_birthday, nick_name, address, phone,
                                      # 删除用户
                                      user_deleter,
                                      bilibili_form,
                                      user_submitter])
        return ft_form

    def delete_user(self, e):
        """
        删除用户
        """
        print(self.user_info)
        delete_user(self.user_info.id)
        self.app.close_end_drawer(e)

    def submit_user(self, e):
        """
        提交用户信息
        """
        self.user_info.avatar_url = self.content.controls[0].background_image_src
        print(self.content.controls[0], "?????")
        self.user_info.birthday = self.content.controls[1].text
        self.user_info.luna_birthday = self.content.controls[2].text
        self.user_info.name = self.content.controls[3].value
        self.user_info.address = self.content.controls[4].value
        self.user_info.phone = self.content.controls[5].value
        if self.update_mode:
            # 如果用户存在, 则更新数据库中
            update_user(self.user_info)
        else:
            # 点击了新增用户, 用户信息可以添加
            insert_user(self.user_info)
        self.app.close_end_drawer(e)

    def fetch_user_bilibili_info(self, ):
        """
        从 Bilibili 链接拉取头像与昵称
        """
        m_user_id = str(self.m_user_id.value)
        self.user_info.bilibili_user_id = int(m_user_id)
        token, _ = get_token()
        user_infos = get_user_details([m_user_id], session_data=str(token))
        if user_infos and len(user_infos) > 0:
            self.user_info.name = user_infos[0][1]
            self.user_info.avatar_url = user_infos[0][2]
            self.content = self.build_user_form(self.user_info)
            self.update()
            return
        # 提示用户 id 不存在
        print("用户 id 不存在")
        # self.page.open()

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
