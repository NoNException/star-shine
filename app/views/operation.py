import flet as ft


class OperationPanel(ft.Column):
    """
    Empty views
    There are none user's , upload from xlxs [UPLOAD]

    [Qeruy By Name ][Query][Add]
    [All][2 Days][7 Days]
    +============================+
    |头像|名称|男/女| Edit       |
    +============================+
    """

    def __init__(self):
        super().__init__()
        self.name_query = ft.TextField(hint_text="Query By Name", expand=True)
        self.width = 400
        user_options = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.name_query,
                ft.OutlinedButton(
                    icon=ft.Icons.FIND_IN_PAGE_SHARP, on_click=self.find_by_name
                ),
                ft.OutlinedButton(icon=ft.Icons.ADD),
                ft.OutlinedButton(icon=ft.Icons.UPLOAD),
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
        self.controls = [user_options, user_info]

    def find_by_name(self, e):
        print("a")
