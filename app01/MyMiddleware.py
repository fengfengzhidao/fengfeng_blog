import json

from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

from lib.get_user_info import get_ip


class StatisticalMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = get_ip(request)
        online_ips = list(cache.get("online_ips", []))

        if online_ips:
            online_ips = list(cache.get_many(online_ips).keys())

        cache.set(ip, 0, 10)  # 超时时间 单位：秒

        if ip not in online_ips:
            online_ips.append(ip)

        cache.set("online_ips", online_ips)

        request.online_list = online_ips


# 解析post请求的数据
class DecodeBodyDataMiddleware(MiddlewareMixin):
    # 请求中间件
    def process_request(self, request):
        if request.method != 'GET' and request.META.get('CONTENT_TYPE') == 'application/json':
            data = json.loads(request.body)
            request.data = data

    # 响应中间件
    def process_response(self, request, response):
        return response
