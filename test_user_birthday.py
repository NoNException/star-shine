import unittest

from app.service.captain_service import user_to_birthday
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
