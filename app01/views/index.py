# @Auth:fengfeng
# @Time:2022/01/02 19:27
from django.contrib import auth
from django.db.models import F
from django.shortcuts import render, HttpResponse, redirect

from app01.models import *
from lib.pagination import Pagination
from lib.qq_get_user import OAuthLogin
from lib.random_code import random_code
from lib.sub_comment import sub_comment_list



# 首页
def index(request):
    """
    首页
    """
    article_list = Articles.objects.filter(status=1, category__in=[1, 2]).order_by('-change_date')
    frontend_list = article_list.filter(category=1)[:6]
    backend_list = article_list.filter(category=2)[:6]

    query_params = request.GET.copy()

    pager = Pagination(
        current_page=request.GET.get('page'),
        all_count=article_list.count(),
        base_url=request.path_info,
        query_params=query_params,
        per_page=10,
        pager_page_count=7
    )
    # 文章列表
    article_list = article_list[pager.start:pager.end]

    # 广告列表
    advert_list = Advert.objects.filter(is_show=True)

    # 文章封面列表
    cover_list = Cover.objects.all()

    link_list = Navs.objects.filter(tag__title='博客')

    # 在线人数
    online_count = len(request.online_list)

    return render(request, 'index.html', locals())


# 搜索
def search(request):
    """

    """
    search_key = request.GET.get('key', '')
    order = request.GET.get('order', '')
    tag = request.GET.get('tag', '')
    word = request.GET.getlist('word')

    query_params = request.GET.copy()

    article_list = Articles.objects.filter(title__contains=search_key)

    # 字数搜索
    if word:
        if len(word) == 1 and word[0] != '':
            article_list = article_list.filter(word__gte=word[0])
        elif len(word) == 2:
            article_list = article_list.filter(word__range=word)

    if tag:
        article_list = article_list.filter(tag__title=tag)

    if order:
        try:
            article_list = article_list.order_by(order)
        except Exception:
            pass

    # 分页器
    pager = Pagination(
        current_page=request.GET.get('page'),
        all_count=article_list.count(),
        base_url=request.path_info,
        query_params=query_params,
        per_page=10,
        pager_page_count=7
    )
    article_list = article_list[pager.start:pager.end]

    return render(request, 'search.html', locals())


# 文章详情页
def article(request, nid):
    """

    """
    article_query = Articles.objects.filter(nid=nid)

    article_query.update(look_count=F('look_count') + 1)
    if not article_query:
        return redirect('/')
    article_obj: Articles = article_query.first()
    comment_list = sub_comment_list(nid)

    if article_obj.pwd:

        pwd = request.session.get(f'article_pwd__{nid}')
        if pwd == article_obj.pwd:
            # 已经输入了成功的密码
            return render(request, 'article.html', locals())

        return render(request, 'article_lock.html', locals())

    return render(request, 'article.html', locals())


# 新闻页
def news(request):
    """
    新闻页，在页面中，注意itab的接口，需要改一下请求头
    """
    return render(request, 'news.html')


# 关于页
def about(request):
    # 编号37的文章
    article_query = Articles.objects.filter(nid=37)

    article_query.update(look_count=F('look_count') + 1)
    if not article_query:
        return redirect('/')
    article_obj: Articles = article_query.first()

    comment_list = sub_comment_list(37)

    return render(request, 'about.html', locals())


# 心情页
def moods(request):
    # 查询所有的头像
    avatar_list = Avatars.objects.all()

    # 搜索
    key = request.GET.get('key', '')

    mood_list = Moods.objects.filter(content__contains=key).order_by('-create_date')

    # 分页器
    query_params = request.GET.copy()

    pager = Pagination(
        current_page=request.GET.get('page'),
        all_count=mood_list.count(),
        base_url=request.path_info,
        query_params=query_params,
        per_page=5,
        pager_page_count=7
    )
    mood_list = mood_list[pager.start:pager.end]

    return render(request, 'moods.html', locals())


# 历史页
def history(request):
    history_list = History.objects.all().order_by('-create_date')
    return render(request, 'history.html', locals())


# 网站导航页
def sites(request):
    # 取所有的标签
    tag_all = NavTags.objects.all()
    tag_list = tag_all.exclude(navs__isnull=True)

    return render(request, 'sites.html', locals())


# 项目相关
def project(request):
    project_list = Project.objects.all()
    article_query = Articles.objects.all()

    return render(request, 'blog.html', locals())


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


# 登录
def login(request):
    return render(request, 'login.html')


# 注册
def sign(request):
    return render(request, 'sign.html')


# 注销
def logout(request):
    auth.logout(request)
    return redirect('/')


# 获取随机验证码
def get_random_code(request):
    data, valid_code = random_code()
    request.session['valid_code'] = valid_code
    request.session['error_count'] = 0
    return HttpResponse(data)
