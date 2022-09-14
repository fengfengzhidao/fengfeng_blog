from django.urls import path, re_path

from api.views import admin_data
from api.views import api_email
from api.views import article
from api.views import comment
from api.views import file
from api.views import history
from api.views import login
from api.views import mood
from api.views import news
from api.views import sites
from api.views import user

urlpatterns = [
    path('login/', login.LoginView.as_view()),  # 登录

    path('sign/', login.SignView.as_view()),  # 注册

    path('get_online/', admin_data.get_online),  # 获取在线人数

    path('get_seven_data/', admin_data.get_seven_data),  # 七日数据

    path('article/', article.ArticleView.as_view()),  # 发布文章

    # 注意这里的顺序，这个要在修改文章的前面，不然会被他捕获到
    re_path(r'article/(?P<nid>\d+)/comment/', comment.CommentView.as_view()),  # 发布评论

    re_path(r'article/(?P<nid>\d+)/', article.ArticleView.as_view()),  # 修改文章

    re_path(r'article_pwd/(?P<nid>\d+)/', article.ArticlePwdView.as_view()),  # 查看加密文章

    re_path(r'comment/digg/(?P<nid>\d+)/', comment.CommentDiggView.as_view()),  # 评论点赞

    re_path(r'article/digg/(?P<nid>\d+)/', article.ArticleDiggView.as_view()),  # 文章点赞

    re_path(r'article/cover/(?P<nid>\d+)/', article.EditArticleCoverView.as_view()),  # 文章修改封面

    re_path(r'article/collects/(?P<nid>\d+)/', article.ArticleCollectsView.as_view()),  # 文章收藏

    path('projects/', article.ProjectArticleView.as_view()),  # 发布项目

    re_path(r'projects/(?P<nid>\d+)/', article.ProjectArticleView.as_view()),  # 修改项目

    path('moods/', mood.MoodsView.as_view()),  # 发布心情

    re_path(r'moods/(?P<nid>\d+)/', mood.MoodsView.as_view()),  # 删除心情

    re_path(r'mood_comments/(?P<nid>\d+)/', mood.MoodCommentsView.as_view()),  # 发布心情评论

    path('history/', history.HistoryView.as_view()),  # 发布记录

    re_path(r'history/(?P<nid>\d+)/', history.HistoryView.as_view()),  # 编辑记录

    path('site_tag/', sites.NavTagsView.as_view()),  # 发布网站标签

    re_path(r'site_tag/(?P<nid>\d+)/', sites.NavTagsView.as_view()),  # 编辑网站标签

    path('sites/', sites.NavView.as_view()),  # 获取网站数据列表

    re_path(r'sites/(?P<nid>\d+)/', sites.NavView.as_view()),  # 编辑网站数据

    re_path(r'site_digg/(?P<nid>\d+)/', sites.NavDiggView.as_view()),  # 网站点赞

    re_path(r'site_coll/(?P<nid>\d+)/', sites.NavCollectsView.as_view()),  # 网站收藏

    path('friends_links/', sites.FriendLinks.as_view()),  # 添加友链

    path('edit_password/', user.EditPasswordView.as_view()),  # 修改密码

    path('edit_avatar/', user.EditAvatarView.as_view()),  # 修改头像

    path('upload/avatar/', file.AvatarView.as_view()),  # 上传头像

    path('upload/cover/', file.CoverView.as_view()),  # 上传封面

    re_path(r'upload/avatar/(?P<nid>\d+)/', file.AvatarView.as_view()),  # 删除头像

    re_path(r'upload/cover/(?P<nid>\d+)/', file.CoverView.as_view()),  # 删除封面

    path('paste_upload/', file.PasteUpload.as_view()),  # 粘贴上传

    path('send_email/', api_email.ApiEmail.as_view()),  # 发送邮箱

    path('perfect_information/', user.EditUserInfoView.as_view()),  # 绑定信息

    path('cancel_collection/', user.CancelCollection.as_view()),  # 取消收藏

    path('reset_avatar/', user.ResetAvatarView.as_view()),  # 重置头像  qq  gitee  # TODO：废弃

    path('feedback/', user.FeedBackView.as_view()),  # 意见反馈

    path('news/', news.NewsView.as_view()),  # 新闻

]
