import json
from urllib.parse import urlencode, parse_qs

import requests
from django.conf import settings
from django.contrib import auth
from django.db.models import Q

from page.models import UserInfo
from .get_user_info import get_ip, get_addr_info


class QQLogin:
    __app_id = settings.QQ_APPID
    __app_key = settings.QQ_KEY
    __redirect_url = settings.QQ_REDIRECT

    def __init__(self, code):
        self._code = code
        self._access_token = self.get_access_token()
        self.open_id = self.get_open_id(self._access_token)

    # 获取token
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

    # 获取openid
    def get_open_id(self, access_token):
        # 获取openid
        response = requests.get(f'https://graph.qq.com/oauth2.0/me?access_token={access_token}')
        openid = json.loads(response.text[10:-4])['openid']
        # print('openid：', openid)
        return openid

    # 获取用户信息
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
    def get_user_info(self) -> tuple:
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

    # 获取token
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

    # 获取用户信息
    @property
    def __get_userinfo(self):
        params = {
            "access_token": self.token
        }
        res = requests.get(url='https://gitee.com/api/v5/user', params=params).json()

        return res


# 同一的登录处理
class OAuthLogin:
    def __init__(self, login_status, code):
        auth_status = {
            'qq': [QQLogin, 1],
            'gitee': [GiteeLogin, 2]
        }

        auth_class = auth_status.get(login_status)
        if not auth:
            raise KeyError('暂无匹配的三方处理类')
        auth_obj: QQLogin or GiteeLogin = auth_class[0](code)
        self.sign_status = auth_class[1]
        self.auth = auth_obj

    def handler(self, request):
        # 用户名和头像
        self.user_info: tuple = self.auth.get_user_info  # 是一个列表  [nick_name, url]
        # 唯一id
        open_id = self.auth.open_id
        # 先查询是否有这个用户
        user = UserInfo.objects.filter(Q(username=open_id) | Q(token=open_id))
        if user:
            # 直接登录
            return self.login(request, user.first())
        # 注册
        return self.register(request)

    def login(self, request, user):
        """登录"""
        auth.login(request, user)

    def register(self, request):
        """注册"""
        user = UserInfo.objects.create_user(
            username=self.auth.open_id,
            password='123456',  # 生成密码， 这里生成密码也无所谓，反正别人也不知道open_id
            nick_name=self.user_info[0],
            avatar_url=self.user_info[1],
            token=self.auth.open_id,
            sign_status=self.sign_status,
            ip=get_ip(request),
            addr=get_addr_info(get_ip(request))
        )
        self.login(request, user)


if __name__ == '__main__':
    qq = QQLogin('A683BC931914F1622BBB629327C84CB7')
    print(qq.get_user_info, qq.open_id)
    # 重新获取头像只有用户重新登录
