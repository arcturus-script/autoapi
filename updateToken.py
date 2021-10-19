import requests


def get_token(refresh_token, clien_id, secret, redirect_uri):
    url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': clien_id,
        'client_secret': secret,
        'redirect_uri': redirect_uri
    }
    try:
        rep = requests.post(url, data=data, headers=headers).json()
        if 'error' in rep:
            raise Exception(rep['error_description'])
        else:
            return {
                'access_token': rep['access_token'],
                'refresh_token': rep['refresh_token']
            }
    except Exception as e:
        print('错误详情:%s' % e)
