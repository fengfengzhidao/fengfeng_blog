from django import forms
from django.db.models import F
from django.http import JsonResponse
from django.views import View

from api.forms import clean_form
from page.models import NavTags, Navs
from lib.cache import frequency_limit_decorator
from lib.permissions_control import is_super_method


# 标签视图
class NavTagsView(View):
    @is_super_method
    def post(self, request, **kwargs):
        res = {
            'msg': '标签添加成功！',
            'code': 442,
            "self": None,
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)
        title = request.data.get('title')
        if not title:
            res['msg'] = '请输入标签名'
            return JsonResponse(res)

        nid = kwargs.get('nid')
        if nid:
            # 编辑
            tag_query = NavTags.objects.filter(nid=nid)
            tag_query.update(title=title)
            res['code'] = 0
            res['msg'] = '标签编辑成功！'
            return JsonResponse(res)
        tag_query = NavTags.objects.filter(title=title)
        if tag_query:
            res['msg'] = '该标签已存在！'
            return JsonResponse(res)

        NavTags.objects.create(title=title)
        res['code'] = 0
        return JsonResponse(res)

    @is_super_method
    def delete(self, request, nid):
        res = {
            'msg': '标签删除成功！',
            'code': 442,
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)
        tag_query = NavTags.objects.filter(nid=nid)
        if tag_query:
            tag_query.delete()
        res['code'] = 0
        return JsonResponse(res)


# 添加网站的验证
class NavForm(forms.Form):
    title = forms.CharField(min_length=4, max_length=32,
                            error_messages={'required': '请输入网站标题', 'min_length': '网站标题小于4字符', 'max_length': '标题超过32字符'})
    abstract = forms.CharField(min_length=10, max_length=128,
                               error_messages={'required': '请输入网站简介', 'min_length': '网站简介小于10字符',
                                               'max_length': '内容超过128字符'})
    href = forms.URLField(error_messages={'required': '请输入网站链接'})
    icon_href = forms.URLField(error_messages={'required': '请输入网站图标'})
    status = forms.IntegerField(required=False)

    # 重写init方法
    def __init__(self, *args, **kwargs):
        # 做自己想做的事情
        self.request = kwargs.pop('request', None)
        self.add_or_edit = kwargs.pop('add_or_edit', True)
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']
        nav_query = Navs.objects.filter(title=title)
        if self.add_or_edit:
            if nav_query:
                self.add_error('title', '该网站标题已存在')
        return title

    def clean_status(self):
        status = 0
        if self.request.user.is_superuser:
            # 超级管理员
            status = 1
        return status


# 网站的视图
class NavView(View):
    def get(self, request):

        title = request.GET.get('title')
        order = request.GET.get('order')
        data = []

        if request.user.is_authenticated:
            nav_coll_list = request.user.navs.all()
        else:
            nav_coll_list = []

        if title == '我的收藏' and request.user.is_authenticated:
            nav_list = request.user.navs.all().order_by(f"-{order}")
        else:
            nav_list = Navs.objects.filter(tag__title=title, status=1).order_by(f"-{order}")

        for nav in nav_list:
            data.append({
                "nid": nav.nid,
                "title": nav.title,
                "abstract": nav.abstract,
                "href": nav.href,
                "icon_href": nav.icon_href,
                "create_date": nav.create_date.strftime("%Y-%m-%d"),
                "collects_count": nav.collects_count,
                "digg_count": nav.digg_count,
                "tags": [{
                    "nid": tag.nid,
                    "title": tag.title,
                } for tag in nav.tag.all()],
                "is_coll": 'show' if nav in nav_coll_list else '',
            })

        return JsonResponse(data, safe=False)

    def post(self, request):
        res = {
            'msg': '网站添加成功！',
            'code': 442,
            "self": None,
        }
        data = request.data

        form = NavForm(data, request=request)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        # 添加
        obj = Navs.objects.create(**form.cleaned_data)

        # 添加标签 [1,5,3]
        tag = data.get('tag')
        if tag:
            obj.tag.add(*tag)

        if not request.user.is_superuser:
            res['msg'] = '感谢添加，管理员正在审核！'

        res['code'] = 0
        return JsonResponse(res)

    @is_super_method
    def put(self, request, nid):
        res = {
            'msg': '网站编辑成功！',
            'code': 442,
            "self": None,
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)
        data = request.data

        form = NavForm(data, request=request, add_or_edit=False)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        # 编辑
        nav_query = Navs.objects.filter(nid=nid)
        nav_query.update(**form.cleaned_data)

        tag = data.get('tag')
        obj: Navs = nav_query.first()

        # 先清空再添加
        obj.tag.clear()
        if tag:
            obj.tag.add(*tag)

        res['code'] = 0
        return JsonResponse(res)

    @is_super_method
    def delete(self, request, nid):
        res = {
            'msg': '网站删除成功！',
            'code': 442,
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)
        nav_query = Navs.objects.filter(nid=nid)
        nav_query.delete()
        res['code'] = 0
        return JsonResponse(res)


# 点赞
class NavDiggView(View):
    @frequency_limit_decorator()
    def post(self, request, nid):
        res = {
            'msg': '点赞+1！',
            'code': 442,
        }

        Navs.objects.filter(nid=nid).update(digg_count=F("digg_count") + 1)
        res['code'] = 0
        return JsonResponse(res)


# 收藏
class NavCollectsView(View):
    def post(self, request, nid):
        # 判断登录
        # 同样的请求，收藏变取消收藏
        res = {
            'msg': '网站收藏成功！',
            'code': 412,
            "isCollects": True,  # 是否是收藏
        }
        if not request.user.username:
            res['msg'] = '请登录'
            return JsonResponse(res)

        # 判断用户是否收藏过网站
        flag = request.user.navs.filter(nid=nid)
        num = 1
        res['code'] = 0
        if flag:
            # 用户已经收藏了网站， 取消收藏
            res['msg'] = '文章取消收藏成功！'
            res['isCollects'] = False
            request.user.navs.remove(nid)
            num = -1
        else:
            request.user.navs.add(nid)

        res['data'] = num
        nav_query = Navs.objects.filter(nid=nid)
        nav_query.update(collects_count=F('collects_count') + num)
        return JsonResponse(res)


# 友链
class FriendLinks(View):
    def post(self, request):
        res = {
            'msg': '友链添加成功！',
            'code': 442,
            "self": None,
        }
        data = request.data

        form = NavForm(data, request=request)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        # 添加
        obj = Navs.objects.create(**form.cleaned_data)

        # 添加标签 [1,5,3]
        nav_tag = NavTags.objects.get(title='博客')
        obj.tag.add(nav_tag.nid)

        if not request.user.is_superuser:
            res['msg'] = '友链添加成功，管理员正在审核！'

        res['code'] = 0
        return JsonResponse(res)
