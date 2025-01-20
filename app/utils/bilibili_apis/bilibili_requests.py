import requests

request_session = requests.Session()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
request_session.headers.update(
    {
        "origin": "https://link.bilibili.com",
        "referer": "https://link.bilibili.com/p/center/index",
        "user-agent": UA,
    }
)