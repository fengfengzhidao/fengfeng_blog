# @Auth:fengfeng
# @Time:2022/01/02 19:27
from django.shortcuts import HttpResponse

from lib.random_code import random_code


# 获取随机验证码
def get_random_code(request):
    data, valid_code = random_code()
    request.session['valid_code'] = valid_code
    request.session['error_count'] = 0
    return HttpResponse(data)
