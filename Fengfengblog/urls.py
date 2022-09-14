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
from django.contrib import admin
from django.urls import path, include, re_path
from page.views import index, backend
from django.conf import settings  ##新增
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),

    path('admin_home/', backend.admin_home),

    path('', index.index),
    path('news/', index.news),
    path('about/', index.about),
    path('sites/', index.sites),
    path('moods/', index.moods),
    path('history/', index.history),
    path('search/', index.search),
    path('project/', index.project),

    path('login/', index.login),
    path('oauth/', index.oauth),  # 三方登录之后的回调
    path('login/random_code/', index.get_random_code),
    path('sign/', index.sign),
    path('logout/', index.logout),

    re_path(r'^article/(?P<nid>\d+)/', index.article),  # 文章详情页

    path('backend/', backend.backend),  # 后台个人中心
    path('backend/add_article/', backend.add_article),  # 后台添加文章
    path('backend/edit_avatar/', backend.edit_avatar),  # 后台修改头像

    path('backend/cover_list/', backend.cover_list),  # 文章封面
    path('backend/avatar_list/', backend.avatar_list),  # 头像列表

    re_path(r'^backend/edit_article/(?P<nid>\d+)/', backend.edit_article),  # 编辑文章

    re_path(r'^api/', include('api.urls')),  # 路由分发  将所有已api开头的请求分发到api这个urls.py中

    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),  # 用户上传文件路由配置

]
