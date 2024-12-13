from datetime import datetime
import unittest

from app.utils.bilibili_apis.revenue_fetcher import query_revenue_list


class TestRevenueGetter(unittest.TestCase):
    """
    收益获取查询 测试
    """

    def test_revenue_query(self):
        now_datetime = datetime.now()
        revenues = query_revenue_list(now_datetime, 1)
        print(revenues)
        # 此处需要用户优先登录
        self.assertIsNotNone(revenues)
        self.assertTrue(len(revenues) > 0)
