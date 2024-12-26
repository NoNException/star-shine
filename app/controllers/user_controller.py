from app.assets.data_class import UserInfo
from app.models import user_db


class UserController:
    def __init__(self, view):
        self.view = view

        # 初始化表格数据
        self.update_table()

    def add_user(self):
        # 获取输入数据
        name = self.view.entry_name.get()
        age = self.view.entry_age.get()

        # 验证输入
        if not name or not age.isdigit():
            self.view.update_table([("错误", "请输入有效的姓名和年龄！", "")])
            return

        # 添加用户
        user_db.insert_user(UserInfo(**{"id": 12, "name": "bruce"}))
        self.update_table()

    def update_table(self):
        users = user_db.fetch_users()
        self.view.update_table(users)
