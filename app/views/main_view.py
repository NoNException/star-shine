from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

# 设置窗口背景颜色（浅色主题）
Window.clearcolor = (0.25, 0.9, 0.9, 1)


class MainView(BoxLayout):
    """优化版三栏式布局：左侧导航栏、中间操作面板、右侧信息栏"""

    def __init__(self, **kwargs):
        super().__init__(orientation='horizontal', padding=10, spacing=10, **kwargs)

        # 设置背景颜色
        self.info_label = None
        self.age_input = None
        self.name_input = None
        with self.canvas.before:
            Color(0.25, 0.9, 0.9, 1)  # 浅青色背景
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # 创建界面布局
        self.create_sidebar()  # 左侧导航栏
        self.create_main_panel()  # 中间操作面板
        self.create_info_panel()  # 右侧信息栏

    # 动态更新背景大小
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    # 左侧导航栏
    def create_sidebar(self):
        sidebar = StackLayout(size_hint=(0.2, 1), padding=10, spacing=10)

        # 按钮
        buttons = ["Main", "UserManage", "System Setting"]
        for btn_text in buttons:
            btn = Button(
                text=btn_text,
                size_hint=(1, None),  # 水平占满，高度固定
                height=40,
                background_normal='',
                background_color=(0.3, 0.3, 0.3, 1),
                color=(1, 1, 1, 1)
            )
            btn.bind(on_press=self.on_nav_click)
            sidebar.add_widget(btn)

        self.add_widget(sidebar)

    # 中间操作面板
    def create_main_panel(self):
        main_panel = StackLayout(size_hint=(0.6, 1), padding=20, spacing=20)

        # 标题
        main_panel.add_widget(Label(text="操作面板", font_size=18, size_hint_y=None, height=40))

        # 表单布局
        grid = StackLayout(spacing=10, padding=[20, 20, 20, 20])

        # 姓名输入框
        grid.add_widget(Label(text="姓名：", size_hint_y=None, height=30))
        self.name_input = TextInput(
            size_hint_y=None,
            height=40,
            background_color=(1, 1, 1, 1),  # 白色背景
            foreground_color=(0, 0, 0, 1)  # 黑色文字
        )
        grid.add_widget(self.name_input)

        # 年龄输入框
        grid.add_widget(Label(text="年龄：", size_hint_y=None, height=30))
        self.age_input = TextInput(
            size_hint_y=None,
            height=40,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        grid.add_widget(self.age_input)

        # 添加用户按钮
        btn_add = Button(
            text="添加用户",
            size_hint_y=None,
            height=40,
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        btn_add.bind(on_press=self.add_user)
        grid.add_widget(btn_add)

        # 添加表单到操作面板
        main_panel.add_widget(grid)
        self.add_widget(main_panel)

    # 右侧信息栏
    def create_info_panel(self):
        info_panel = StackLayout(size_hint=(0.2, 1), padding=10, spacing=10)

        # 添加标题
        info_panel.add_widget(Label(text="信息栏", font_size=18, size_hint_y=None, height=50))

        # 添加信息显示标签
        self.info_label = Label(
            text="等待操作...",
            size_hint_y=None,
            height=400,
            halign="left",
            valign="top"
        )
        self.info_label.bind(size=self.info_label.setter('text_size'))  # 文字动态调整
        info_panel.add_widget(self.info_label)

        # 添加信息栏到布局
        self.add_widget(info_panel)

    # 导航栏按钮点击事件
    def on_nav_click(self, instance):
        self.info_label.text = f"点击了：{instance.text}"

    # 添加用户按钮点击事件
    def add_user(self, instance):
        # 获取输入值
        name = self.name_input.text
        age = self.age_input.text

        # 检查输入是否有效
        if not name or not age.isdigit():
            self.info_label.text = "[b]输入无效，请重新输入！[/b]"
        else:
            self.info_label.text = f"[b]用户添加成功！[/b]\n姓名：{name}, 年龄：{age}"
