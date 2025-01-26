import os

DATABASE_PATH = os.path.join("data", "user_data.db")


def env_init():
    """
    加载环境变量, 配置文件在以下两个文件中
    ~/langchain_api_key.ini
    ~/segment_api_key
    """
    with open("app/app_config", "r") as f:
        for li in f.readlines():
            if li.strip() and "=" in li:
                env_pairs = li.split("=")
                os.environ[env_pairs[0]] = env_pairs[1].strip()

