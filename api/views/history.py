import datetime

from django import forms
from django.http import JsonResponse
from django.views import View

from api.forms import clean_form
from page.models import History
from lib.permissions_control import is_super_method

"""
在实际的体验中，回忆录的功能挺弱的，考虑不把它放入导航中
"""


class HistoryForm(forms.Form):
    title = forms.CharField(error_messages={'required': '请输入事件标题'})
    content = forms.CharField(error_messages={'required': '请输入事件内容'})
    create_date = forms.CharField(required=False)
    drawing = forms.CharField(required=False)

    def clean_create_date(self):
        create_date = self.cleaned_data['create_date']
        if not create_date:
            create_date = datetime.date.today()
            return create_date
        date = datetime.datetime.strptime(create_date.split('T')[0], '%Y-%m-%d').date()
        return date


class HistoryView(View):
    @is_super_method
    def post(self, request, **kwargs):

        res = {
            'msg': '记录发布成功！',
            "code": 412,
            "self": None,
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)
        data = request.data

        form = HistoryForm(data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        res['code'] = 0
        nid = kwargs.get('nid')
        if nid:
            # 编辑操作
            history_query = History.objects.filter(nid=nid)
            history_query.update(**form.cleaned_data)
            res['msg'] = '记录编辑成功'
            return JsonResponse(res)
        History.objects.create(**form.cleaned_data)
        return JsonResponse(res)

    @is_super_method
    def delete(self, request, nid):
        res = {
            'msg': '记录发布成功！',
            "code": 412,
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)
        history_query = History.objects.filter(nid=nid)
        history_query.delete()
        res['code'] = 0
        return JsonResponse(res)
