from django.views import View
from django.http import JsonResponse
from markdown import markdown
from pyquery import PyQuery
from app01.models import Tags, Articles, Cover, Project
from django import forms
from api.views.login import clean_form
import random
from django.db.models import F
from lib.permissions_control import is_super_method


# 添加文章或 编辑文章的验证
class AddArticleForm(forms.Form):
    title = forms.CharField(error_messages={'required': '请输入文章标题'})
    content = forms.CharField(error_messages={'required': '请输入文章内容'})
    abstract = forms.CharField(required=False)  # 不进行为空验证
    cover_id = forms.CharField(required=False)  # 不进行为空验证
    category = forms.IntegerField(required=False)
    status = forms.IntegerField(required=False)
    pwd = forms.CharField(required=False)
    recommend = forms.BooleanField(required=False)
    word = forms.IntegerField(required=False)  # 文章字数

    # 文章简介
    def clean_abstract(self):
        abstract = self.cleaned_data['abstract']
        if abstract:
            return abstract
        # 截取正文的前30个字符
        content = self.cleaned_data.get('content')
        if content:
            abstract = PyQuery(markdown(content)).text()[:90]
            return abstract

    # 文章封面
    def clean_cover_id(self):
        cover_id = self.cleaned_data['cover_id']
        if cover_id:
            return cover_id
        cover_set = Cover.objects.all().values('nid')
        cover_id = random.choice(cover_set)['nid']
        return cover_id

    # 获取文章的字符个数
    def clean_word(self):
        return len(self.cleaned_data.get('content', ''))


# 给文章添加标签
def add_article_tags(tags, article_obj):
    for tag in tags:
        if tag.isdigit():
            article_obj.tag.add(tag)
        else:
            # 先创建，再多对多关联
            tag_obj = Tags.objects.create(title=tag)
            article_obj.tag.add(tag_obj.nid)


# 文章
class ArticleView(View):
    # 添加文章
    @is_super_method
    def post(self, request):
        res = {
            'msg': '文章发布成功！',
            "code": 412,
            'data': None
        }
        data = request.data
        data['status'] = 1

        form = AddArticleForm(data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 校验通过
        form.cleaned_data['author'] = '枫枫'
        form.cleaned_data['source'] = '枫枫知道个人博客'
        article_obj = Articles.objects.create(**form.cleaned_data)
        tags = data.get('tags')
        # 添加标签
        add_article_tags(tags, article_obj)

        res['code'] = 0
        res['data'] = article_obj.nid
        return JsonResponse(res)

    # 编辑文章
    @is_super_method
    def put(self, request, nid):
        res = {
            'msg': '文章编辑成功！',
            "code": 412,
            'data': None
        }

        article_query = Articles.objects.filter(nid=nid)
        if not article_query:
            res['msg'] = '请求错误'
            return JsonResponse(res)
        data = request.data
        data['status'] = 1

        form = AddArticleForm(data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 校验通过
        form.cleaned_data['author'] = '枫枫'
        form.cleaned_data['source'] = '枫枫知道个人博客'
        article_query.update(**form.cleaned_data)

        tags = data.get('tags')
        # 标签修改
        # 清空这篇文章所有的标签
        article_query.first().tag.clear()

        # 添加标签
        add_article_tags(tags, article_query.first())

        res['code'] = 0
        res['data'] = article_query.first().nid
        return JsonResponse(res)


# 文章点赞
class ArticleDiggView(View):
    def post(self, request, nid):
        # nid  评论id
        res = {
            'msg': '点赞成功！',
            'code': 412,
            "data": 0,
        }
        comment_query = Articles.objects.filter(nid=nid)
        comment_query.update(digg_count=F('digg_count') + 1)

        digg_count = comment_query.first().digg_count

        res['code'] = 0
        res['data'] = digg_count
        return JsonResponse(res)


# 文章收藏
class ArticleCollectsView(View):
    def post(self, request, nid):
        # 判断登录
        # 同样的请求，收藏变取消收藏
        res = {
            'msg': '文章收藏成功！',
            'code': 412,
            "isCollects": True,  # 是否是收藏
            'data': 0,
        }
        if not request.user.username:
            res['msg'] = '请登录'
            return JsonResponse(res)

        # 判断用户是否收藏过文章
        flag = request.user.collects.filter(nid=nid)
        num = 1
        res['code'] = 0
        if flag:
            # 用户已经收藏了文章， 取消收藏
            res['msg'] = '文章取消收藏成功！'
            res['isCollects'] = False
            request.user.collects.remove(nid)
            num = -1
        else:
            request.user.collects.add(nid)

        article_query = Articles.objects.filter(nid=nid)
        article_query.update(collects_count=F('collects_count') + num)
        collects_count = article_query.first().collects_count
        res['data'] = collects_count
        return JsonResponse(res)


# 查看加密文章
class ArticlePwdView(View):
    def post(self, request, nid):
        res = {
            'msg': '文章密码输入正确！',
            "code": 444,
        }

        pwd = request.data.get('pwd')
        # 找到这篇文章
        article_query = Articles.objects.filter(nid=nid)
        if not article_query:
            res['msg'] = '请求错误'
            return JsonResponse(res)
        article_obj = article_query.first()
        if article_obj.pwd != pwd:
            res['msg'] = '文章密码输入错误'
            return JsonResponse(res)

        request.session[f'article_pwd__{nid}'] = pwd

        res['code'] = 0
        return JsonResponse(res)


# 修改文章封面
class EditArticleCoverView(View):
    @is_super_method
    def post(self, request, nid):
        if not request.user.is_superuser:
            return JsonResponse({})
        cid = request.data.get('nid')
        Articles.objects.filter(nid=nid).update(cover_id=cid)
        return JsonResponse({})


# 项目相关
class ProjectArticleView(View):
    @is_super_method
    def post(self, request):

        res = {
            'msg': '项目添加成功！',
            "code": 432,
        }
        title = request.data.get('title')
        if not title:
            res['msg'] = '请输入标题'
            return JsonResponse(res)
        pro = Project.objects.create(title=title)

        article_list = request.data.get('article')

        pro.article.clear()
        if article_list:
            pro.article.add(*article_list)

        res['code'] = 0
        return JsonResponse(res)

    @is_super_method
    def put(self, request, nid):

        res = {
            'msg': '项目修改成功！',
            "code": 432,
        }
        title = request.data.get('title')
        if not title:
            res['msg'] = '请输入标题'
            return JsonResponse(res)
        pro = Project.objects.filter(nid=nid)
        if not pro:
            res['msg'] = '没有对应的标题'
            return JsonResponse(res)

        pro.update(title=title)

        article_list = request.data.get('article')

        pro.first().article.clear()
        if article_list:
            pro.first().article.add(*article_list)

        res['code'] = 0
        return JsonResponse(res)
