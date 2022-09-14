import random

from django.contrib import auth
from django.http import JsonResponse
from django.views import View

from api.forms import clean_form
from api.forms.login_form import LoginForm, SignForm
from page.models import UserInfo, Avatars


# CBV
class LoginView(View):
    """
    登录视图
    """

    def post(self, request):
        res = {
            'code': 425,
            'msg': "登录成功！",
            "self": None
        }
        form = LoginForm(request.data, request=request)
        if not form.is_valid():
            # 验证不通过
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        # 写我们的登录操作
        user = form.cleaned_data.get('user')
        # 登录操作
        auth.login(request, user)
        res['code'] = 0
        return JsonResponse(res)


class SignView(View):
    """
    注册视图
    """

    def post(self, request):
        res = {
            'code': 425,
            'msg': "注册成功！",
            "self": None
        }
        form = SignForm(request.data, request=request)

        if not form.is_valid():
            # 验证不通过
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        # 注册成功的代码

        user = UserInfo.objects.create_user(
            username=request.data.get('name'),
            password=request.data.get('pwd'),
        )
        # 随机选择头像
        avatar_list = [i.nid for i in Avatars.objects.all()]
        user.avatar_id = random.choice(avatar_list)
        user.nick_name = request.data.get('name')
        user.save()

        # 注册之后直接登录
        auth.login(request, user)
        res['code'] = 0

        return JsonResponse(res)
