import customtkinter as ctk
from app.config import setup_theme
from app.views.main_view import MainView


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 设置窗口基本信息
        self.title("三栏布局框架")
        self.geometry("900x600")

        # 设置主题
        setup_theme()

        # 创建主视图
        self.view = MainView(self)
        self.view.pack(expand=True, fill="both")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
