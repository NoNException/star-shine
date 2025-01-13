"""
# 收益列表
# 2. Revenue List Page
# 3. Save Revenue into db if user's token is valid
"""
from urllib.parse import quote

import flet as ft

from app.service.revenue_service import is_user_need_login
from app.utils.daos.login_db import save_token
from app.utils.login_utils import generate_qr_code, poll_qr_code, parse_login_url


class RevenueListPage(ft.Container):
    """
    扫码对话框
    """

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.login_dialog = BilibiliLoginDialog(self, page)

        # 收益列表
        self.revenue_list = ft.DataTable(columns=[
            ft.DataColumn(ft.Text("First name")),
            ft.DataColumn(ft.Text("Last name")),
            ft.DataColumn(ft.Text("Age"), numeric=True),
        ], rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("John")),
                    ft.DataCell(ft.Text("Smith")),
                    ft.DataCell(ft.Text("43")),
                ],
            ),
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Jack")),
                    ft.DataCell(ft.Text("Brown")),
                    ft.DataCell(ft.Text("19")),
                ],
            ),
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Alice")),
                    ft.DataCell(ft.Text("Wong")),
                    ft.DataCell(ft.Text("25")),
                ],
            ),
        ], )

        self.content = ft.Column(controls=[
            ft.TextField("请输入收益", width=200),
            ft.Divider(),
            self.revenue_list
        ])

    def show_login_dialog(self):
        """
        显示登录对话框
        """
        self.page.open(self.login_dialog)

    def close_login_dialog(self):
        self.page.close(self.login_dialog)

    def did_mount(self):
        if is_user_need_login():
            self.show_login_dialog()


class BilibiliLoginDialog(ft.AlertDialog):
    scan_state_dict = ['Waiting for scan', 'Scanned', 'Confirmed', 'Expired']

    def __init__(self, app: RevenueListPage, page: ft.Page):
        super().__init__()
        self.app = app
        self.page = page
        self.qrcode_info = None
        self.qrcode_key = None
        self.qrcode_img = ft.Image()
        self.scan_state = ft.Text(value=self.scan_state_dict[0])
        self.content = [
            ft.Text("扫码登录"),
            self.qrcode_img,
            self.scan_state
        ]
        self.running = False

    def did_mount(self):
        """
        每次加载的时候, 查询一次登录二维码
        """
        self.running = True
        self.qrcode_info = generate_qr_code()
        self.qrcode_key = self.qrcode_info["qrcode_key"]
        self.qrcode_img = ft.Image(src=self.qrcode_info["qrcode"]) if self.qrcode_info else ft.Image()
        self.page.run_thread(self.query_scan)

    def will_unmount(self):
        self.qrcode_img = ft.Image()
        self.scan_state = ft.Text(value=self.scan_state_dict[0])
        self.running = False

    def query_scan(self) -> None:
        """
        查询扫码结果
        """
        while self.running:
            scan_state, url_ = poll_qr_code(self.qrcode_key)
            if scan_state == 0:
                # 登录成功
                self.scan_state.value = self.scan_state_dict[2]
                tokens = parse_login_url(url_)
                session_data = quote(tokens["SESSDATA"])
                save_token(session_data, tokens["Expires"])
                self.running = False
            if scan_state == 86101:
                # 未扫码
                self.scan_state.value = self.scan_state_dict[0]
                self.running = False
            if scan_state == 86090:
                # 已扫码未确认
                self.scan_state.value = self.scan_state_dict[1]
                self.running = False
        self.app.close_login_dialog()
