from django.contrib import admin

from page.models import *
from .admins.ad_admin import AdvertAdmin
from .admins.article_admin import ArticleAdmin
from .admins.comment_admin import CommentAdmin
from .admins.feedback_admin import FeedBackAdmin
from .admins.menu_admin import MenuAdmin
from .admins.menuimg_admin import MenuImgAdmin
from .admins.navs_admin import NavsAdmin
from .admins.project_admin import ProjectAdmin
from .admins.user_admin import UserInfoAdmin

admin.site.site_header = '枫枫知道个人博客'  # 登录框的文字
admin.site.site_title = '枫枫知道个人博客|后台系统'  # 浏览器头部信息

admin.site.register(Articles, ArticleAdmin)  # 文章表
admin.site.register(UserInfo, UserInfoAdmin)  # 用户信息
admin.site.register(Tags)  # 文章标签
admin.site.register(Cover)  # 文章封面
admin.site.register(Comment, CommentAdmin)  # 文章评论
admin.site.register(Avatars)  # 用户头像
admin.site.register(Advert, AdvertAdmin)  # 广告
admin.site.register(MenuImg, MenuImgAdmin)  # 站点图片
admin.site.register(Menu, MenuAdmin)  # 菜单
admin.site.register(Feedback, FeedBackAdmin)  # 意见反馈
admin.site.register(Project, ProjectAdmin)  # 项目相关
admin.site.register(Navs, NavsAdmin)  # 网站导航
