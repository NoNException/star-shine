import os

import requests
import json
from app.utils.app_utils.common_utils import app_log


@app_log
def access_token_getter():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    client_id = os.environ.get("BAIDU_CLIENT_ID")
    client_secret = os.environ.get("BAIDU_CLIENT_SECRET")
    params = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception("Failed to get access token: {}".format(response.text))

    response_json = response.json()
    # TODO D: 在数据库中记录 access_token 和过期时间, 在打开地址识别栏的时候, 校验token是否过期
    return response_json.get("access_token")


@app_log
def address_recognition(address):
    access_token = access_token_getter()
    # 地址识别 API 的 URL
    api_url = f"https://aip.baidubce.com/rpc/2.0/nlp/v1/address?access_token={access_token}"
    # 请求头
    headers = {
        "Content-Type": "application/json"
    }

    # 请求数据
    data = {
        "text": replace_digits_with_x(address)
    }

    # 发起 POST 请求
    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        raise Exception("Address recognition failed: {}".format(response.text))
    address = response.json()
    address_total = f"{address['province']}/{address['city']}/{address['county']}/{address['town']}"
    address_detail = f"{address['detail']}"
    return replace_digits_with_x(address_total), replace_digits_with_x(address_detail)


def replace_digits_with_x(text):
    return ''.join(str(9 - int(char)) if char.isdigit() else char for char in text)
