from typing import List
import datetime

import flet as ft
from flet.core.textfield import KeyboardType
from flet.core.types import MainAxisAlignment, CrossAxisAlignment

from app.assets.data_class import UserInfo
from app.pages.user_management import load_user_from_excel
from app.utils.daos.user_db import fetch_users, update_user, insert_user


class CaptainView(ft.Column):
    """
    Empty views
    There are none user's , upload from xlxs [UPLOAD]

    [Query By Name ][Query][Add][Upload]
    [All][2 Days][7 Days]
    +============================+
    |头像|名称|男/女| Edit       |
    +============================+
    """

    def __init__(self, page: ft.Page):
        super().__init__()
        self.expand = True
        self.page = page
        # 文件上传
        file_picker = ft.FilePicker(
            on_result=self.apply_captain_xlsx,
        )
        page.overlay.append(file_picker)
        self.file_list = ft.Row(alignment=ft.MainAxisAlignment.START)
        user_operations = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.OutlinedButton(
                    icon=ft.Icons.FIND_IN_PAGE_SHARP, on_click=self.find_by_name
                ),
                ft.OutlinedButton(icon=ft.Icons.ADD, on_click=self.add_user),
                ft.OutlinedButton(
                    icon=ft.Icons.UPLOAD,
                    on_click=lambda e: file_picker.pick_files(
                        allowed_extensions=["xlsx"]
                    ),
                ),
                self.file_list,
            ],
        )
        self.user_info = UserPanel(fetch_users())

        self.controls = [
            user_operations,
            ft.Divider(),
            ft.Markdown("### 舰长列表"),
            self.user_info,
        ]

    def apply_captain_xlsx(self, e):
        """
        展示文件名称,
        """
        file_path = ""
        for f in e.files:
            self.file_list.controls.append(ft.Text(f.name))
            file_path = f.path
        # 添加选择器
        self.file_list.controls.append(
            ft.OutlinedButton(
                text="覆盖",
                on_click=lambda e: self.save_captains(file_path, "override"),
            )
        )

        self.file_list.controls.append(
            ft.OutlinedButton(
                text="追加",
                on_click=lambda e: self.save_captains(file_path, "append"),
            )
        )
        self.update()

    def save_captains(self, file_path: str, mode="override"):
        load_user_from_excel(file_path, mode)
        self.update()

    def find_by_name(self, e):
        print(e)

    def add_user(self, e):
        user_adder = UserAdder(self.page, user_info=None)
        end_drawer = ft.NavigationDrawer(
            position=ft.NavigationDrawerPosition.END,
            controls=[user_adder],
        )

        self.page.open(end_drawer)

    def fetch_from_bilibili_url(self, e):
        print(e)


class UserPanel(ft.Container):
    def __init__(self, users: List[UserInfo]):
        super().__init__()
        self.users = users

        self.grid_view = ft.GridView(
            expand=True,
            runs_count=3,
            child_aspect_ratio=3,
            spacing=1,
            run_spacing=1,
        )
        self.content = self.grid_view

    def did_mount(self):
        # 在每次加载 panel 的时候, 查询用户信息
        self.users = fetch_users()
        ft.Row(
            controls=[
                ft.CircleAvatar(
                    foreground_image_src="https://i0.hdslb.com/bfs/face/7f704ecd473a4d933d51cd3e9356f78815fe1702.jpg@240w_240h_1c_1s_!web-avatar-nav.avif"
                ),
                ft.Text("test"),
            ]
        )
        user_cards = [
            ft.Card(
                content=render_user_card(u),
            )
            for u in self.users
        ]
        self.grid_view.controls = user_cards

        self.update()


class UserAdder(ft.Container):
    """用户添加 panel"""

    def __init__(self, page: ft.Page, user_info: UserInfo = None):
        super().__init__()
        self.padding = ft.padding.only(left=20, right=20, top=20, bottom=20)
        self.date_picker_mode = "birthday"
        self.page = page
        self.user_info = UserInfo() if not user_info else user_info
        self.date_picker = ft.DatePicker(
            first_date=datetime.datetime(year=2023, month=10, day=1),
            last_date=datetime.datetime(year=2025, month=10, day=1),
            date_picker_entry_mode=ft.DatePickerEntryMode.INPUT,
            on_change=lambda e: self.handle_change(e),
        )
        self.birthday = ft.ElevatedButton(
            self.user_info.birthday if self.user_info.birthday else "Setting Birthday",
            on_click=lambda e: self.open_date_picker(mode="birthday"),
        )
        self.luna_birthday = ft.ElevatedButton(
            self.birthday if self.user_info.luna_birthday else "Setting Luna Birthday",
            on_click=lambda e: self.open_date_picker(mode="luna_birthday"),
        )
        self.nick_name = ft.TextField(label="昵称", value=self.user_info.name if self.user_info.name else "")
        self.address = ft.TextField(label="地址", value=self.user_info.address if self.user_info.address else "")
        self.phone = ft.TextField(label="电话", value=self.user_info.phone if self.user_info.phone else "")
        self.content = ft.Column(
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                ft.CircleAvatar(background_image_src="", radius=30, max_radius=100),
                self.nick_name,
                self.birthday,
                self.luna_birthday,
                self.address,
                self.phone,
                ft.ElevatedButton(
                    text="从 Bilibili 链接拉取头像与昵称",
                    on_click=self.fetch_from_bilibili_url,
                ),
                ft.ElevatedButton(text="提交", on_click=self.submit_user),
            ],
        )

    def submit_user(self, e):
        self.user_info.name = self.nick_name.value
        self.user_info.address = self.address.value
        self.user_info.phone = self.phone.value
        print("submit user", self.user_info)
        if self.user_info.id:
            update_user(self.user_info)
        else:
            insert_user(self.user_info)


    def fetch_from_bilibili_url(self, e):
        """
        从 Bilibili 链接拉取头像与昵称
        """
        print(e)

    def handle_change(self, e):
        """
        处理日期选择器的变化
        """
        date_str = e.data.split("T")[0]
        if self.date_picker_mode == "birthday":
            self.birthday.text = date_str
            self.user_info.birthday = date_str
            self.birthday.update()
        else:
            self.luna_birthday.text = date_str
            self.user_info.luna_birthday = date_str
            self.luna_birthday.update()

    def open_date_picker(self, mode="birthday"):
        self.date_picker_mode = mode
        self.page.open(self.date_picker)


def render_user_card(user: UserInfo):
    return ft.Row(
        alignment=MainAxisAlignment.START,
        vertical_alignment=CrossAxisAlignment.CENTER,
        controls=[
            ft.CircleAvatar(
                radius=25,
                max_radius=200,
                foreground_image_src="https://i0.hdslb.com/bfs/face/7f704ecd473a4d933d51cd3e9356f78815fe1702.jpg@240w_240h_1c_1s_!web-avatar-nav.avif",
            ),
            ft.Column(
                alignment=MainAxisAlignment.CENTER,
                controls=[ft.Text(user.name), ft.Text(user.birthday)],
            ),
        ],
    )
