import datetime

from django.http import JsonResponse

from page.models import UserInfo


# 获取在线人数
def get_online(request):
    return JsonResponse({'data': len(request.online_list)})


# 获取七日内数据
def get_seven_data(request):
    # TODO:这里应该是有个问题的，同一个人，后面登录的时间会把上次登录的时间覆盖，造成统计不准
    today = datetime.date.today()
    seven_data = {
        'date': [],
        'login_count': [],
        'sign_count': [],
    }
    for i in range(6, -1, -1):
        date = today - datetime.timedelta(days=i)
        # 登录人数
        login_count = UserInfo.objects.filter(
            last_login__year=date.year,
            last_login__month=date.month,
            last_login__day=date.day,
        ).count()
        sign_count = UserInfo.objects.filter(
            date_joined__year=date.year,
            date_joined__month=date.month,
            date_joined__day=date.day,
        ).count()
        seven_data['date'].append(date.strftime('%m-%d'))
        seven_data['login_count'].append(login_count)
        seven_data['sign_count'].append(sign_count)

    return JsonResponse(seven_data)
