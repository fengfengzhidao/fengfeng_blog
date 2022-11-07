from django.db.models import F, Count
from django.http import JsonResponse
from django.views import View
from api.forms.article_form import AddArticleForm
from api.forms import clean_form
from page.models import Tags, Articles, Cover, Project
from lib.permissions_control import is_super_method
from lib.cache import frequency_limit_decorator
from datetime import datetime, timedelta


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
    # 文章日历
    def get(self, request):
        """
        TODO:缓存后面记得加上
        """
        now = datetime.now()

        article_data = Articles.objects.extra(
            select={'date': 'date_format(create_date, "%%Y-%%m-%%d")'}
        ).values_list('date').annotate(Count('pk'))


        date_dict = {}
        for i in range(365, -1, -1):
            yesterday = now - timedelta(days=i)
            date_dict[f'{yesterday.strftime("%Y-%m-%d")}'] = 0
        for data in article_data:
            if date_dict.get(data[0]) == 0:
                date_dict[data[0]] = data[1]
        article_date_list = list(date_dict.items())
        article_date_range = [article_date_list[0][0], article_date_list[-1][0]]
        return JsonResponse({'code': 0, 'data': {
            "article_date_list": article_date_list,
            "article_date_range": article_date_range,
        }})

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

    @frequency_limit_decorator()
    def post(self, request, nid):
        # 后台肯定要做一个点赞的频率限制
        # nid  文章id
        res = {
            'msg': '点赞成功！',
            'code': 412,
            "data": 0,
        }
        comment_query = Articles.objects.filter(nid=nid)
        comment_query.update(digg_count=F('digg_count') + 1)

        digg_count = comment_query.first().digg_count
        # 把新的点赞数返回
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
