from typing import List

import flet as ft
from flet.core.types import MainAxisAlignment, CrossAxisAlignment

from app.assets.data_class import UserInfo
from app.service.captain_service import user_to_birthday
from app.utils.daos.user_db import fetch_users


class UserListView(ft.Container):
    """
    用户列表
    """

    def __init__(self, app, users: List[UserInfo]):
        super().__init__()
        self.users = users
        self.app = app
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
        self.users = fetch_users(query_all=True)
        self.grid_view.controls = self.user_card_builder(self.users)

    def apply_filter(self, fileter_name=None, users: list[UserInfo] = None):
        if not users or len(users) == 0:
            day_filter_map = {
                "3Days": 3, "7Days": 7, "In Months": 30
            }
            users = user_to_birthday(day_filter_map[fileter_name]) if fileter_name in day_filter_map.keys() \
                else fetch_users(query_all=True)
        self.grid_view.controls = self.user_card_builder(users)
        self.update()

    def user_card_builder(self, users: List[UserInfo]) -> List[ft.Card]:
        """
        构建用户卡片
        :param users: 用户列表
        :return: List[ft.Card]
        """
        user_cards = [
            ft.Card(content=self.render_user_card(u), ) for u in users
        ]
        return user_cards

    def render_user_card(self, user: UserInfo):
        """
        渲染用户卡片
        """
        return ft.Row(
            alignment=MainAxisAlignment.START,
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                ft.CircleAvatar(radius=25,
                                max_radius=200,
                                foreground_image_src=user.avatar_url,
                                ),
                ft.Column(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[ft.Text(user.name), ft.Text(user.birthday)],
                ),
                ft.TextButton(text="修改", on_click=lambda e: self.app.open_user_panel(e, user)),
            ],
        )
