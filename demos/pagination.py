import flet as ft

from app.views.common_view.pagination import Pagination


def main(page: ft.Page):
    # 生成示例数据（100条）
    sample_data = [f"数据条目 {i + 1}" for i in range(101)]

    def data_getter(start=0, end=10):
        return [ft.DataRow(cells=[ft.DataCell(ft.Text(c))]) for c in sample_data[start:end]], len(sample_data)

    columns_getter = [ft.DataColumn(ft.Text(c)) for c in ["数据条目"]]
    pagination = Pagination(page, None, data_getter, columns_getter, total_count=101, page_size=10)
    page.add(pagination)


if __name__ == '__main__':
    ft.app(target=main)
