import time

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import F
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View

from api.forms import clean_form
from api.forms.user_form import *
from lib.qq_get_user import QQLogin
from page.models import Articles
from page.models import Avatars, UserInfo, Feedback


# 修改密码
class EditPasswordView(View):
    def post(self, request):
        res = {
            "msg": '密码修改成功！',
            'self': None,
            'code': 414,
        }
        data = request.data
        form = EditPasswordForm(data, request=request)
        if not form.is_valid():
            # 验证不通过
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        user = request.user
        user.set_password(data['pwd'])
        user.save()
        auth.logout(request)  # 退出登录
        res['code'] = 0
        return JsonResponse(res)


# 选择头像
class EditAvatarView(View):
    def put(self, request):
        res = {
            'msg': '头像修改成功',
            'code': 414,
        }
        avatar_id = request.data.get('avatar_id')

        # 要判断用户的登录状态
        user = request.user
        sign_status = user.sign_status
        avatar = Avatars.objects.get(nid=avatar_id)

        if sign_status == 0:
            # 用户名密码注册
            user.avatar_id = avatar_id
        else:
            avatar_url = avatar.url.url
            user.avatar_url = avatar_url
        user.save()
        res['data'] = avatar.url.url
        res['code'] = 0
        return JsonResponse(res)


# 信息绑定
class EditUserInfoView(View):
    def put(self, request):
        res = {
            'code': 332,
            'msg': '信息绑定成功！',
            "self": None,
        }

        # 校验时间
        valid_email_obj = request.session.get('valid_email_obj')
        if not valid_email_obj:
            res['msg'] = '请先获取验证码！'
            return JsonResponse(res)

        time_stamp = valid_email_obj['time_stamp']
        now = time.time()
        if (now - time_stamp) > 300:  # 5分钟
            res['msg'] = "验证码超时，请重新获取！"
            return JsonResponse(res)

        form = EditUserInfoForm(request.data, request=request)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        # 绑定信息
        user = request.user

        user.email = form.cleaned_data['email']
        user.save()

        res['code'] = 0
        return JsonResponse(res)


# 我的收藏
class CancelCollection(View):
    def post(self, request):
        nid_list = request.POST.getlist('nid')
        # 这里有个bug，取消收藏，对应文章的收藏数也要-1
        request.user.collects.remove(*nid_list)
        article_query: QuerySet = Articles.objects.filter(nid__in=nid_list)
        article_query.update(collects_count=F('collects_count') - 1)
        return redirect('/backend/')


# 重置头像
class ResetAvatarView(View):
    def post(self, request: WSGIRequest):
        res = {
            'msg': '头像重置成功',
            'code': 414,
        }
        # 当前用户一致性校验
        user: UserInfo = request.user
        code = request.GET.get('code')
        if user.sign_status == 1:
            qq = QQLogin(code)
            if user.token != qq.open_id:
                res['msg'] = '用户不一致'
                return JsonResponse(res)
            user_info = qq.get_user_info
            user.nick_name = user_info[0]
            user.avatar_url = user_info[1]
            user.save()
            res['code'] = 0
        return JsonResponse(res)


# 意见反馈
class FeedBackView(View):
    def post(self, request):
        res = {
            'msg': '反馈成功，枫枫正在给你回信！',
            "code": 543,
            'self': None
        }
        form = FeedBackForm(request.data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        Feedback.objects.create(**form.cleaned_data)
        res['code'] = 0
        return JsonResponse(res)
