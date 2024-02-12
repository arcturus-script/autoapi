from config import api_list
from tools import create_redis_key, get, get_localtime, post, timeDelay
import redis


class AutoApi:
    def __init__(self, conf) -> None:
        self.client_id = conf.get("client_id")
        self.secret = conf.get("secret")
        self.redirect_uri = conf.get("redirect_uri")
        self.redis_key = create_redis_key(conf.get("redis_key"))
        self.refresh_token = conf.get("refresh_token")
        self.redis = redis.StrictRedis(
            host=conf.get("redis_host"),
            port=conf.get("redis_port"),
        )

    def test_key_exists(self):
        return self.redis.exists(self.redis_key)

    def get_token(self):
        url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.secret,
            "redirect_uri": self.redirect_uri,
        }

        try:
            rep = post(url, data=data, headers=headers)

            if "error" in rep:
                raise Exception(rep["error_description"])
            else:
                return [rep.get("access_token"), rep.get("refresh_token")]

        except Exception as ex:
            print(f"[Error] {ex}")

    def start(self):
        if self.test_key_exists() == 0:
            if self.refresh_token == "":
                print("Refresh token is empty. :(")
                return

            self.redis.set(self.redis_key, self.refresh_token)

        self.refresh_token = self.redis.get(self.redis_key)  # overlay config

        tokens = self.get_token()
        self.redis.set(self.redis_key, tokens[1])  # update token

        headers = {
            "Authorization": tokens[0],
            "Content-Type": "application/json",
        }

        for i in range(3):
            print((f"开始第{i + 1}次测试").center(20, "#"))

            try:
                for idx, API in enumerate(api_list):
                    if get(API, headers) == 200:
                        print(f"第{idx + 1}次调用成功")
                    else:
                        print(f"第{idx + 1}次调用失败")

                    timeDelay(1, 4)

                print(f"[Info] time: {get_localtime()}")
            except Exception as ex:
                print(f"[Error] {ex}")

            timeDelay(1, 4)
