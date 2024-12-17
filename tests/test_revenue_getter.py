from datetime import datetime
import unittest

from app.utils.bilibili_apis.revenue_fetcher import query_revenue_list
from app.utils.daos.login_db import get_token


class TestRevenueGetter(unittest.TestCase):
    """
    收益获取查询 测试
    """

    def test_revenue_query(self):
        now_datetime = datetime.strptime("2024-12-14", "%Y-%m-%d")
        token, _ = get_token()
        revenues = query_revenue_list(now_datetime, str(token), page_size=5)
        # 此处需要用户优先登录
        self.assertIsNotNone(revenues)
        self.assertTrue(len(revenues) > 0)
        self.assertTrue(len(revenues) == 20)
        print(revenues)
