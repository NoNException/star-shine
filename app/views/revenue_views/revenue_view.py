import flet as ft


def main(page: ft.Page):
    page.title = "使用ListView实现搜索历史 + 热搜(可点击)"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # -------------------------
    # 1. 模拟本地“搜索历史”和“热搜”
    # -------------------------
    search_history_data = []
    trending_data = []

    # -------------------------
    # 2. 创建 ListView
    #    - 将“搜索历史”、“清空历史”、“热搜”等统统放在同一个 ListView 中
    # -------------------------
    list_view = ft.ListView(
        spacing=5,
        padding=10,
    )

    # 为了方便后续更新，先把 list_view 加到页面
    page.add(list_view)

    # -------------------------
    # 3. 构建 ListView 的内容
    # -------------------------
    def build_list_view():
        """
        重建ListView内部所有条目：
          - 搜索历史标题
          - 历史条目（可点击）
          - 清空历史
          - 分割线
          - 热搜标题
          - 热搜条目（可点击）
        """
        list_view.controls.clear()

        # 3.1 搜索历史标题
        list_view.controls.append(
            ft.ListTile(
                title=ft.Text("搜索历史", weight=ft.FontWeight.BOLD),
                # 点击标题本身一般没啥操作，这里留空
            )
        )

        # 3.2 搜索历史条目
        for item in search_history_data:
            list_view.controls.append(
                ft.ListTile(
                    title=ft.Text(item),
                    on_click=lambda e, kw=item: on_history_item_click(kw)
                )
            )

        # 3.3 清空历史
        list_view.controls.append(
            ft.ListTile(
                title=ft.Text("清空历史", color=ft.colors.RED_400),
                on_click=lambda e: clear_search_history()
            )
        )

        # 3.4 分割线
        list_view.controls.append(
            ft.Divider(height=1, thickness=1, color=ft.colors.BLACK12)
        )

        # 3.5 热搜标题
        list_view.controls.append(
            ft.ListTile(
                title=ft.Text("热搜", weight=ft.FontWeight.BOLD),
            )
        )

        # 3.6 热搜条目
        for item in trending_data:
            list_view.controls.append(
                ft.ListTile(
                    title=ft.Text(item),
                    on_click=lambda e, kw=item: on_trending_item_click(kw)
                )
            )

        # 刷新页面
        page.update()

    # -------------------------
    # 4. 点击逻辑
    # -------------------------
    def on_history_item_click(keyword):
        """点击历史记录后，做一些逻辑处理"""
        print(f"[历史] 你点击了：{keyword}")
        # 这里你可以执行搜索，或跳转页面等

    def on_trending_item_click(keyword):
        """点击热搜后，做一些逻辑处理"""
        print(f"[热搜] 你点击了：{keyword}")
        # 这里你可以执行搜索，或跳转页面等

    def clear_search_history():
        """清空历史"""
        search_history_data.clear()
        build_list_view()

    # -------------------------
    # 5. 首次渲染
    # -------------------------
    build_list_view()

    # -------------------------
    # 6. 如果有需要，可以在后续再更新 list_view
    #    例如动态增加搜索历史条目，或更新热搜等。
    # -------------------------


# 启动 Flet 应用
if __name__ == "__main__":
    ft.app(target=main)
