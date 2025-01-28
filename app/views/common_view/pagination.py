import math

import flet as ft
from flet.core.control import Control


class Pagination(ft.Container):
    """
    分页组件
    """

    def __init__(self, page, app, row_getter, cols, page_size=10, total_count=0, *args, **kwargs):
        """
        初始化分页组件

        """
        super().__init__(*args, **kwargs)
        self.total_count = total_count
        self._current_page = 1
        self._page_size = page_size
        self._total_page_number = math.ceil(self.total_count / self._page_size)
        self.page = page
        self.app = app
        self.row_getter = row_getter
        page_ft = self.current_page
        self.next_button = ft.IconButton(
            icon=ft.Icons.ARROW_FORWARD,
            on_click=lambda e: self.page_change(page_ft, 1)
        )
        self.total_page_count = ft.Text(value=f"| {self._total_page_number}")
        # 数据展示列
        self.data_column = ft.DataTable(columns=cols)

        self.prev_button = ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            on_click=lambda e: self.page_change(page_ft, -1),
            disabled=True
        )
        self.content = ft.Column([
            ft.Container(
                self.data_column,
                border=ft.border.all(1, ft.Colors.GREY_400),
                padding=10
            ),
            ft.Row([
                self.prev_button,
                page_ft,
                self.total_page_count,
                self.next_button
            ],
                alignment=ft.MainAxisAlignment.CENTER)
        ])
        # 首次加载数据

    def did_mount(self):
        self.update_display()

    @property
    def page_size(self):
        return self._page_size

    @property
    def current_page(self):
        return ft.Text(value=f"{self._current_page}")

    def update_display(self):
        """更新数据显示"""
        # 清空当前显示
        self.data_column.rows.clear()
        # 计算分页位置
        start = (self._current_page - 1) * self._page_size
        end = min(start + self._page_size, self.total_count)

        # 添加新数据
        datas, total_count = self.row_getter(start, end)
        for item in datas:
            self.data_column.rows.append(item)
        # 更新页码显示
        self.total_count = total_count
        self._total_page_number = math.ceil(self.total_count / self._page_size)
        self.total_page_count.value = f"| {self._total_page_number}"
        self.prev_button.disabled = (int(self._current_page) == 1)
        self.next_button.disabled = (int(self._current_page) == self._total_page_number)
        self.update()

    # 分页控制按钮
    def page_change(self, control: Control, offset=1):
        """
        上一页
        """
        self._current_page += offset
        control.value = str(self._current_page)
        self.update_display()
