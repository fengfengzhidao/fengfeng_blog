from django.shortcuts import render


def news(request):
    """
    新闻页，在页面中，注意itab的接口，需要改一下请求头
    """
    return render(request, 'news.html')