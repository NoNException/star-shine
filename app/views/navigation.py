import flet as ft


class NavigationRailPanel(ft.NavigationRail):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.min_width = 100
        self.min_extended_width = 100
        self.group_alignment = -1
        # 默认选中第一个菜单项
        self.selected_index = 0
        # 设置导航项
        self.destinations = [
            ft.NavigationRailDestination(
                icon=ft.Icons.HOME,
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.PEOPLE,
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS,
            ),
        ]

        # 注册事件处理
        self.on_change = lambda ie: self.on_nav_change(ie)

    def on_nav_change(self, e):
        return print("Selected destination:", e.control.selected_index)
