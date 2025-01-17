"""
# 收益列表
# 2. Revenue List Page
# 3. Save Revenue into db if user's token is valid
"""
import time
from cProfile import label
from urllib.parse import quote

import flet as ft

from app.assets.data_class import Revenue
from app.service.revenue_service import bilibili_sync
from app.utils.daos.login_db import save_token
from app.service.bilibili_login_service import parse_login_url, poll_qr_code, generate_qr_code, is_user_need_login
from app.utils.daos.revenue_db import query_revenues


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
        self.revenue_list = ft.DataTable(columns=[
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Time")),
            ft.DataColumn(ft.Text("Gift")),
            ft.DataColumn(ft.Text("Golds"), numeric=True),
        ], rows=[], )
        self.filters = ft.Row(controls=[
            ft.TextField(label="舰长", width=200),
            ft.TextField(label="收益(S)", width=200),
            ft.TextField(label="收益(E)", width=200),
            ft.TextField(label="时间(S)", width=200),
            ft.TextField(label="时间(E)", width=200),
        ])
        self.sync_start_time = ft.TextField(label="Start Time")
        self.sync_end_time = ft.TextField(label="End Time")
        self.content = ft.Column(controls=[
            self.filters,
            ft.Row(controls=[
                ft.OutlinedButton("Export2Excel",on_click=lambda e: print("Export2Excel")),
                ft.OutlinedButton("SyncFormBiliBili", on_click=lambda e: bilibili_sync(
                    self.sync_start_time.value, self.sync_end_time.value
                )),
                self.sync_start_time, self.sync_end_time
            ]),
            ft.Divider(),
            self.revenue_list
        ])

    def close_login_dialog(self):
        self.page.close(self.login_dialog)
        self.login_dialog.open_dialog(False)

    def did_mount(self):
        print("Running in RevenueListPage")
        if is_user_need_login():
            # 打开登录页面
            self.login_dialog.open_dialog(True)
            self.page.open(self.login_dialog)
        else:
            # 获取最新的收益列表
            print("Start query revenue list")
            filter_values = [None if c.value == '' else c.value for c in self.filters.controls]
            rows, count = query_revenues(
                {
                    "uname": filter_values[0],
                    "start_time": filter_values[1],
                    "end_time": filter_values[2],
                    "min_gold": filter_values[3],
                    "max_gold": filter_values[4],
                    # "gift_name": filter_values[4],
                },
                limit=10,
                offset=0,
            )
            self.revenue_list.rows = [to_data_cell(r) for r in rows]
            self.update()


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
