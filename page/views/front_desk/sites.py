from django.shortcuts import render

from page.models import *


# 网站导航页
def sites(request):
    # 取所有的标签
    tag_all = NavTags.objects.all()
    tag_list = tag_all.exclude(navs__isnull=True)

    return render(request, 'sites.html', locals())