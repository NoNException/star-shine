"""
revenue 列表同步视图
"""

import flet as ft


class RevenueSyncView(ft.AlertDialog):
    def __init__(self, page, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.parent = parent
        # if self.filters can't query any revenues, show's bilibili query dialog
        self.sync_start_time = ft.TextField(label="Start Time")
        self.sync_end_time = ft.TextField(label="End Time")
