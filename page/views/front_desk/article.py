from django.db.models import F
from django.shortcuts import render, redirect

from lib.sub_comment import sub_comment_list
from page.models import *


# 文章详情页
def article(request, nid):
    """

    """
    article_query = Articles.objects.filter(nid=nid)

    article_query.update(look_count=F('look_count') + 1)
    if not article_query:
        return redirect('/')
    article_obj: Articles = article_query.first()
    comment_list = sub_comment_list(nid)

    if article_obj.pwd:

        pwd = request.session.get(f'article_pwd__{nid}')
        if pwd == article_obj.pwd:
            # 已经输入了成功的密码
            return render(request, 'article.html', locals())

        return render(request, 'article_lock.html', locals())

    return render(request, 'article.html', locals())