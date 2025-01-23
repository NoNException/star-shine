from calendar import month
from datetime import datetime
from typing import Optional

import flet as ft
from flet.core.types import DateTimeValue


class LunaDatePicker(ft.DatePicker):

    @property
    def value(self) -> Optional[DateTimeValue]:
        print("1-1:", self.__value)
        return self.__value

    @value.setter
    def value(self, value: Optional[DateTimeValue]):
        self.__value = value
        print("1:", value)
        self._set_attr("value", value)

    @property
    def current_date(self) -> Optional[DateTimeValue]:
        print("2-1:", self.__current_date)
        return self.__current_date

    @current_date.setter
    def current_date(self, value: Optional[DateTimeValue]):
        self.__current_date = value
        print("2:", value)
        self._set_attr("currentDate", self.__current_date)


def update_a(page, date_picker):
    print("5?????:", date_picker.value, date_picker.current_date)
    date_picker.current_date =  "+++++"
    date_picker.value = "???"
    date_picker.update()
    page.open(date_picker)


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_change(e):
        page.add(ft.Text(f"Date changed: {e.control.value}"))

    def handle_dismissal(e):
        page.add(ft.Text(f"DatePicker dismissed"))

    a = LunaDatePicker(
        current_date=datetime(year=2024, month=1, day=1),
        field_label_text="农历生日",
        field_hint_text="正月/初一",
        help_text="请输入农历生日",
        on_change=handle_change,
        on_dismiss=handle_dismissal,
    )
    page.add(a)
    page.add(
        ft.ElevatedButton(
            "Pick date",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: update_a(page, a),
        )
    )
    page.update()


if __name__ == '__main__':
    ft.app(main)
