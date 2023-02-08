import datetime

import pendulum
from django import template
from django.utils.safestring import mark_safe

from page.models import Avatars, Cover, UserInfo

# 注册
register = template.Library()


# 用户是否收藏了文章
@register.filter
def is_user_collects(article, request):
    if str(request.user) == 'AnonymousUser':
        # 没有登录
        return ''
    if article in request.user.collects.all():
        return 'show'
    return ''


# 判断是否有文章内容
@register.filter
def is_article_list(article_list):
    if len(article_list):
        return 'search_content'
    return 'no_content'


# 时间格式化
@register.filter
def date_humaniz(date: datetime.datetime):
    if not date:
        return '--'
    pendulum.set_locale('zh')
    tz = pendulum.now().tz
    time_difference = pendulum.parse(date.strftime('%Y-%m-%d %H:%M:%S'), tz=tz).diff_for_humans()
    return time_difference


# 计算使用头像的总和
@register.filter
def to_calculate_avatar(avatar: Avatars):
    count = avatar.moodcomment_set.count() + avatar.moods_set.count() + avatar.userinfo_set.count()
    if count:
        return ''
    return 'no_avatar'


@register.filter
def to_calculate_cover(cover: Cover):
    count = cover.articles_set.count()
    if count:
        return ''
    return 'no_cover'


@register.filter
def get_tags(tag_list):
    return mark_safe(''.join([f"<i>{i.title}</i>" for i in tag_list]))


# 用户收藏的文章id列表
@register.filter
def get_coll_nid(lis):
    return [i.nid for i in lis]


@register.filter
def get_login(user):
    if user.sign_status in [1, 2]:
        return "show_reset_avatar"
    return ''


# 获取用户头像
@register.filter
def get_avatar(user: UserInfo):
    if user.sign_status in [1, 2]:
        return user.avatar_url
    if user.avatar:
        return user.avatar.url.url
    return ''


# 获取用户地址信息
@register.filter
def get_addr(addr: str):
    # return addr
    addr = eval(addr)
    if type(addr) is tuple:
        if addr[1] == "":
            return addr[0]
        return f"{addr[0]} · {addr[1]}"
    if type(addr) is dict:
        return f"{addr['prov']} · {addr['city']}"
    return ""


@register.filter
def generate_advert(adv_list):
    lis = []

    for i in adv_list:
        item = {}
        if i.img:  # 用户直接上传
            item['url'] = i.img.url
            item['title'] = i.title
            item['href'] = i.href
            lis.append(item)
        else:
            html_s: str = i.img_list
            html_new = html_s.replace('；', ';').replace('\n', ';')
            img_list = html_new.split(';')
            for u in img_list:
                item['url'] = u
                item['title'] = i.title
                item['href'] = i.href
                lis.append(item)
    return lis
