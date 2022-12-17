from django.db.models import F
from django.shortcuts import render, redirect

from lib.sub_comment import sub_comment_list
from page.models import *


# 关于页
def about(request):
    # 编号37的文章
    article_query = Articles.objects.filter(nid=37)

    article_query.update(look_count=F('look_count') + 1)
    if not article_query:
        return redirect('/')
    article_obj: Articles = article_query.first()

    comment_list = sub_comment_list(37)

    return render(request, 'about.html', locals())