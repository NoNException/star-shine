import unittest

from app.assets.data_class import Revenue
from app.service.captain_service import user_to_birthday
from app.service.revenue_service import days_gap
from app.utils.app_utils.excel_utils import write_to_excel
from app.utils.daos.login_db import clean_tokens, get_token
from app.utils.qrcode import create_qrcode


class UserBirthdayTest(unittest.TestCase):

    def test_birthday(self):
        users = user_to_birthday(3)
        self.assertIsNotNone(users)
        print(users)

    def test_clean_token(self):
        clean_tokens()
        a, b = get_token()
        self.assertIsNone(a)
        self.assertIsNone(b)

    def test_create_qrcode(self):
        qrcode = create_qrcode("www.baidu.com")
        print(qrcode)
        self.assertIsNotNone(qrcode)

    def test_day_gap(self):
        a = days_gap(['2024-12-01', '2024-12-21'])
        self.assertEqual(len(a), 21)
        print(a)

    def test_export_2_excel(self):
        write_to_excel("aa.xlsx", [Revenue(id=12)])
        self.assertTrue(True)
