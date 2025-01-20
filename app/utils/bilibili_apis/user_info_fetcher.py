from app.utils.app_utils.common_utils import app_log
from app.utils.bilibili_apis.bilibili_requests import request_session


@app_log
def get_user_details(u_ids: list[str], session_data: str):
    """
    获取指定用户的详细信息。

    参数：
    uids (list): 用户的 mid 列表，每个 mid 为字符串类型。

    返回：
    dict: 包含用户详细信息的字典。
    """
    # 将用户 mid 列表转换为逗号分隔的字符串
    uids_str = ','.join(u_ids)
    # Bilibili 多用户详细信息 API 的 URL
    url = 'https://api.bilibili.com/x/polymer/pc-electron/v1/user/cards'
    # 定义请求参数
    params = {
        'uids': uids_str
    }
    cookie = {"SESSDATA": session_data}
    try:
        # 发送 GET 请求
        response = request_session.get(url, params=params, cookies=cookie)
        # 检查响应状态码
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 0:
                user_data = data['data']
                return [(k, d['name'], d['face']) for k, d in user_data.items()]
            else:
                print(f"API 返回错误：{data['message']}")
        else:
            print(f"请求失败，状态码：{response.status_code}")
    except request_session.RequestException as e:
        print(f"请求过程中发生错误：{e}")
    return None
