# 查询直播收益
import asyncio
import http.cookies
import itertools
import json
import os
import time
from datetime import datetime, timedelta, timezone
from typing import Optional

import pandas as pd
import aiohttp


def get_today() -> datetime:
    return datetime.now(tz=timezone(timedelta(hours=8)))


def is_today(dt: datetime) -> bool:
    return dt.strftime("%Y%m%d") == get_today().strftime("%Y%m%d")


class Dumper:
    # 获取收益地址
    _REVENUE_API = "https://api.live.bilibili.com/xlive/revenue/v1/giftStream/getReceivedGiftStreamNextList"
    # 获取礼物类型
    _GIFTTYPE_API = "https://api.live.bilibili.com/gift/v1/master/getGiftTypes"
    _UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"

    def __init__(
        self, cookies: dict, sleep=2, session: Optional[aiohttp.ClientSession] = None
    ):
        self.sleep = sleep
        # userId
        self._uid = int(cookies["DedeUserID"])
        self._session = session or aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=15)
        )
        cookie_jar = http.cookies.SimpleCookie(cookies)
        for cookie in cookie_jar:
            cookie_jar[cookie]["domain"] = "bilibili.com"
        self._session.cookie_jar.update_cookies(cookie_jar)
        self._last_request = 0

    async def close(self):
        await self._session.close()

    async def _get_api(self, url, **kwargs):
        """基础 API 调用
        :param url: 请求的 url 路径
        :param kwargs: 情况参数
        return: iay"""
        if time.time() - self._last_request < self.sleep:
            await asyncio.sleep(self.sleep)
        self._last_request = time.time()
        async with self._session.get(url, **kwargs) as r:
            rsp = await r.json()
            if r.status != 200 or rsp["code"] != 0:
                raise ValueError(
                    f"Failed to get data ({rsp['code']}): {rsp.get('message', rsp)}"
                )
            return rsp["data"]

    async def _get_gift_types(self):
        return await self._get_api(
            self._GIFTTYPE_API,
            headers={
                "origin": "https://link.bilibili.com",
                "referer": "https://link.bilibili.com/p/center/index",
                "user-agent": self._UA,
            },
        )

    async def _fetch_by_date(self, dt: datetime, paid_only=True):
        """
        按日期获取收益记录
        :param dt: 日期
        :param paid_only: 是否只查询类型
        return:  查询到数据"""
        params = {
            "limit": 20,
            "coin_type": 1 if paid_only else 0,
            "gift_id": "",
            "begin_time": dt.strftime("%Y-%m-%d"),
            "uname": "",
        }
        entries = []
        for pn in itertools.count():
            print(f"fetching transaction page {pn:2d} for {params['begin_time']}")
            data = await self._get_api(
                self._REVENUE_API,
                params=params,
                headers={
                    "origin": "https://link.bilibili.com",
                    "referer": "https://link.bilibili.com/p/center/index",
                    "user-agent": self._UA,
                },
            )
            entries.extend(data["list"])
            if not data["list"] or not data.get("has_more"):
                break
            params["last_id"] = data["list"][-1]["id"]
        return entries

    async def fetch_by_date(self, dt: datetime, paid_only=True, retries=5):
        """按天获取数据
        :param dt: 日期
        :param paid_only: 是否已经支付
        :param retries: 重试次数
        return 获取到的数据
        """

        for i in range(retries):
            try:
                return await self._fetch_by_date(dt, paid_only=paid_only)
            except (aiohttp.ServerDisconnectedError, asyncio.TimeoutError):
                if i == retries - 1:
                    raise
        raise

    async def dump_by_date(self, dt: datetime, paid_only=True, use_cache=True):
        """Dump transactions on date `dt` to raw json and excel spreadsheet
        :param df:
        :param paid_only:
        :param use_cache:
        return entries 实体列表
        """
        # +free-parial
        suffix = ("" if paid_only else "+free") + ("-partial" if is_today(dt) else "")
        # userId-date+free-parial
        basename = f"{self._uid}-{dt.strftime('%Y%m%d')}{suffix}"
        use_cache = use_cache and not is_today(dt)

        raw_json_fn = f"raw/{basename}.json"
        #  读取本地的json 文件中的数据
        if os.path.exists(raw_json_fn) and use_cache:
            with open(raw_json_fn, "rt", encoding="utf-8") as f:
                entries = json.load(f)
                print(f'loaded from cached "{raw_json_fn}"')
        else:
            # 按天获取数据
            entries = await self.fetch_by_date(dt, paid_only=paid_only)
            lines = ",\n".join(
                json.dumps(entry, ensure_ascii=False, separators=(",", ":"))
                for entry in entries
            )
            os.makedirs(os.path.dirname(raw_json_fn), exist_ok=True)
            with open(raw_json_fn, "wt", encoding="utf-8") as f:
                f.write(f"[\n{lines}\n]")
            print(f'entries written to "{raw_json_fn}"')

        if entries:
            xlsx_fn = f"table/{basename}.xlsx"
            os.makedirs(os.path.dirname(xlsx_fn), exist_ok=True)
            pd.DataFrame(entries).to_excel(xlsx_fn, index=False)
            print(f'entries written to "{xlsx_fn}"')
        else:
            print("nothing record to write to excel for " + dt.strftime("%Y-%m-%d"))

        return entries

    async def dump_date_range(
        self, dt: datetime, n_days: int, paid_only=True, use_cache=True
    ):
        """Backwards dump transactions starting from date `dt`, up to `n_days` ago
        :param dt: 时间戳
        :param n_days: 提前 n 天的数据
        :param paid_only: ???
        :param use_caseh: ???
        return ???
        """
        for diff in range(n_days):
            await self.dump_by_date(
                dt - timedelta(days=diff), paid_only=paid_only, use_cache=use_cache
            )
