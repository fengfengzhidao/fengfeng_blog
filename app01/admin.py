from django.contrib import admin
from app01.models import *
from django.utils.safestring import mark_safe
from api.utils.qq_get_user import QQLogin
from django.core.mail import send_mail
from threading import Thread
from django.conf import settings
import re
from api.models import Email

admin.site.site_header = '枫枫知道个人博客'  # 登录框的文字
admin.site.site_title = '枫枫知道个人博客|后台系统'  # 浏览器头部信息


# 文章表
class ArticleAdmin(admin.ModelAdmin):
    def get_cover(self):
        if self.cover:
            return mark_safe(f'<img src="{self.cover.url.url}" style="height:60px; border-radius:5px;">')
        return

    get_cover.short_description = '文章封面'

    def get_tags(self):
        tag_list = ', '.join([i.title for i in self.tag.all()])
        return tag_list

    get_tags.short_description = '文章标签'

    def get_title(self):
        return mark_safe(f'<a href="/article/{self.nid}/" target="_blank">{self.title}</a>')

    get_title.short_description = '文章'

    def get_edit_delete_btn(self):
        return mark_safe(f"""
        <a href="/backend/edit_article/{self.nid}/" target="_blank">编辑</a>
        <a href="/admin/app01/articles/{self.nid}/delete/">删除</a>
        """)

    get_edit_delete_btn.short_description = '操作'

    list_display = [get_title,
                    get_cover, get_tags,
                    'category',
                    'look_count', 'digg_count', 'comment_count', 'collects_count', 'word',
                    'change_date',
                    get_edit_delete_btn, ]
    list_display_links = ['change_date']

    def action_word(self, request, queryset):
        for obj in queryset:
            word = len(obj.content)
            obj.word = word
            obj.save()

    action_word.short_description = '获取文章字数'

    def delete_comment(self, request, queryset):
        for article in queryset:
            article: Articles = article
            article.comment_set.all().delete()
            article.comment_count = 0
            article.save()

    delete_comment.short_description = '删除文章评论'
    action_word.type = 'success'

    actions = [action_word, delete_comment]


admin.site.register(Articles, ArticleAdmin)


# 用户信息
class UserInfoAdmin(admin.ModelAdmin):
    def get_avatar(self: UserInfo):
        if self.sign_status in [1, 2]:
            return mark_safe(f'<img src="{self.avatar_url}" style="width:30px;height:30px;border-radius:50%;">')

        if self.avatar:
            return mark_safe(f'<img src="{self.avatar.url.url}" style="width:30px;height:30px;border-radius:50%;">')

    get_avatar.short_description = '头像'

    def get_user_name(self):
        if not self.sign_status:
            return self.username
        return '****'

    get_user_name.short_description = '用户名'

    list_display = [get_user_name, 'nick_name', get_avatar, 'sign_status', 'ip', 'addr', 'is_superuser', 'date_joined', 'last_login']

    # 获取头像
    def get_avatar_action(self, request, queryset):
        for obj in queryset:
            if not obj.sign_status:
                continue
            # 其他平台注册的

    get_avatar_action.short_description = '获取用户信息'

    actions = [get_avatar_action]


admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Tags)
admin.site.register(Cover)


class CommentAdmin(admin.ModelAdmin):
    def get_content(self: Comment):
        content = self.content
        lis = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img style="width:15px; height:15px;margin: 0 5px;" src="\2" alt="\1">',
                     content, )
        return mark_safe(lis)

    get_content.short_description = '评论内容'
    list_display = ['user', get_content, 'article', 'create_time', 'comment_count']


admin.site.register(Comment, CommentAdmin)
admin.site.register(Avatars)


# 广告
class AdvertAdmin(admin.ModelAdmin):

    def get_href(self):
        return mark_safe(f"""<a href="{self.href}" target="_blank">跳转链接</a>""")

    get_href.short_description = '跳转链接'

    def get_img_list(self):
        # 解析分号;；
        # 解析换行符号\n
        html_s: str = self.img_list
        html_new = html_s.replace('；', ';').replace('\n', ';')
        img_list = html_new.split(';')

        html_str = ''
        for i in img_list:
            html_str += f'<img src="{i}" style="height:60px; border-radius:5px; margin-right:10px">'
        return mark_safe(html_str)

    get_img_list.short_description = '广告图组'

    def get_img(self):
        if self.img:
            return mark_safe(f"""<img src="{self.img.url}" style="height:60px; border-radius:5px">""")

    get_img.short_description = '用户上传'

    list_display = ['title', get_img, 'is_show', 'author', get_img_list, get_href]


admin.site.register(Advert, AdvertAdmin)


# 站点图片
class MenuIngAdmin(admin.ModelAdmin):
    def get_img(self):
        if self.url:
            return mark_safe(f"""<img src="{self.url.url}" style="height:60px; border-radius:5px">""")

    get_img.short_description = '背景图'
    list_display = ['url', get_img]


admin.site.register(MenuImg, MenuIngAdmin)


# 菜单
class MenuAdmin(admin.ModelAdmin):
    add_form_template = 'simple_admin/add_form.html'

    change_form_template = 'simple_admin/add_form.html'

    def get_menu_url(self: Menu):
        lis = [f"<img src='{i.url.url}' style='height:60px; border-radius:5px; margin-right:5px; margin-bottom:5px;'>"
               for i in
               self.menu_url.all()]

        return mark_safe(''.join(lis))

    get_menu_url.short_description = '图片组'

    list_display = ['menu_title', 'menu_title_en',
                    'title', 'abstract',
                    'rotation', "abstract_time",
                    'menu_rotation', 'menu_time', get_menu_url]


admin.site.register(Menu, MenuAdmin)


# 网站导航
class NavsAdmin(admin.ModelAdmin):
    list_display = ['title']


admin.site.register(Navs, NavsAdmin)


# 意见反馈
class FeedBackAdmin(admin.ModelAdmin):
    list_display = ['email', 'content', 'status', 'processing_content']
    readonly_fields = ['email', 'content', 'status']

    def has_add_permission(self, request):
        return False

    def save_model(self, request, obj, form, change):  # change == True 编辑
        if not change:
            return
        # 编辑
        email = obj.email
        content = obj.content
        obj.status = True
        processing_content = form.data.get('processing_content')

        Thread(target=send_mail,
               args=(f'【枫枫知道】你反馈的信息：{content}被回复了！',
                     processing_content,
                     settings.EMAIL_HOST_USER,
                     [email, ],
                     False)).start()
        Email.objects.create(
            email=email,
            content=processing_content,
        )
        return super(FeedBackAdmin, self).save_model(request, obj, form, change)


admin.site.register(Feedback, FeedBackAdmin)


# 项目相关
class ProjectAdmin(admin.ModelAdmin):

    def get_article(self: Project):
        article_list = []
        for i in self.article.all():
            article_list.append(i.title)
        return mark_safe(' ,  '.join(article_list))

    get_article.short_description = '文章列表'
    list_display = ['title', get_article]


admin.site.register(Project, ProjectAdmin)
