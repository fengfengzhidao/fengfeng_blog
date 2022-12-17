from django.shortcuts import render

from lib.pagination import Pagination
from page.models import *


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
    # 文章列表
    article_list = article_list[pager.start:pager.end]

    # 广告列表
    advert_list = Advert.objects.filter(is_show=True)

    # 文章封面列表
    cover_list = Cover.objects.all()

    link_list = Navs.objects.filter(tag__title='博客')

    # 在线人数
    online_count = len(request.online_list)

    return render(request, 'index.html', locals())