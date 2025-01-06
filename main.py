import flet as ft
from app.views.app_layout import AppLayout


class StarShine(AppLayout):
    def __init__(self, page: ft.Page):
        self.page = page
        self.view_map = {
            "/captains": self.set_captain_view,
            "/revenues": self.set_revenue_view,
            "/notes": self.set_note_view,
        }
        self.page.on_route_change = self.route_chage
        super().__init__(self, self.page)

    def route_chage(self, index):
        troute = ft.TemplateRoute(self.page.route)

        print(f"On route_chage..{troute.route}")
        for k, v in self.view_map.items():
            print(k)
            if troute.match(k):
                print(k)
                v()
        self.page.update()


def main(page: ft.Page):
    page.adaptive = True
    # 设置页面标题和布局
    page.title = "Star Shine"
    # page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    # page.vertical_alignment = ft.MainAxisAlignment.START
    # page.padding = 10

    # 加载主页
    home_page = StarShine(page)
    page.add(home_page)
    # 运行应用
    page.update()


# 启动应用
ft.app(target=main)
