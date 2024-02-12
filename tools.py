import requests as req
import random
import time


def create_redis_key(key: str):
    return f"auto_api_onedrive_refresh_token_{key}"


def get(url, headers):
    res = req.get(url, headers=headers)
    return res.status_code


def post(*args, **kwargs):
    return req.post(*args, **kwargs).json()


def timeDelay(x, y):
    t = random.randrange(x, y)
    time.sleep(t)


def get_localtime():
    return time.asctime(time.localtime(time.time()))
