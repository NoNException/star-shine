from typing import List
import datetime

import flet as ft
from flet.core.types import MainAxisAlignment, CrossAxisAlignment

from app.assets.data_class import UserInfo
from app.service.captain_service import user_to_birthday, load_user_from_excel
from app.utils.bilibili_apis.user_info_fetcher import get_user_details
from app.utils.daos.login_db import get_token
from app.utils.daos.user_db import fetch_users, update_user, insert_user, delete_user


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

        def handle_submit(e):
            print(f"handle_submit e.data: {e.data}")

        def handle_tap(e):
            self.user_search.open_view()

        self.user_search_lv = ft.ListView(controls=self.query_base_user())
        self.user_search = ft.SearchBar(
            view_elevation=4,
            bar_hint_text="Search Users...",
            view_hint_text="Choose a user from the suggestions...",
            on_change=self.handle_change,
            on_submit=handle_submit,
            on_tap=handle_tap,
            controls=[self.user_search_lv]
        )

        user_operations = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.user_search,
                ft.CupertinoButton(icon=ft.Icons.ADD, on_click=self.open_user_panel),
                ft.CupertinoButton(
                    icon=ft.Icons.UPLOAD,
                    on_click=lambda e: file_picker.pick_files(
                        allowed_extensions=["xlsx"]
                    ),
                ),
                self.file_list,
            ],
        )
        self.user_info_drawer = ft.NavigationDrawer(
            position=ft.NavigationDrawerPosition.END,
            controls=[UserAdder(self, self.page, user_info=None)],
        )
        self.user_list = UserList(self, fetch_users(query_all=True))

        self.user_filter = ft.Tabs(selected_index=0, on_change=self.apply_tabs_change,
                                   tabs=[ft.Tab(text="All"), ft.Tab(text="3Days"), ft.Tab(text="7Days"),
                                         ft.Tab(text="In Months")]
                                   )
        self.controls = [
            user_operations,
            ft.Divider(),
            self.user_filter,
            self.user_list,
        ]

    # User Search Actions
    def close_anchor(self, e):
        """
        关闭抽屉
        """
        user: UserInfo = e.control.data
        self.user_list.apply_filter(users=[user])
        self.user_search.bar_hint_text = user.name
        self.user_search.close_view()

    def handle_change(self, e):
        user_name = e.data
        users = fetch_users(fuzz_query=user_name, query_all=True)
        final_list = [ft.ListTile(title=ft.Text(f"{u.name}"), on_click=self.close_anchor, data=u) for u in users]
        final_list.append(ft.ListTile(title=ft.Text("Clear..."), on_click=self.clear_search, data=None))
        self.user_search_lv.controls.clear()
        for f in final_list:
            self.user_search_lv.controls.append(f)
        self.user_search_lv.update()

    def clear_search(self, e):
        """
        清除搜索框
        """
        self.user_search.bar_hint_text = "Search Users..."
        self.user_filter.selected_index = 0
        self.user_search.close_view()
        self.user_list.apply_filter(fileter_name="")
        self.user_filter.update()

    def query_base_user(self):
        users = fetch_users(order_by="name", desc=True, limit=7)
        final_list = [ft.ListTile(title=ft.Text(f"{u.name}"), on_click=self.close_anchor, data=u) for u in users]
        final_list.append(ft.ListTile(title=ft.Text("Clear..."), on_click=self.clear_search, data=None))
        return final_list

    # User filter Actions
    def apply_tabs_change(self, e):
        """
        应用 filter , 筛选用户
        :param e:
        """
        filter_name = self.user_filter.tabs[self.user_filter.selected_index].text
        self.user_list.apply_filter(filter_name)

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
                on_click=lambda e: self.batch_save_captains(file_path, "override"),
            )
        )

        self.file_list.controls.append(
            ft.OutlinedButton(
                text="追加",
                on_click=lambda e: self.batch_save_captains(file_path, "append"),
            )
        )
        self.update()

    def batch_save_captains(self, file_path: str, mode="override"):
        load_user_from_excel(file_path, mode)
        self.update()

    def open_user_panel(self, e, user_info: UserInfo = None):
        """
        添加/修改用户
        """
        if user_info:
            self.user_info_drawer.controls = [UserAdder(self, self.page, user_info=user_info)]
        else:
            self.user_info_drawer.controls = [UserAdder(self, self.page)]
        self.page.open(self.user_info_drawer)

    def close_end_drawer(self, e):
        """
        关闭抽屉
        """
        self.user_info_drawer.controls = [UserAdder(self, self.page)]
        self.page.close(self.user_info_drawer)


class UserList(ft.Container):
    """
    用户列表
    """

    def __init__(self, app: CaptainView, users: List[UserInfo]):
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


class UserAdder(ft.Container):
    """用户添加 panel"""

    def __init__(self, app: CaptainView, page: ft.Page, user_info: UserInfo = None):
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
