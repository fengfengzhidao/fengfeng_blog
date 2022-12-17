from django.shortcuts import render

from page.models import *


# 历史页
def history(request):
    history_list = History.objects.all().order_by('-create_date')
    return render(request, 'history.html', locals())