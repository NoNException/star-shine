import unittest

from app.assets.data_class import Revenue
from app.config import env_init
from app.service.captain_service import user_to_birthday
from app.service.revenue_service import days_gap
from app.utils.app_utils.excel_utils import write_to_excel
from app.utils.badu_apis.address_auto_recognize import address_recognition
from app.utils.bilibili_apis.user_info_fetcher import get_user_details
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

    def test_user_ids_query(self):
        user_ids = ['419106160']
        token, _ = get_token()
        user_details = get_user_details(user_ids, str(token))
        self.assertIsNotNone(user_details)
        if user_details:
            for mid, details in user_details.items():
                print(f"用户 MID: {mid}")
                print(f"昵称: {details['name']}")
                print(f"头像链接: {details['face']}")
                print(f"认证信息: {details['official']['title']}")
                print(f"会员状态: {'是' if details['vip']['status'] == 1 else '否'}")
                print("-" * 40)

    def test_user_address(self):
        env_init()
        aa = address_recognition("浙江省杭州市钱塘区新科路02号 粽子 17681870000")
        address = f"{aa["province"]} {aa['city']} {aa['county']} {aa['town']} {aa['detail']}"
        self.assertIsNotNone(aa)
        print(address)

