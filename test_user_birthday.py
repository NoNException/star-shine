import unittest

from app.pages.birthday_manager import user_to_birthday


class UserBirthdayTest(unittest.TestCase):

    def test_birthday(self):

        users = user_to_birthday(3)
        self.assertIsNotNone(users)
        print(users)
