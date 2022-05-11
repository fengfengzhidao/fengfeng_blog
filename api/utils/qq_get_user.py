from urllib.parse import urlencode, parse_qs
import requests
import json
from django.conf import settings


class QQLogin:
    __app_id = settings.QQ_APPID
    __app_key = settings.QQ_KEY
    __redirect_url = settings.QQ_REDIRECT

    def __init__(self, code):
        self._code = code
        self._access_token = self.get_access_token()
        self.open_id = self.get_open_id(self._access_token)

    def get_access_token(self):
        # 获取Access_token
        params = {
            'grant_type': 'authorization_code',
            'client_id': self.__app_id,
            'client_secret': self.__app_key,
            'code': self._code,
            'redirect_uri': self.__redirect_url
        }
        response = requests.get(url='https://graph.qq.com/oauth2.0/token?' + urlencode(params))
        access_token = parse_qs(response.text)['access_token'][0]
        # print('access_token：', access_token)
        return access_token

    def get_open_id(self, access_token):
        # 获取openid
        response = requests.get(f'https://graph.qq.com/oauth2.0/me?access_token={access_token}')
        openid = json.loads(response.text[10:-4])['openid']
        # print('openid：', openid)
        return openid

    def __get_user_info(self, access_token, open_id):
        params = {
            'access_token': access_token,
            'oauth_consumer_key': self.__app_id,
            'openid': open_id
        }
        res = requests.get(f'https://graph.qq.com/user/get_user_info?{urlencode(params)}')
        nick_name = res.json()['nickname']
        figureurl_qq = res.json()['figureurl_qq_2']
        return nick_name, figureurl_qq

    @property
    def get_user_info(self):
        return self.__get_user_info(self._access_token, self.open_id)


class GiteeLogin:
    __client_id = settings.GITEE_ID
    __redirect_uri = settings.GITEE_REDIRECT
    __client_secret = settings.GITEE_SECRET

    def __init__(self, code):
        token = self.get_token(code)
        self.token = token
        user_info = self.__get_userinfo
        self.get_user_info = (user_info['login'], user_info['avatar_url'])
        self.open_id = user_info['id']

    def get_token(self, code):
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': self.__client_id,
            'redirect_uri': self.__redirect_uri,
            'client_secret': self.__client_secret,
        }
        res = requests.post(url='https://gitee.com/oauth/token', data=data).json()
        return res['access_token']

    @property
    def __get_userinfo(self):
        params = {
            "access_token": self.token
        }
        res = requests.get(url='https://gitee.com/api/v5/user', params=params).json()

        return res


if __name__ == '__main__':
    qq = QQLogin('A683BC931914F1622BBB629327C84CB7')
    print(qq.get_user_info, qq.open_id)
    # 重新获取头像只有用户重新登录
