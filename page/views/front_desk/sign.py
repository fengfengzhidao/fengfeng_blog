from django.shortcuts import render


# 注册
def sign(request):
    return render(request, 'sign.html')
