import flet as ft


class InfoPanel(ft.Column):
    def __init__(self):
        super().__init__()
        self.spacing = 10

        # 信息栏标题
        self.controls.append(ft.Text("信息栏", size=20, weight=ft.FontWeight.BOLD))

        # 模拟信息展示
        self.controls.append(ft.Text("用户: 张三"))
        self.controls.append(ft.Text("生日: 1998-02-15"))
        self.controls.append(ft.Text("状态: 活跃"))
