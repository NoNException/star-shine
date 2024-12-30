import flet as ft


class OperationPanel(ft.Column):
    def __init__(self):
        super().__init__()
        self.spacing = 20

        # 操作栏标题
        self.controls.append(ft.Text("操作面板", size=20, weight=ft.FontWeight.BOLD))

        # 输入框和按钮
        self.controls.append(ft.TextField(label="姓名", width=300))
        self.controls.append(ft.TextField(label="年龄", width=300))
        self.controls.append(ft.ElevatedButton(text="提交", on_click=self.submit_form))

    def submit_form(self, e):
        print("提交数据成功！")
