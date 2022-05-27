import updateToken as ut
import requests as req
import ScfOperate
import random
import os
import time

API_list = [
    r'https://graph.microsoft.com/v1.0/me/drive/root',
    r'https://graph.microsoft.com/v1.0/me/drive',
    r'https://graph.microsoft.com/v1.0/drive/root',
    r'https://graph.microsoft.com/v1.0/users',
    r'https://graph.microsoft.com/v1.0/me/messages',
    r'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
    r'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta',
    r'https://graph.microsoft.com/v1.0/me/drive/root/children',
    r'https://graph.microsoft.com/v1.0/me/drive/recent',
    r'https://graph.microsoft.com/v1.0/me/mailFolders',
    r'https://graph.microsoft.com/v1.0/me/outlook/masterCategories'
]


# 封装一个简易的 get 请求
def get(url, headers):
    rep = req.get(url, headers=headers)
    return rep.status_code


# 一个简易的延时器
def timeDelay(x, y):
    # 随机延迟一定的时间
    t = random.randrange(x, y)
    time.sleep(t)


def start():
    refresh_token = os.getenv('refresh_token')
    clien_id = os.getenv('clien_id')
    secret = os.getenv('secret')
    # uri 必须和 Azure 上一模一样 少一个字符都不行
    redirect_uri = os.getenv('redirect_uri')
    # 云函数名称
    function_name = os.getenv('function_name')
    # 云函数地区
    region = os.getenv('region')
    # 密钥
    SecretId = os.getenv('secret_id')
    SecretKey = os.getenv('secret_key')

    # 获取 refresh_token 和 access_token
    token = ut.get_token(refresh_token, clien_id, secret, redirect_uri)
    access_token = token['access_token']
    refresh_token = token['refresh_token']
    # 将 refresh_token 存入环境变量
    # 必须全部变量重新存进去
    ScfOperate.EnvWrite(refresh_token, function_name, clien_id, secret,
                        redirect_uri, region, SecretId, SecretKey)

    headers = {
        'Authorization': access_token,
        'Content-Type': 'application/json'
    }
    for i in range(3):
        print(('开始第%d次测试' % (i + 1)).center(20, '#'))
        try:
            for index, API in enumerate(API_list):
                if get(API, headers) == 200:
                    print('第%d次调用成功' % (index + 1))
                else:
                    print('第%d次调用失败' % (index + 1))
                timeDelay(1, 4)
            localtime = time.asctime(time.localtime(time.time()))
            print('运行结束时间为:%s' % localtime)
        except Exception as e:
            print('出现异常:%s' % e)
        timeDelay(1, 4)


def main(*arg):
    return start()


if __name__ == '__main__':
    main()
