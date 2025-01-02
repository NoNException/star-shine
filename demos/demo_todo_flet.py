import flet as ft


class TodoApp(ft.Column):
    """可充用的 APP CLASS"""

    def __init__(self):
        super().__init__()
        self.new_task = ft.TextField(hint_text="What's need to be done?", expand=True)
        self.items_left = ft.Text("0 items left.")
        self.tasks = ft.Column()
        self.width = 600
        self.filter = ft.Tabs(
            selected_index=0,
            on_change=self.tabs_change,
            tabs=[ft.Tab(text="all"), ft.Tab(text="active"), ft.Tab(text="completed")],
        )
        self.controls = [
            ft.Row(
                controls=[
                    self.new_task,
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD, on_click=self.add_clicked
                    ),
                ],
            ),
            ft.Column(
                spacing=25,
                controls=[
                    self.filter,
                    self.tasks,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.items_left,
                            ft.OutlinedButton(
                                text="Clear completed", on_click=self.clear_clicked
                            ),
                        ],
                    ),
                ],
            ),
        ]

    def clear_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.completed:
                self.task_delete(task)

    def before_update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task in self.tasks.controls:
            task.visible = (
                status == "all"
                or (status == "active" and not task.completed)
                or (status == "completed" and task.completed)
            )
            if not task.completed:
                count += 1
        self.items_left.value = f"{count} items left."

    def tabs_change(self, e):
        self.update()

    def task_status_change(self):
        self.update()

    def add_clicked(self, e):
        task = Task(
            self.new_task.value,
            self.task_status_change,
            self.task_delete,
        )
        self.tasks.controls.append(task)
        self.new_task.value = ""
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()


class Task(ft.Column):
    def __init__(self, task_name, task_status_change, task_delete):
        super().__init__()
        self.completed = False
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete
        # 展示名称
        self.display_task = ft.Checkbox(
            value=False, label=self.task_name, on_change=self.status_changed
        )
        self.edit_name = ft.TextField(expand=True)

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.CREATE_OUTLINED,
                            tooltip="Edit To-Do",
                            on_click=self.edit_cliked,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINED,
                            tooltip="Delete Task",
                            on_click=self.delete_cliked,
                        ),
                    ],
                ),
            ],
        )
        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.Icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.Colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )
        self.controls = [self.display_view, self.edit_view]

    def status_changed(self, e):
        self.completed = self.display_task.value
        self.task_status_change()

    def edit_cliked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def delete_cliked(self, e):
        self.task_delete(self)


def main(main_page: ft.Page):
    main_page.title = "To-Do App"
    main_page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    main_page.update()
    todo = TodoApp()
    main_page.add(todo)


if __name__ == "__main__":
    ft.app(main)
