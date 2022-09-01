from django.http import JsonResponse
from django.shortcuts import redirect


# 视图函数权限验证
def is_super_fun(fun):
    def inner(*args, **kwargs):
        request = args[0]
        if not request.user.is_superuser:
            return redirect('/')
        res = fun(*args, **kwargs)
        return res

    return inner


# api权限验证
def is_super_method(fun):
    def inner(*args, **kwargs):
        request = args[1]
        if not request.user.is_superuser:
            res = {
                'code': 555,
                'msg': '权限验证失败'
            }
            return JsonResponse(res)
        res = fun(*args, **kwargs)
        return res

    return inner
