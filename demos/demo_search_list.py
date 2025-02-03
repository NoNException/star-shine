import flet as ft


class CustomerSearchBar(ft.SearchBar):
    """
    自定义的“SearchBar”组件:
      - 包含一个输入框
      - 下拉容器用于显示“搜索历史”与“热搜”
      - 点击历史或热搜时，填入输入框并执行搜索
      - 提供清空历史功能
    """

    def __init__(
            self,
            placeholder: str = "搜索你感兴趣的视频",
            history_data: list[str] = None,
            custom_container: ft.Container = None,
            max_history: int = 10,  # 最多保留多少条历史
            *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.placeholder = placeholder
        self.history_data = history_data or []
        self.max_history = max_history
        self.search_history_container = ft.Container()
        self.custom_container = custom_container
        self.controls = self.build()

    def build(self):
        # 初次构建时，把“历史”和“热搜”列表写入下拉容器
        self._build_suggestion_list()

        # 最终返回一个Column，将搜索框与下拉建议上下排列
        # 或者也可用Stack让下拉悬浮在搜索框之下
        return [
            self.search_history_container,
            ft.Divider(height=9, thickness=3),
            self.custom_container
        ]

    def _build_suggestion_list(self):
        """根据当前历史数据、热搜数据重构下拉列表内容"""
        history_panel = ft.Column()

        # --- 搜索历史 ---
        # 标题 + 清空按钮
        history_header = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text("搜索历史", weight=ft.FontWeight.BOLD),
                ft.TextButton(
                    text="清空",
                    on_click=lambda e: self._clear_search_history()
                )
            ]
        )
        history_panel.controls.append(history_header)
        # 历史列表
        chip_panels = []
        for item in self.history_data:
            chip_panels.append(
                ft.Chip(
                    label=ft.Text(item),
                    on_click=lambda e: self._on_history_item_click(e)
                )
            )
        history_panel.controls.append(ft.Row(controls=chip_panels, wrap=True))
        self.search_history_container.content = history_panel

    def _clear_search_history(self):
        """清空搜索历史"""
        self.history_data.clear()
        self._build_suggestion_list()
        self.update()

    def _on_history_item_click(self, e):
        """点击历史记录后：将其放入输入框并执行搜索"""
        self.bar_hint_text = e.control.data
        self.close_view()


# ----------------------------------------------
# 使用示例
# ----------------------------------------------
def main(page: ft.Page):
    page.title = "搜索示例 - 自定义SearchBar"

    def handle_tap(e):
        search_bar.open_view()

    def handle_change(e):
        print(e.data)

    # 创建一个SearchBar实例
    search_bar = CustomerSearchBar(
        bar_hint_text="搜索你感兴趣的视频",
        history_data=["自然拼读", "瑞秋英语Rachel", "田鸽田jay和lari", "马斯克演讲", "flet"],
        custom_container=ft.Container(content=ft.Column(
            controls=[
                ft.Text("自定义内容"),
                ft.Text("aaaa")

            ]
        )),
        max_history=10,
        on_change=handle_change,
        on_tap=handle_tap,
        expand=False
    )

    # 将SearchBar加到页面
    page.add(
        ft.Row([search_bar], alignment=ft.MainAxisAlignment.CENTER)
    )

    # 如果想让 SearchBar 宽度自动扩展占据剩余空间，可将 expand=True 并放到合适的容器布局中。


if __name__ == "__main__":
    ft.app(target=main)
