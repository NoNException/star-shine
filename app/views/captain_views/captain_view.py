import flet as ft

from app.assets.data_class import UserInfo
from app.service.captain_service import load_user_from_excel
from app.utils.daos.user_db import fetch_users
from app.views.captain_views.captain_lister import UserListView
from app.views.captain_views.captain_modifier import UserAdder


class CaptainUserView(ft.Column):
    """
    Captain User View
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
        self.user_list = UserListView(self, fetch_users(query_all=True))

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


