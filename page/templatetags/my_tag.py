import re

from django import template
from django.utils.safestring import mark_safe

from page.models import Tags, Menu, Articles
from lib.search import Search

# 注册
register = template.Library()


# 自定义过滤器
# @register.filter
# def add1(item):
#     return int(item) + 1


@register.inclusion_tag('my_tag/headers.html')
def banner(menu_name, article=None):
    if article:
        # 说明是文章详情页面
        # 拿到文章的封面
        cover = article.cover.url.url
        img_list = [cover]
        title = article.title
        slogan_list = [article.abstract[:30]]
        return locals()

    menu_obj = Menu.objects.get(menu_title_en=menu_name)
    img_list = [i.url.url for i in menu_obj.menu_url.all()]
    menu_time = menu_obj.menu_time
    title = menu_obj.title
    slogan_list = menu_obj.abstract.replace('；', ';').replace('\n', ';').split(';')
    slogan_time = menu_obj.abstract_time
    if not menu_obj.menu_rotation:
        # 如果不轮播
        img_list = img_list[0:1]
        menu_time = 0

    if not menu_obj.rotation:
        slogan_list = slogan_list[0:1]
        slogan_time = 0

    return locals()


@register.simple_tag
def generate_order_html(request, key):
    order = request.GET.get(key, '')
    order_list = []
    if key == 'order':
        order_list = [
            ('', '综合排序'),
            ('-create_date', '最新发布'),
            ('-look_count', '最多浏览'),
            ('-digg_count', '最多点赞'),
            ('-collects_count', '最多收藏'),
            ('-comment_count', '最多评论')
        ]
    elif key == 'word':
        order = request.GET.getlist(key, '')
        if order == '':
            order = ['']
        order_list = [
            ([''], '全部字数'),
            (['0', '100'], '100字以内'),
            (['100', '500'], '500字以内'),
            (['500', '1000'], '1000字以内'),
            (['1000', '3000'], '3000字以内'),
            (['3000', '5000'], '5000字以内'),
            (['5000', '1000'], '10000字以内'),
            (['10000'], '10000字以上'),
        ]
    elif key == 'tag':
        tag_list = Tags.objects.exclude(articles__isnull=True)
        order_list.append(('', '全部标签'))
        for tag in tag_list:
            order_list.append((tag.title, tag.title))

    query_params = request.GET.copy()

    order = Search(
        key=key,
        order=order,
        order_list=order_list,
        query_params=query_params
    )
    return mark_safe(order.order_html())


# 显示对于的图标和数字
@register.simple_tag
def show_article_icon(article, state):
    # 当前排序的状态
    correspond = {
        'digg': ['digg_count', 'fa-thumbs-up'],
        'look': ['look_count', 'fa-eye'],
        'collects': ['collects_count', 'fa-star'],
        'comment': ['comment_count', 'fa-comment'],
    }
    key = 'look'
    if state:
        word = re.search(r'[-](.*?)_.*?', state)
        key = word.group(1)
    attr = correspond.get(key, ['look_count', 'fa-eye'])
    number = getattr(article, attr[0])
    return mark_safe(f"""
    <i class="fa {attr[1]}"></i>
    {number}
    """)


# 生成标签
@register.simple_tag
def generate_tag_html():
    tag_list = Tags.objects.all()[:15]
    tag_html = []
    for tag in tag_list:
        if tag.articles_set.all():
            tag_html.append(f'<li>{tag.title} <i>{tag.articles_set.count()}</i></li>')
        else:
            tag_html.append(f'<li>{tag.title}</li>')
    return mark_safe(''.join(tag_html))


# 动态导航
@register.simple_tag
def dynamic_navigation(request):
    path = request.path_info
    path_dict = {
        '/': '首页',
        '/news/': '新闻',
        '/moods/': '心情',
        '/history/': '回忆录',
        '/about/': '关于',
        '/search/': '文章搜索',
        '/sites/': '网站导航',
        '/project/': '项目相关',
    }
    nav_list = []
    for k, v in path_dict.items():
        if k == path:
            nav_list.append(f'<a href="{k}" class="active">{v}</a>')
            continue
        nav_list.append(f'<a href="{k}">{v}</a>')

    return mark_safe(''.join(nav_list))


@register.simple_tag
def generate_drawing(drawing: str):
    if not drawing:
        return ''
    drawing = drawing.replace('；', ';').replace('\n', ';')
    drawing_list = drawing.split(';')
    html_s = ''
    for i in drawing_list:
        html_s += f'<img style="margin-right:10px; margin-top:5px;" src="{i}" alt="">'

    return mark_safe(html_s)


@register.simple_tag
def generate_li(content: str):
    if not content:
        return ''
    drawing = content.replace('；', ';').replace('\n', ';')
    drawing_list = drawing.split(';')
    html_s = ''
    for i in drawing_list:
        html_s += f'<li>{i}</li>'

    return mark_safe(html_s)


# 上一篇 下一篇
@register.simple_tag
def generate_p_n(article: Articles):
    article_list = list(Articles.objects.filter(category=article.category))
    now_index = article_list.index(article)
    max_index = len(article_list) - 1
    if now_index == 0:
        prev = '<a href="javascript:void (0);">已经是第一篇啦</a>'
    else:
        # 上一篇
        prev_article = article_list[article_list.index(article) - 1]
        prev = f'<a href="/article/{prev_article.nid}/">上一篇：{prev_article.title}</a>'
    if now_index == max_index:
        next = '<a href="javascript:void (0);">已经是最后一篇啦</a>'
    else:
        # 下一篇
        next_article = article_list[article_list.index(article) + 1]
        next = f'<a href="/article/{next_article.nid}/">下一篇：{next_article.title}</a>'

    return mark_safe(prev + next)


# 计算某个分类的文章数
@register.simple_tag
def calculation_category_count(cid):
    article_query = Articles.objects.filter(category=cid)
    return article_query.count()


@register.simple_tag
def get_article_query_nid(article_query):
    lis = []
    for i in article_query:
        lis.append(str(i.nid))

    return lis


# 根据配置生成对应的登录链接
@register.simple_tag
def gen_setting_login_url(name):
    from django.conf import settings
    if name == 'qq' or name == 1:
        return mark_safe(
            f'https://graph.qq.com/oauth2.0/show?which=Login&display=pc&response_type=code&client_id={settings.QQ_APPID}&redirect_uri={settings.QQ_REDIRECT}')
    elif name == 'gitee' or name == 2:
        return mark_safe(
            f'https://gitee.com/oauth/authorize?client_id={settings.GITEE_ID}&redirect_uri={settings.GITEE_REDIRECT}&response_type=code'
        )
    return ''

