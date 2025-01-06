import flet as ft
from app.views.navigation import SideBar
from app.views.operation import OperationPanel
from app.views.info_panel import InfoPanel


class AppLayout(ft.Row):
    def __init__(self, app, page: ft.Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page: ft.Page = page
        self.app = app
        # 左侧导航栏
        self.nav_bar = SideBar(app, page)
        # 中间操作栏
        self.operation_panel = OperationPanel()
        # 右侧信息栏
        self.info_panel = InfoPanel()
        self.expand = True

        self._active_view: ft.Control = ft.Row()
        # 布局设置
        self.controls = [self.nav_bar, ft.VerticalDivider(width=2), self._active_view]

    @property
    def active_view(self):
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        print("view.....")
        self.controls[-1] = self._active_view
        self.update()

    def set_captain_view(self):
        print("???????")
        self.active_view = ft.Row([ft.Text("Captain Views")])
        self.nav_bar.selected_index = 0
        self.nav_bar.update()
        self.page.update()

    def set_revenue_view(self):
        self.active_view = ft.Row([ft.Text("Revenue Views")])
        self.nav_bar.selected_index = 0
        self.nav_bar.update()
        self.page.update()

    def set_note_view(self):
        self.active_view = ft.Row([ft.Text("Note View")])
        self.nav_bar.selected_index = 0
        self.nav_bar.update()
        self.page.update()
