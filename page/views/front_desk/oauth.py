from django.shortcuts import redirect

from lib.qq_get_user import OAuthLogin


# 三方登录就写在这里
def oauth(request):
    # 第三方登陆
    data = request.GET
    flag = data.get('flag')
    code = data.get('code')
    if not flag or not code:
        return redirect('/login/')

    oauth = OAuthLogin(flag, code)
    oauth.handler(request)
    return redirect('/')
