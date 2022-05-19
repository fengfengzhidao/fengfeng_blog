# @Auth:fengfeng
# @Time:2022/01/02 19:27

"""
网站前台的视图函数
"""
from django.shortcuts import render, HttpResponse, redirect
from app01.utils.random_code import random_code
from django.contrib import auth
from app01.models import *
from app01.utils.sub_comment import sub_comment_list
from django.db.models import F
from app01.utils.pagination import Pagination


# Create your views here.
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
    article_list = article_list[pager.start:pager.end]

    advert_list = Advert.objects.filter(is_show=True)

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


# 登录
def login(request):
    data = request.GET
    if len(data) != 2:
        return render(request, 'login.html')
    # 第三方登陆
    flag = data.get('flag')
    code = data.get('code')
    if not flag or not code:
        return redirect('/login/')
    from api.utils.qq_get_user import QQLogin, GiteeLogin
    from django.db.models import Q
    # 登录源
    sign_status = 1
    # 根据不同的三方登录去做相同的事情 拿到用户名和头像 唯一id
    try:
        if flag == 'qq':
            other = QQLogin(code)
        elif flag == 'gitee':
            sign_status = 2
            other = GiteeLogin(code)
    except Exception as e:
        return redirect('/login/')
    # 用户名和头像
    user_info = other.get_user_info
    # 唯一id
    open_id = other.open_id
    # 先查询是否有这个用户
    user = UserInfo.objects.filter(Q(username=open_id) | Q(token=open_id))
    if user:
        # 登录操作
        auth.login(request, user.first())
        return redirect('/')
    # 注册用户
    user = UserInfo.objects.create_user(
        username=other.open_id,
        password='123456',  # 生成密码
        nick_name=user_info[0],
        avatar_url=user_info[1],
        token=open_id,
        sign_status=sign_status,
    )
    auth.login(request, user)
    return redirect('/')


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
