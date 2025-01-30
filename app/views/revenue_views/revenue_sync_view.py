"""
revenue 列表同步视图,
同步功能, 同步进度显示功能
"""
from datetime import datetime, timedelta

import flet as ft

from app.service.revenue_service import days_gap


class RevenueSyncView(ft.AlertDialog):
    def __init__(self, page, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.parent = parent
        # if self.filters can't query any revenues, show's bilibili query dialog
        self.sync_latest_current_month_eb = ft.ElevatedButton("同步本月",
                                                              on_click=lambda e: self.sync_latest_current_month(e))
        self.sync_latest_30_eb = ft.ElevatedButton("同步最近30天", on_click=self.sync_latest_30)
        self.content = ft.Column([
            self.sync_latest_current_month_eb, self.sync_latest_30_eb
        ])
        self.progress_bar = ft.ProgressBar(value=0, width=200)

    def did_mount(self):
        self.progress_bar.value = 0

    def sync_latest_current_month(self, e):
        # 获得月初到昨天的时间点
        start_time = datetime(datetime.now().year, datetime.now().month, 1)
        end_time = datetime.now() - timedelta(days=1)
        self.sync_data(start_time, end_time)

    def sync_latest_30(self, e):
        # 获得最近30天的时间点
        start_time = datetime.now() - timedelta(days=30)
        end_time = datetime.now() - timedelta(days=1)
        self.sync_data(start_time, end_time)

    def sync_data(self, start_time, end_time):
        """
        同步数据
        :param start_time: 开始时间, date 对象
        :param end_time: 结束时间, date 对象
        """
        # Chip用来展示同步过程中的状态提示
        days = days_gap(start_time, end_time)
        # 按照天数, 初始化对应数量的 chip
        for index, day in enumerate(days):
            day_str = day.strftime("%Y-%m-%d")
            day_chip = ft.Chip(
                label=ft.Text(day_str),
                color=ft.colors.WHITE,
                bgcolor=ft.colors.BLUE,
            )
            self.progress_bar.value = (index + 1) / len(days)
            # 更新Chip文案
            day_chip.text = f"已同步第 {index + 1}/{len(days)} 页数据"
            # 每次更新都需要调用 page.update() 让UI实时刷新

        # 全部同步结束后再提示
        day_chip.text = "同步完成"
