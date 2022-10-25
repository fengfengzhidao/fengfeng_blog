# @Time:2022/9/2 8:41
# @Author:fengfeng
from django.conf import settings


def admin_media(request):
    return {
        'SITE_TITLE': settings.SITE_TITLE,
        'SITE_BEIAN': settings.SITE_BEIAN,
        'IS_ADVERTIS': settings.IS_ADVERTIS,
        'SITE_INFO': settings.SITE_INFO,
        'VERSION': settings.VERSION,
        'MUSIC_GROUP_ID': settings.MUSIC_GROUP_ID,
        'ONLINE_CHAT': settings.ONLINE_CHAT,
        'CALENDAR': settings.CALENDAR,
    }
