from fastapi import background
import flet as ft
import os
from app.pages.user_management import load_user_from_excel
from app.utils.daos.file_handler import read_uploaded_file


class CaptainView(ft.Column):
    """
    Empty views
    There are none user's , upload from xlxs [UPLOAD]

    [Query By Name ][Query][Add][Upload]
    [All][2 Days][7 Days]
    +============================+
    |头像|名称|男/女| Edit       |
    +============================+
    """

    def __init__(self, page: ft.Page):
        super().__init__()
        self.expand = True
        # 文件上传
        file_picker = ft.FilePicker(
            on_result=self.apply_captain_xlsx,
        )
        page.overlay.append(file_picker)
        self.file_list = ft.Row(alignment=ft.MainAxisAlignment.START)
        user_operations = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.OutlinedButton(
                    icon=ft.Icons.FIND_IN_PAGE_SHARP, on_click=self.find_by_name
                ),
                ft.OutlinedButton(icon=ft.Icons.ADD),
                ft.OutlinedButton(
                    icon=ft.Icons.UPLOAD,
                    on_click=lambda e: file_picker.pick_files(
                        allowed_extensions=["xlsx"]
                    ),
                ),
                self.file_list,
            ],
        )
        user_info = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("头像"),
                ft.Text("名称"),
                ft.Text("性别"),
                ft.OutlinedButton(icon=ft.Icons.EDIT),
            ],
        )

        self.controls = [
            user_operations,
            ft.Divider(),
            ft.Markdown("### 用户列表"),
            user_info,
        ]

    def apply_captain_xlsx(self, e):
        """
        展示文件名称
        """
        file_path = ""
        for f in e.files:
            self.file_list.controls.append(ft.Text(f.name))
            print(f)
            print("+-+")
            file_path = f.path
        # 添加选择器
        self.file_list.controls.append(
            ft.OutlinedButton(
                text="覆盖",
                on_click=lambda e: self.save_captains(file_path, "override"),
            )
        )

        self.file_list.controls.append(
            ft.OutlinedButton(
                text="追加",
                on_click=lambda e: self.save_captains(file_path, "append"),
            )
        )
        self.update()

    def save_captains(self, file_path: str, mode="override"):
        load_user_from_excel(file_path, mode)
        self.update()

    def find_by_name(self, e):
        print("a")
