import flet as ft
from app.views.navigation import NavigationRailPanel
from app.views.operation import OperationPanel
from app.views.info_panel import InfoPanel


class HomePage(ft.Row):
    def __init__(self, page):
        super().__init__()

        # 左侧导航栏
        self.nav_bar = NavigationRailPanel(page)
        # 中间操作栏
        self.operation_panel = OperationPanel()
        # 右侧信息栏
        self.info_panel = InfoPanel()
        self.expand = True

        # 布局设置
        self.controls = [
            ft.Container(self.nav_bar),
            ft.VerticalDivider(width=2),
            ft.Column(
                controls=[
                    ft.Container(self.operation_panel, expand=1),
                ],
            ),
            ft.Container(self.info_panel, width=300),
        ]
