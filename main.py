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
        self.page.on_route_change = self.route_change
        super().__init__(self, page)

    def route_change(self, index):
        template_route = ft.TemplateRoute(self.page.route)

        print(f"On route_change..{template_route.route}")
        for k, v in self.view_map.items():
            if template_route.match(k):
                v()
        self.page.update()


def command(e, page):
    if e.data == "--r":
        page


def main(page: ft.Page):
    # 设置页面标题和布局
    page.title = "Star Shine"
    page.theme_mode = ft.ThemeMode.SYSTEM
    # page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    # page.vertical_alignment = ft.MainAxisAlignment.START
    # page.padding = 10

    # 加载主页
    home_page = StarShine(page)
    page.add(home_page,
             ft.TextField(label="Command Panel", on_submit=lambda e: command(e, page)))
    # 运行应用
    page.update()


if __name__ == '__main__':
    # 启动应用
    ft.app(target=main)
