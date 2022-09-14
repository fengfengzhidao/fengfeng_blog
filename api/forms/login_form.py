# @Time:2022/9/2 21:17
# @Author:fengfeng
# CBV  class
# FBV  function

from django import forms
from django.contrib import auth

from page.models import UserInfo


class LoginBaseForm(forms.Form):
    # 重写init方法
    def __init__(self, *args, **kwargs):
        # 做自己想做的事情
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    # 局部钩子
    def clean_code(self):
        code: str = self.cleaned_data.get('code')
        valid_code: str = self.request.session.get('valid_code')
        if code.upper() != valid_code.upper():
            self.add_error('code', '验证码输入错误！')
        return code


# 登录的字段验证
class LoginForm(LoginBaseForm):
    name = forms.CharField(error_messages={'required': '请输入用户名'})
    pwd = forms.CharField(error_messages={'required': '请输入密码'})
    code = forms.CharField(error_messages={'required': '请输入验证码'})

    # 全局钩子
    def clean(self):
        name = self.cleaned_data.get('name')
        pwd = self.cleaned_data.get('pwd')

        user = auth.authenticate(username=name, password=pwd)
        error_count = self.request.session.get('error_count', 0)
        if error_count >= 3:
            self.add_error('name', '错误过多，请重新获取验证码')
            return None

        if not user:
            # 失败， 给一个字段添加错误信息
            error_count += 1
            self.request.session['error_count'] = error_count
            self.add_error('name', '用户名或密码错误')
            return self.cleaned_data

        # 把用户对象放到cleaned_data中
        self.cleaned_data['user'] = user
        return self.cleaned_data


# 注册的字段验证
class SignForm(LoginBaseForm):
    name = forms.CharField(error_messages={'required': '请输入用户名'})
    pwd = forms.CharField(error_messages={'required': '请输入密码'})
    re_pwd = forms.CharField(error_messages={'required': '请输入确认密码'})
    code = forms.CharField(error_messages={'required': '请输入验证码'})

    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        re_pwd = self.cleaned_data.get('re_pwd')
        if pwd != re_pwd:
            self.add_error('re_pwd', '两次密码不一致')
        return self.cleaned_data

    def clean_name(self):
        name = self.cleaned_data.get('name')
        user_query = UserInfo.objects.filter(username=name)
        if user_query:
            self.add_error('name', '该用户已注册')
        return name
