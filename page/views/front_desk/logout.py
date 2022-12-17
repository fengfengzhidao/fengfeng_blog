from django.contrib import auth
from django.shortcuts import redirect


# 注销
def logout(request):
    auth.logout(request)
    return redirect('/')