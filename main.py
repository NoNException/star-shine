import flet as ft
from app.views.home_page import HomePage
from flet import Theme


def main(page: ft.Page):
    page.adaptive = True
    # 设置页面标题和布局
    page.title = "Star Shine"
    # page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    # page.vertical_alignment = ft.MainAxisAlignment.START
    # page.padding = 10

    # 加载主页
    home_page = HomePage(page)
    page.add(home_page)
    # 运行应用
    page.update()


# 启动应用
ft.app(target=main)
