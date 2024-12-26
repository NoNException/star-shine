import customtkinter as ctk


class UserView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        # 标题
        self.label_title = ctk.CTkLabel(self, text="用户信息管理", font=("Arial", 24))
        self.label_title.grid(row=0, column=0, columnspan=2, pady=10)

        # 用户输入框
        self.label_name = ctk.CTkLabel(self, text="姓名:")
        self.label_name.grid(row=1, column=0, padx=10, pady=10)
        self.entry_name = ctk.CTkEntry(self, width=200)
        self.entry_name.grid(row=1, column=1, padx=10, pady=10)

        self.label_age = ctk.CTkLabel(self, text="年龄:")
        self.label_age.grid(row=2, column=0, padx=10, pady=10)
        self.entry_age = ctk.CTkEntry(self, width=200)
        self.entry_age.grid(row=2, column=1, padx=10, pady=10)

        # 按钮
        self.button_add = ctk.CTkButton(self, text="添加用户")
        self.button_add.grid(row=3, column=0, columnspan=2, pady=10)

        # 数据表格
        self.table = ctk.CTkTextbox(self, height=150, width=400)
        self.table.grid(row=4, column=0, columnspan=2, pady=10)

    def set_controller(self, controller):
        self.controller = controller
        self.button_add._command = controller.add_user

    def update_table(self, data):
        self.table.delete(1.0, "end")
        for user in data:
            self.table.insert("end", "asdf")
