import time
from urllib.parse import quote

import flet as ft

from app.service.bilibili_login_service import generate_qr_code, poll_qr_code, parse_login_url
from app.utils.daos.login_db import save_token


class BilibiliLoginDialog(ft.AlertDialog):
    scan_state_dict = ['Waiting for scan', 'Scanned', 'Confirmed', 'Expired']

    def __init__(self, app, page: ft.Page):
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
