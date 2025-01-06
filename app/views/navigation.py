import flet as ft


class SideBar(ft.NavigationRail):
    def __init__(self, app, page: ft.Page):
        super().__init__()
        self.page: ft.Page = page
        self.app = app
        self.min_width = 100
        self.group_alignment = -1
        # 默认选中第一个菜单项
        self.selected_index = 0
        # 设置导航项
        self.destinations = [
            ft.NavigationRailDestination(
                icon=ft.Icons.PEOPLE,
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.NOTES_ROUNDED,
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.COLLECTIONS,
            ),
        ]

        # 注册事件处理
        self.on_change = self.on_nav_change

    def on_nav_change(self, e):
        index = e.control.selected_index
        self.update()
        if index == 0:
            self.page.route = "/captains"
        elif index == 1:
            self.page.route = "/revenues"
        elif index == 2:
            self.page.route = "/notes"
        self.page.update()
