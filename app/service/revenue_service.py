import datetime

from app.utils.daos.login_db import get_token


def is_user_need_login():
    """
    检查用户是否需要登录
    """
    token, expire_at = get_token()

    if token and expire_at and datetime.now().timestamp() < float(expire_at):
        return True
    return False
