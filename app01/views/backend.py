import datetime

from django.shortcuts import render, redirect
from app01.models import *
from django.contrib import auth
from lib.permissions_control import is_super_fun
from api.models import *


# 后台
def backend(request):
    if not request.user.username:
        # 没有登录
        return redirect('/')

    data = request.GET
    if len(data) != 2:
        user = request.user
        collects_query = user.collects.all()
        return render(request, 'backend/backend.html', locals())
    # 第三方登陆
    flag = data.get('flag')
    code = data.get('code')
    if not flag or not code:
        return redirect('/login/')
    from lib.qq_get_user import QQLogin, GiteeLogin
    from django.db.models import Q
    # 登录源
    sign_status = 1
    # 根据不同的三方登录去做相同的事情 拿到用户名和头像 唯一id
    try:
        if flag == 'qq':
            other = QQLogin(code)
        elif flag == 'gitee':
            sign_status = 1
            other = GiteeLogin(code)
    except Exception as e:
        return redirect('/login/')
    # 用户名和头像
    user_info = other.get_user_info
    # 唯一id
    open_id = other.open_id
    # 先查询是否有这个用户
    user = UserInfo.objects.filter(Q(username=open_id) | Q(token=open_id))
    if not user:
        # 没有这个用户
        return redirect('/login/')
    # 修改头像
    user.update(
        avatar_url=user_info[1],
        nick_name=user_info[0],
    )
    return redirect('/backend/')


# 添加文章
@is_super_fun
def add_article(request):
    # 拿到所有到分类，标签
    tag_list = Tags.objects.all()
    # 拿到所有的文章封面
    cover_list = Cover.objects.all()
    c_l = []
    for cover in cover_list:
        c_l.append({
            "url": cover.url.url,
            'nid': cover.nid
        })

    category_list = Articles.category_choice
    return render(request, 'backend/add_article.html', locals())


# 编辑文章
@is_super_fun
def edit_article(request, nid):
    article_obj = Articles.objects.get(nid=nid)
    tags = [str(tag.nid) for tag in article_obj.tag.all()]

    # 拿到所有到分类，标签
    tag_list = Tags.objects.all()
    # 拿到所有的文章封面
    cover_list = Cover.objects.all()
    c_l = []
    for cover in cover_list:
        c_l.append({
            "url": cover.url.url,
            'nid': cover.nid
        })
    category_list = Articles.category_choice
    return render(request, 'backend/edit_article.html', locals())


# 编辑头像
def edit_avatar(request):
    user = request.user
    sign_status = user.sign_status
    # 查询所有的头像
    avatar_list = Avatars.objects.all()

    if sign_status == 0:
        # 如果是用户名注册
        avatar_id = request.user.avatar.nid
    else:
        avatar_url = request.user.avatar_url
        for i in avatar_list:
            if i.url.url == avatar_url:
                avatar_id = i.nid
    return render(request, 'backend/edit_avatar.html', locals())


# 头像列表
@is_super_fun
def avatar_list(request):
    avatar_query = Avatars.objects.all()

    return render(request, 'backend/avatar_list.html', locals())


# 文章封面
@is_super_fun
def cover_list(request):
    cover_query = Cover.objects.all()
    return render(request, 'backend/cover_list.html', locals())


@is_super_fun
def admin_home(request):
    # 用户总数
    user_count = UserInfo.objects.count()
    article_count = Articles.objects.count()
    nav_count = Navs.objects.count()
    mood_count = Moods.objects.count()
    email_count = Email.objects.count()
    link_count = Navs.objects.filter(tag__title='博客').count()
    # 今日注册
    now = datetime.date.today()
    today_sign = UserInfo.objects.filter(
        date_joined__gte=now,
    ).count()

    return render(request, 'admin_home.html', locals())
