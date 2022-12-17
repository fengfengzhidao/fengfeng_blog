"""Fengfengblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings  ##新增
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from page.views import backend
from page.views.front_desk.article import article
from page.views.front_desk.history import history
from page.views.front_desk.index import index
from page.views.front_desk.moods import moods
from page.views.front_desk.news import news
from page.views.front_desk.oauth import oauth
from page.views.front_desk.search import search
from page.views.front_desk.sign import sign
from page.views.front_desk.sites import sites
from page.views.front_desk.about import about
from page.views.front_desk.project import project
from page.views.front_desk.login import login
from page.views.front_desk.logout import logout
from page.views.front_desk.get_random_code import get_random_code

urlpatterns = [
    path('admin/', admin.site.urls),  # 后台
    path('admin_home/', backend.admin_home),  # 后台的看板
    path('', index),  # 首页
    path('news/', news),  # 新闻
    path('about/', about),  # 关于
    path('sites/', sites),  # 网站导航
    path('moods/', moods),  # 心情
    path('history/', history),  # 网站历史
    path('search/', search),  # 搜索
    path('project/', project),  # 项目
    path('login/', login),  # 登录
    path('oauth/', oauth),  # 三方登录之后的回调
    path('login/random_code/', get_random_code),  # 图片验证码
    path('sign/', sign),  # 注册
    path('logout/', logout),  # 注销
    re_path(r'^article/(?P<nid>\d+)/', article),  # 文章详情页
    path('backend/', backend.backend),  # 后台个人中心
    path('backend/add_article/', backend.add_article),  # 后台添加文章
    path('backend/edit_avatar/', backend.edit_avatar),  # 后台修改头像
    path('backend/cover_list/', backend.cover_list),  # 文章封面
    path('backend/avatar_list/', backend.avatar_list),  # 头像列表
    re_path(r'^backend/edit_article/(?P<nid>\d+)/', backend.edit_article),  # 编辑文章
    re_path(r'^api/', include('api.urls')),  # 路由分发  将所有已api开头的请求分发到api这个urls.py中
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),  # 用户上传文件路由配置

]
