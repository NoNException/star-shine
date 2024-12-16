from datetime import datetime
import unittest

from app.utils.bilibili_apis.revenue_fetcher import query_revenue_list
from app.utils.daos.login_db import get_token


class TestRevenueGetter(unittest.TestCase):
    """
    收益获取查询 测试
    """

    def test_revenue_query(self):
        now_datetime = datetime.now()
        token, _ = get_token()
        revenues = query_revenue_list(now_datetime, str(token), date_str="2024-12-14")
        # 此处需要用户优先登录
        self.assertIsNotNone(revenues)
        self.assertTrue(len(revenues) > 0)
        print(revenues)
