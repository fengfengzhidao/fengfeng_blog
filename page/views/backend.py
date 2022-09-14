import datetime

from django.shortcuts import render, redirect

from api.models import *
from page.models import *
from lib.permissions_control import is_super_fun
from page.models import UserInfo


# 后台
def backend(request):
    if not request.user.username:
        # 没有登录
        return redirect('/')

    user: UserInfo = request.user
    collects_query = user.collects.all()
    return render(request, 'backend/backend.html', locals())


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
