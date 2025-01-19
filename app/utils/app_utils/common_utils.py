import logging
import uuid
from functools import wraps


def app_log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f" - Function: [{func.__name__}] with args: {args} and kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f" - Function: [{func.__name__}] returned: {result}")
        return result

    return wrapper


def uuid_getter():
    return str(uuid.uuid4())
