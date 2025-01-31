"""
revenue 列表同步视图,
同步功能, 同步进度显示功能
"""
import time
from calendar import month
from datetime import datetime, timedelta

import flet as ft

from app.service.revenue_service import days_gap, bilibili_sync
from app.utils.app_utils.common_utils import app_log


class RevenueSyncView(ft.AlertDialog):
    def __init__(self, page, parent, miss_day_number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.parent = parent
        self.miss_days = miss_day_number - 1
        self.day_range = []
        # if self.filters can't query any revenues, show's bilibili query dialog

        self.picker = ft.DatePicker()
        self.start_time = ft.TextField(label="开始时间", on_click=lambda e: self.open_time_picker(e))
        self.end_time = ft.TextField(label="结束时间", on_click=lambda e: self.open_time_picker(e))
        self.start_sync_eb = ft.ElevatedButton("开始同步", on_click=self.start_sync, visible=False)
        self.chips_panel = ft.Row(wrap=True, width=self.page.width / 1.5)
        self.progress_bar = ft.ProgressBar(value=0, visible=False)
        self.finish_controls = ft.Column(controls=[ft.Text("同步完毕!", color=ft.colors.GREEN),
                                                   ft.OutlinedButton(on_click=lambda ee: self.close_this(),
                                                                     text="关闭")], visible=False)
        self.content_controls = ft.Column([
            self.start_time,
            self.end_time,
            self.start_sync_eb,
            self.progress_bar,
            self.chips_panel,
            self.finish_controls
        ])
        self.content = self.content_controls

    def did_mount(self):
        self.progress_bar.value = 0
        self.progress_bar.visible = False

    def clean_controllers(self):
        self.start_time.value = ""
        self.end_time.value = ""
        self.start_time.disabled = False
        self.end_time.disabled = False
        self.progress_bar.value = 0
        self.progress_bar.visible = False
        self.finish_controls.visible = False
        self.chips_panel.clean()

    def open_time_picker(self, e):
        """
        打开时间选择器
        开始时间是默认的
        结束时间是昨天
        """
        # 获得昨天的日期
        first_day = datetime.now() - timedelta(days=self.miss_days)
        end_day = datetime.now() - timedelta(days=1)

        def handle_change(de):
            date_time_choose = de.control.value
            e.control.value = date_time_choose.strftime("%Y-%m-%d")
            e.control.disabled = True
            e.control.update()
            start_time_str = self.start_time.value
            end_time_str = self.end_time.value

            if start_time_str != "" and end_time_str != "":
                # 渲染 chips
                start_date = datetime.strptime(start_time_str, "%Y-%m-%d")
                end_date = datetime.strptime(end_time_str, "%Y-%m-%d")
                self.render_chips(start_date, end_date)

            self.page.close(self.picker)

        if self.start_time.value is not None and self.start_time.value != "":
            first_day = datetime.strptime(self.start_time.value, "%Y-%m-%d")

        self.picker = ft.DatePicker(first_date=datetime(year=first_day.year, month=first_day.month, day=first_day.day),
                                    value=datetime(year=first_day.year, month=first_day.month, day=first_day.day),
                                    last_date=datetime(year=end_day.year, month=end_day.month, day=end_day.day),
                                    on_change=handle_change)
        self.page.open(self.picker)

    @app_log
    def render_chips(self, start_time, end_time):
        """
        同步数据
        :param start_time: 开始时间, date 对象
        :param end_time: 结束时间, date 对象
        """
        # Chip用来展示同步过程中的状态提示
        self.day_range = days_gap(start_time, end_time)
        self.chips_panel.controls.clear()
        # 按照天数, 初始化对应数量的 chip
        reversed_day_range = list(reversed(self.day_range))
        for index, day in enumerate(reversed_day_range):
            day_str = day.strftime("%m-%d")

            day_chip = ft.Chip(
                label=ft.Text(day_str),
                width=self.page.width / 1.5 / 5,
                leading=ft.Icon(ft.Icons.CHECK_BOX_OUTLINE_BLANK),
            )
            self.chips_panel.controls.append(day_chip)
            # 每次更新都需要调用 page.update() 让UI实时刷新
        self.progress_bar.visible = True
        # 显示同步按钮
        self.start_sync_eb.visible = True
        self.update()

    def start_sync(self, e):
        total_len = len(self.day_range)
        reversed_day_range = list(reversed(self.day_range))

        def update_chip(chip_index):
            chip = self.chips_panel.controls[chip_index]
            # 更新状态为绿色
            chip.bgcolor = ft.Colors.GREEN
            chip.leading = ft.Icon(ft.Icons.CHECK_BOX)
            chip.update()
            time.sleep(0.3)
            # 更新进度条
            self.progress_bar.value = (chip_index + 1) / total_len
            self.progress_bar.update()

        for index, day in enumerate(reversed_day_range):
            bilibili_sync(day, update_chip(index))

        self.finish_controls.visible = True

        self.content_controls.update()

    def close_this(self):
        self.page.close(self)
