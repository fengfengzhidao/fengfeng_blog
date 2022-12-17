from django.shortcuts import render

from page.models import *


# 项目相关
def project(request):
    project_list = Project.objects.all()
    article_query = Articles.objects.all()

    return render(request, 'blog.html', locals())
