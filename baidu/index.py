from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.services.cfc.cfc_client import CfcClient
import requests as req
import random
import time
import os


def update(REFRESH_TOKEN: str) -> None:
    try:
        """
        AK: Access Key,  SK: Secret Key
        可登录 https://console.bce.baidu.com/iam/?_=1653631921430#/iam/accesslist 查看
        """
        AK = os.environ["BCE_ACCESS_KEY_ID"]
        SK = os.environ["BCE_ACCESS_KEY_SECRET"]
        REDIRECT_URL = os.environ["REDIRECT_URL"]
        FUNC = os.getenv("FUNC", "autoApi")

        """
        host (str): CFC域名服务, 可选值:
            1. cfc.bj.baidubce.com(华北-北京)
            2. cfc.gz.baidubce.com(华南-广州)
            3. cfc.su.baidubce.com(华东-苏州)
        """
        HOST = os.getenv("HOST", "cfc.gz.baidubce.com")

        CLIENT_ID = os.environ["CLIENT_ID"]
        SECRET = os.environ["SECRET"]

        config = BceClientConfiguration(
            credentials=BceCredentials(AK, SK),
            endpoint=f"http://{HOST}",
        )

        # CFC 服务的客户端
        cfc_client = CfcClient(config)

        cfc_client.update_function_configuration(
            FUNC,
            description="更新环境变量🎉",
            environment={
                "REFRESH_TOKEN": REFRESH_TOKEN,
                "REDIRECT_URL": REDIRECT_URL,
                "FUNC": FUNC,
                "HOST": HOST,
                "CLIENT_ID": CLIENT_ID,
                "SECRET": SECRET,
            },
        )

    except KeyError as e:
        print(f"获取环境变量时出错, 原因: {e}")
    except Exception as e:
        print(f"更新 token 时出错, 原因: {e}")


# 获取 refresh_token
def get_token() -> str:
    try:
        REFRESH_TOKEN = os.environ["REFRESH_TOKEN"]
        CLIENT_ID = os.environ["CLIENT_ID"]
        SECRET = os.environ["SECRET"]
        REDIRECT_URL = os.environ["REDIRECT_URL"]

        URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
        HEADER = {"Content-Type": "application/x-www-form-urlencoded"}
        DATA = {
            "grant_type": "refresh_token",
            "refresh_token": REFRESH_TOKEN,
            "client_id": CLIENT_ID,
            "client_secret": SECRET,
            "redirect_uri": REDIRECT_URL,
        }

        resp = req.post(URL, data=DATA, headers=HEADER).json()

        if "error" in resp:
            raise Exception(resp["error_description"])
        else:
            return {
                "ACCESS_TOKEN": resp["access_token"],
                "REFRESH_TOKEN": resp["refresh_token"],
            }
    except KeyError as e:
        print(f"环境变量中缺少关键字: {e}")
    except Exception as e:
        print(f"请求 token 中出现错误, 原因: {e}")


APIS = [
    r"https://graph.microsoft.com/v1.0/me/drive/root",
    r"https://graph.microsoft.com/v1.0/me/drive",
    r"https://graph.microsoft.com/v1.0/drive/root",
    r"https://graph.microsoft.com/v1.0/users",
    r"https://graph.microsoft.com/v1.0/me/messages",
    r"https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules",
    r"https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta",
    r"https://graph.microsoft.com/v1.0/me/drive/root/children",
    r"https://graph.microsoft.com/v1.0/me/drive/recent",
    r"https://graph.microsoft.com/v1.0/me/mailFolders",
    r"https://graph.microsoft.com/v1.0/me/outlook/masterCategories",
]


def timeDelay(x, y):
    time.sleep(random.randrange(x, y))


def main(*arg):
    token = get_token()

    ACCESS_TOKEN = token["ACCESS_TOKEN"]
    REFRESH_TOKEN = token["REFRESH_TOKEN"]

    update(REFRESH_TOKEN)  # 更新 refresh_token

    HEADERS = {
        "Authorization": ACCESS_TOKEN,
        "Content-Type": "application/json",
    }

    for i in range(3):
        print(f"开始第{i+1}次测试".center(20, "#"))

        try:
            for i, API in enumerate(APIS):
                if req.get(API, headers=HEADERS).status_code == 200:
                    print(f"第 {i + 1} 次调用成功")
                else:
                    print(f"第 {i + 1} 次调用失败")

                timeDelay(1, 4)

            localtime = time.asctime(time.localtime(time.time()))

            print(f"运行结束时间为 {localtime}")

        except Exception as e:
            print(f"调用 API 时出现异常, 原因 {e}")

        timeDelay(1, 4)
