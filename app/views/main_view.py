import customtkinter as ctk


class MainView(ctk.CTkFrame):
    """主视图框架：包含左侧导航栏、中间操作面板、右侧信息栏"""

    def __init__(self, parent):
        super().__init__(parent)

        # 设置主框架布局
        self.grid_columnconfigure(1, weight=1)  # 中间面板自适应扩展
        self.grid_rowconfigure(0, weight=1)

        # 创建左侧导航栏
        self.create_sidebar()

        # 创建中间操作面板
        self.create_main_panel()

        # 创建右侧信息栏
        self.create_info_panel()

    # 左侧导航栏
    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nswe")  # 固定在左侧
        self.sidebar.grid_rowconfigure(10, weight=1)

        # 标题
        title_label = ctk.CTkLabel(self.sidebar, text="导航栏", font=("Arial", 18))
        title_label.pack(pady=20)

        # 添加导航按钮
        self.nav_buttons = []
        nav_items = ["首页", "用户管理", "设置"]
        for item in nav_items:
            btn = ctk.CTkButton(
                self.sidebar, text=item, command=lambda x=item: self.on_nav_click(x)
            )
            btn.pack(pady=10, padx=20, fill="x")
            self.nav_buttons.append(btn)

    # 中间操作面板
    def create_main_panel(self):
        self.main_panel = ctk.CTkFrame(self, corner_radius=10)
        self.main_panel.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        # 添加占位内容
        label = ctk.CTkLabel(self.main_panel, text="操作面板", font=("Arial", 18))
        label.pack(pady=20)

    # 右侧信息栏
    def create_info_panel(self):
        self.info_panel = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.info_panel.grid(row=0, column=2, sticky="nswe", padx=(0, 10))  # 固定在右侧

        # 信息栏标题
        info_label = ctk.CTkLabel(self.info_panel, text="信息栏", font=("Arial", 18))
        info_label.pack(pady=20)

        # 示例信息显示
        self.info_text = ctk.CTkTextbox(self.info_panel, height=400, width=180)
        self.info_text.pack(padx=10, pady=10)

    # 导航栏按钮点击事件
    def on_nav_click(self, item):
        self.info_text.insert("end", f"点击了: {item}\n")
