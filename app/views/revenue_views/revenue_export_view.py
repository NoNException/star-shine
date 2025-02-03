from datetime import datetime, timedelta

import flet as ft

from app.utils.app_utils.common_utils import uuid_getter
from app.utils.app_utils.excel_utils import write_to_excel
from app.utils.daos.revenue_db import query_count_by_month, query_revenues


class RevenueExportDialog(ft.AlertDialog):

    def __init__(self, page: ft.Page, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.parent = parent
        self.title = ft.Text("Export Revenue")
        self.export_ob = ft.TextButton(text="开始导出", disabled=True, on_click=lambda e: self.revenue_export(e))
        self.actions = [
            self.export_ob,
            ft.TextButton("Close", on_click=self.clean_close)
        ]
        self.month_dropdown = ft.Dropdown(width=self.page.width / 5,
                                          options=[ft.dropdown.Option(rm) for rm in
                                                   list(reversed(get_last_12_months()))],
                                          on_change=lambda e: self.show_export_ob(e))
        self.showing_panel = ft.Column()
        self.content = ft.Column(controls=[ft.Text("选择月份进行导出"),
                                           ft.Row(
                                               controls=[ft.Text("导出"), self.month_dropdown, ft.Text("收益数据")]),
                                           self.showing_panel
                                           ],
                                 width=self.page.width / 3)

    def revenue_export(self, e):
        """
        导出符合条件的 excel 文件
        """
        user_month = self.month_dropdown.value
        file_name = f"{user_month}-收益数据.xlsx"

        user_month = self.month_dropdown.value
        start_time = datetime.strptime(user_month, "%Y年%m月").replace(day=1)
        # 获取下个月的第一天
        end_time = (start_time + timedelta(days=32)).replace(day=1)
        revenues, count = query_revenues({
            "start_time": start_time,
            "end_time": end_time,
        }, query_all=1)
        write_to_excel(file_name, revenues)
        self.showing_panel.controls.append(ft.Text(f"😄导出成功, 文件名为{file_name}"))
        self.showing_panel.update()

    def clean_close(self, e):
        self.showing_panel.controls.clear()
        self.month_dropdown.value = ""
        self.page.close(self)

    def show_export_ob(self, e):
        self.export_ob.disabled = False
        print("User has choose ", e.data)
        re_cnt, gold_sum, user_cnt = query_count_by_month(e.data)
        self.showing_panel.controls.append(ft.Text(
            f"你已经勾选了导出{e.data}数据, 该月共有{re_cnt}条收益记录，{gold_sum}金币，{user_cnt}用户, 确认导出?"))
        self.update()


def get_last_12_months():
    """
    返回包含当前月份在内的最近 12 个月(共12条)，格式为 ['YYYY-MM', 'YYYY-MM', ...]。
    默认从最早的月份到当前月份升序排列。
    """
    # 获取当前日期所在月的 1 号，方便计算
    current_month_first_day = datetime.today().replace(day=1)

    # 用来存储结果的列表
    months_list = []

    for i in range(12):
        # 计算“当前月 - i个月”
        # 这里的思路：从 0 开始遍历 0~11，i=0 表示当月，i=1 表示上个月，以此类推
        year = current_month_first_day.year
        month = current_month_first_day.month - i

        # 如果 month 小于等于 0，说明需要往前推一年
        while month <= 0:
            month += 12
            year -= 1

        # 构造这个月的日期对象(以每月1号来代表该月)
        date_obj = datetime(year, month, 1)
        # 按指定格式拼接字符串
        months_list.append(date_obj.strftime("%Y年%m月"))

    # 此时 months_list 的顺序是从当前月份往前推，到最早的（例如：2025-01, 2024-12, 2024-11, ...）
    # 如果希望按照从最早到当前月份的“升序”，可以反转列表
    months_list.reverse()
    return months_list
