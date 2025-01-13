import flet as ft
from flet.core.textfield import TextField

from app.views.navigation import SideBar
from app.views.captain_view import CaptainView
from app.views.info_panel import InfoPanel
from app.views.revenue_view import RevenueListPage


class AppLayout(ft.Row):
    def __init__(self, app, page: ft.Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page: ft.Page = page
        self.app = app
        # 左侧导航栏
        self.nav_bar = SideBar(app, page)
        # 中间操作栏
        self.captain_view = CaptainView(page)
        self.revenue_view = RevenueListPage(page)
        # 右侧信息栏
        self.expand = True
        self._active_view: ft.Control = self.captain_view
        # 布局设置
        self.controls = [self.nav_bar, ft.VerticalDivider(width=2), self._active_view
                         ]

    @property
    def active_view(self):
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.controls[-1] = self._active_view
        self.update()

    def set_captain_view(self):
        self.active_view = self.captain_view
        self.nav_bar.selected_index = 0
        self.nav_bar.update()
        self.page.update()

    def set_revenue_view(self):
        self.active_view = self.revenue_view
        self.nav_bar.selected_index = 1
        self.nav_bar.update()
        self.page.update()

    def set_note_view(self):
        self.active_view = ft.Row([ft.Text("Note View")])
        self.nav_bar.selected_index = 2
        self.nav_bar.update()
        self.page.update()
