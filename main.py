from kivy.core.text import LabelBase

from app.views.main_view import MainView
from kivy.app import App

LabelBase.register(name="Roboto", fn_regular="/System/Library/Fonts/STHeiti Light.ttc")


class MainApp(App):
    def build(self):
        self.title = "Mai???n"
        return MainView()


if __name__ == "__main__":
    MainApp().run()
