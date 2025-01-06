import flet as ft

from flet import (
    Alignment,
    AppBar,
    Colors,
    Column,
    Container,
    Control,
    CrossAxisAlignment,
    Icon,
    IconButton,
    MainAxisAlignment,
    NavigationRail,
    NavigationRailDestination,
    NavigationRailLabelType,
    Page,
    PopupMenuButton,
    PopupMenuItem,
    Row,
    Text,
    TextAlign,
    Icons,
    UserControl,
    border_radius,
    margin,
    padding,
)
from flet.core.border_radius import vertical


class Sidebar(UserControl):
    def __init__(self, app_layout, page):
        super().__init__()
        self.app_layout = app_layout
        self.page = page
        self.top_nav_items = [
            NavigationRailDestination(
                label_content=Text("Boards"),
                label="Boards",
                icon=Icons.BOOK_OUTLINED,
                selected_icon=Icons.BOOK_OUTLINED,
            ),
            NavigationRailDestination(
                label_content=Text("Members"),
                label="Members",
                icon=Icons.PERSON,
                selected_icon=Icons.PERSON,
            ),
        ]
        self.top_nav_rail = NavigationRail(
            selected_index=None,
            label_type=NavigationRailLabelType.ALL,
            destinations=self.top_nav_items,
            on_change=self.top_nav_change,
            bgcolor=Colors.BLUE_GREY_200,
            extended=True,
            expand=True,
        )

    def build(self):
        self.view = Container(
            content=Column(
                controls=[
                    Row([Text("WorkSpace")]),
                    Container(
                        bgcolor=Colors.BLACK26,
                        border_radius=border_radius.all(30),
                        height=1,
                        width=200,
                    ),
                    self.top_nav_rail,
                    Container(
                        bgcolor=Colors.BLACK26,
                        border_radius=border_radius.all(30),
                        height=1,
                        width=200,
                    ),
                ],
                tight=True,
            ),
            padding=padding.all(15),
            margin=margin.all(0),
            width=250,
            bgcolor=Colors.BLUE_GREY_200,
        )
        return self.view

    def top_nav_change(self, e):
        self.top_nav_rail.selected_index = e.control.selected_index
        self.update()


class AppLayout(Row):
    def __init__(self, app, page, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.app = app
        self.page = page
        self.toggle_nav_rail_button = IconButton(
            icon=Icons.ARROW_CIRCLE_LEFT,
            icon_color=Colors.BLUE_GREY_400,
            selected=False,
            selected_icon=Icons.ARROW_CIRCLE_RIGHT,
            on_click=self.toggle_nav_rail,
        )
        self.sidebar = Sidebar(self, page)
        self._active_view: Control = Column(
            controls=[Text("Active View")],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )
        self.controls = [self.sidebar, self.toggle_nav_rail_button, self._active_view]

    @property
    def active_view(self):
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.update()

    def toggle_nav_rail(self, e):
        self.sidebar.visible = not self.sidebar.visible
        self.toggle_nav_rail_button.selected = not self.toggle_nav_rail_button.selected
        self.page.update()


class TrelloApp(AppLayout):
    def __init__(self, page: Page):
        self.page = page
        self.appbar_items = [
            PopupMenuItem(text="Login"),
            PopupMenuItem(),  # divider
            PopupMenuItem(text="Setting"),
        ]
        self.appbar = AppBar(
            leading=Icon(Icons.GRID_GOLDENRATIO_ROUNDED),
            leading_width=100,
            title=Text("Trolli", size=32, text_align=TextAlign.START),
            center_title=False,
            toolbar_height=75,
            bgcolor=Colors.LIGHT_BLUE_ACCENT_700,
            actions=[
                Container(
                    content=PopupMenuButton(items=self.appbar_items),
                    margin=margin.only(left=50, right=25),
                )
            ],
        )
        self.page.appbar = self.appbar
        self.page.update()
        super().__init__(
            self,
            self.page,
            tight=True,
            expand=True,
            vertical_alignment=CrossAxisAlignment.START,
        )


if __name__ == "__main__":

    def main(page: Page):
        page.title = "Flet Trello clone"
        page.padding = 0
        page.bgcolor = Colors.BLUE_GREY_200
        app = TrelloApp(page)
        page.add(app)
        page.update()

    ft.app(main)
