import requests

from app.utils.app_utils import app_log
from app.utils.qrcode import create_qrcode


request_session = requests.Session()
request_session.headers.update({"User-Agent": "MyCustomUserAgent/1.0"})

def parse_login_url(url):
    from urllib.parse import parse_qs, urlparse

    query = parse_qs(urlparse(url).query)
    return {
        "SESSDATA": query.get("SESSDATA", [None])[0],
        "Expires": int(query.get("Expires", [0])[0]),
    }


def poll_qr_code(qrcode_key):
    """
    拉取二维码状态
    """
    url = "https://passport.bilibili.com/x/passport-login/web/qrcode/poll"
    response = request_session.get(url, params={"qrcode_key": qrcode_key})
    response_data = response.json()
    response_in_data: dict = response_data['data']
    status_code = response_in_data["code"]
    return status_code, response_in_data["url"] if "url" in response_in_data.keys() else None


@app_log
def generate_qr_code() -> dict:
    """
    获取登录二维码
    """
    url = "https://passport.bilibili.com/x/passport-login/web/qrcode/generate"
    # 设置自定义 User-Agent
    response = request_session.get(url).json()
    if response["code"] == 0:
        url = response["data"]["url"]
        qrcode_key = response["data"]["qrcode_key"]
        return {
            "qrcode": create_qrcode(url),
            "qrcode_key": qrcode_key
        }
    raise Exception("Failed to generate QR code.")
