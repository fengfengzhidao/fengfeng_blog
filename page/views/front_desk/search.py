from django.shortcuts import render

from lib.pagination import Pagination
from page.models import *


# 搜索
def search(request):
    """

    """
    search_key = request.GET.get('key', '')
    order = request.GET.get('order', '')
    tag = request.GET.get('tag', '')
    word = request.GET.getlist('word')

    query_params = request.GET.copy()

    article_list = Articles.objects.filter(title__contains=search_key)

    # 字数搜索
    if word:
        if len(word) == 1 and word[0] != '':
            article_list = article_list.filter(word__gte=word[0])
        elif len(word) == 2:
            article_list = article_list.filter(word__range=word)

    if tag:
        article_list = article_list.filter(tag__title=tag)

    if order:
        try:
            article_list = article_list.order_by(order)
        except Exception:
            pass

    # 分页器
    pager = Pagination(
        current_page=request.GET.get('page'),
        all_count=article_list.count(),
        base_url=request.path_info,
        query_params=query_params,
        per_page=10,
        pager_page_count=7
    )
    article_list = article_list[pager.start:pager.end]

    return render(request, 'search.html', locals())