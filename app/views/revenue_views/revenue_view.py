"""
# 收益列表
# 2. Revenue List Page
# 3. Save Revenue into db if user's token is valid
"""
import time
from cProfile import label
from itertools import count
from urllib.parse import quote

import flet as ft

from app.assets.data_class import Revenue
from app.service.revenue_service import bilibili_sync
from app.utils.app_utils.common_utils import uuid_getter
from app.utils.app_utils.excel_utils import write_to_excel
from app.utils.daos.login_db import save_token
from app.service.bilibili_login_service import parse_login_url, poll_qr_code, generate_qr_code, is_user_need_login
from app.utils.daos.revenue_db import query_revenues, query_miss_days
from app.views.common_view.pagination import Pagination
from app.views.revenue_views.revenue_sync_view import RevenueSyncView


def to_data_cell(revenue: Revenue):
    """
    将数据转换为DataCell

    Args:
        revenue (Revenue): _description_
    Return:
        将用户信息
    """
    print(revenue)
    return ft.DataRow(
        cells=[
            ft.DataCell(ft.Text(revenue.uname)),
            ft.DataCell(ft.Text(revenue.time)),
            ft.DataCell(ft.Text(f"{revenue.gift_num}/{revenue.gift_name}")),
            ft.DataCell(ft.Text(revenue.gold)),
        ],
    )


class RevenueListPage(ft.Container):
    """
    扫码对话框
    """

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.login_dialog = BilibiliLoginDialog(self, page)
        self.page.overlay.append(self.login_dialog)
        # # 收益列表

        self.filters = ft.Row(controls=[
            ft.TextField(label="舰长", width=200),
            ft.TextField(label="时间(S)", width=200),
            ft.TextField(label="时间(E)", width=200),
            ft.TextField(label="收益(S)", width=200),
            ft.TextField(label="收益(E)", width=200),
        ])
        # if self.filters can't query any revenues, show's bilibili query dialog
        self.sync_start_time = ft.TextField(label="Start Time")
        self.sync_end_time = ft.TextField(label="End Time")

        def clear_filters():
            for f in self.filters.controls:
                f.value = ''
            self.query_revenue()

        cols = [
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Time")),
            ft.DataColumn(ft.Text("Gift")),
            ft.DataColumn(ft.Text("Golds"), numeric=True),
        ]
        _, total_count = self.query_revenue()
        self.revenue_list = Pagination(page, app=None, row_getter=self.query_revenue, cols=cols,
                                       total_count=total_count)
        self.sync_bt = ft.OutlinedButton(text="同步", on_click=lambda e: self.open_revenue_sync_dialog())
        self.sync_dialog = RevenueSyncView(page, self)
        self.content = ft.Column(controls=[
            self.filters,
            ft.Row(controls=[
                ft.OutlinedButton("导出", on_click=lambda e: self.revenue_export()),
                self.sync_bt,
                ft.OutlinedButton("查询", on_click=lambda e: self.query_revenue()),
                ft.OutlinedButton("重置", on_click=lambda e: clear_filters())
            ]),
            self.revenue_list
        ])

    def did_mount(self):
        self.revenue_list.update_display()

    def before_update(self):
        days = query_miss_days()
        print("---", days)
        self.sync_bt.text = f"同步({days}天)"

    def open_revenue_sync_dialog(self):
        self.page.open(self.sync_dialog)

    def close_login_dialog(self):
        self.page.close(self.login_dialog)
        self.login_dialog.open_dialog(False)

    def query_revenue(self, start=0, end=10):
        rows, total_count = query_revenues(
            offset=start,
            limit=end - start,
            **self.build_filter()
        )
        print(len(rows), "???", total_count, "????")
        return [to_data_cell(r) for r in rows], total_count

    def did_mount(self):
        print("Running in RevenueListPage")
        if is_user_need_login():
            # 打开登录页面
            self.login_dialog.open_dialog(True)
            self.page.open(self.login_dialog)
        else:
            # 获取最新的收益列表
            print("Start query revenue list")
            self.query_revenue()

    def build_filter(self):
        """
        构建 values , 用于查询收益列表
        """
        filter_values = [None if c.value == '' else c.value for c in self.filters.controls]
        return {
            "uname": filter_values[0],
            "start_time": filter_values[1],
            "end_time": filter_values[2],
            "min_gold": filter_values[3],
            "max_gold": filter_values[4],
            # "gift_name": filter_values[4],
        }

    def revenue_export(self):
        """
        导出符合条件的 excel 文件
        """

        file_name = f"{uuid_getter()}.xlsx"

        def close_banner(e):
            self.page.close(banner)

        banner = ft.Banner(content=ft.Text(f"Exported to {file_name}"), actions=[
            ft.TextButton(text="Cancel", on_click=close_banner)
        ])

        revenues, count = query_revenues(**self.build_filter(), query_all=1)
        write_to_excel(file_name, revenues)
        self.page.open(banner)


class BilibiliLoginDialog(ft.AlertDialog):
    scan_state_dict = ['Waiting for scan', 'Scanned', 'Confirmed', 'Expired']

    def __init__(self, app: RevenueListPage, page: ft.Page):
        super().__init__()
        self.app = app
        self.page = page
        self.qrcode_info = None
        self.has_login = False
        self.in_login = False
        self.qrcode_key = None
        self.qrcode_img = ft.Image(src="")
        self.scan_state = ft.Text(value=self.scan_state_dict[0])
        self.content = ft.Column(controls=[
            ft.Text("扫码登录"),
            self.qrcode_img,
            self.scan_state
        ])

    def open_dialog(self, open):
        if open:
            self.qrcode_info = generate_qr_code()
            self.qrcode_key = self.qrcode_info["qrcode_key"]
            self.qrcode_img.src = self.qrcode_info["qrcode"]
            self.in_login = True
            self.page.run_thread(self.query_scan)
        else:
            self.in_login = False

    def query_scan(self) -> None:
        """
        查询扫码结果
        """
        while self.in_login:
            scan_state, url_ = poll_qr_code(self.qrcode_key)
            if scan_state == 0:
                # 登录成功
                self.scan_state.value = self.scan_state_dict[2]
                time.sleep(1)
                tokens = parse_login_url(url_)
                session_data = quote(tokens["SESSDATA"])
                save_token(session_data, tokens["Expires"])
                self.in_login = False
            if scan_state == 86101:
                # 未扫码
                self.scan_state.value = self.scan_state_dict[0]
                self.scan_state.update()
            if scan_state == 86090:
                # 已扫码未确认
                self.scan_state.value = self.scan_state_dict[1]
                self.scan_state.update()
            time.sleep(2)
        self.app.close_login_dialog()
