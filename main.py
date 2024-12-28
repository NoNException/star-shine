from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from kivy.app import App

LabelBase.register(name="Roboto", fn_regular="/System/Library/Fonts/STHeiti Light.ttc")

# 加载 KV 文件
Builder.load_file('app/views/main_view.kv')


class MainView(BoxLayout):
    """三栏式布局的逻辑控制"""

    # 导航栏点击事件
    def on_nav_click(self, instance):
        self.ids.info_label.text = f"点击：{instance.text}"

    # 添加用户按钮点击事件
    def add_user(self):
        # 获取输入值
        name = self.ids.name_input.text
        age = self.ids.age_input.text

        # 检查输入是否有效
        if not name or not age.isdigit():
            self.ids.info_label.text = "[b]输入无效，请重新输入！[/b]"
        else:
            self.ids.info_label.text = f"[b]用户添加成功！[/b]\n姓名：{name}, 年龄：{age}"


# 应用入口
class MainApp(App):
    def build(self):
        self.title = "Main"
        return MainView()


if __name__ == '__main__':
    MainApp().run()