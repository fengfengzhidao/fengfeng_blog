from django.shortcuts import render

from lib.pagination import Pagination
from page.models import *


# 心情页
def moods(request):
    # 查询所有的头像
    avatar_list = Avatars.objects.all()

    # 搜索
    key = request.GET.get('key', '')

    mood_list = Moods.objects.filter(content__contains=key).order_by('-create_date')

    # 分页器
    query_params = request.GET.copy()

    pager = Pagination(
        current_page=request.GET.get('page'),
        all_count=mood_list.count(),
        base_url=request.path_info,
        query_params=query_params,
        per_page=5,
        pager_page_count=7
    )
    mood_list = mood_list[pager.start:pager.end]

    return render(request, 'moods.html', locals())