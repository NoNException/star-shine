from datetime import datetime

from app.utils.daos.login_db import get_token


def is_user_need_login():
    """
    检查用户是否需要登录
    """
    token, expire_at = get_token()
    if not token or not expire_at or datetime.now().timestamp() < float(expire_at):
        print("Need user login....")
        return True

    print("don't need user login....")
    return False
