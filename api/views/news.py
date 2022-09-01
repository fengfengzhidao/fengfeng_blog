import time

from django.views import View
from django.http import JsonResponse
import requests
# from lib.work_wechat import work
from lib.get_user_info import get_ip, get_addr_info

url = "https://api.codelife.cc/api/top/list"


class NewsView(View):
    def post(self, request):

        headers = request.headers
        Signaturekey: str = headers.get('Signaturekey')
        try:
            res = requests.post(url, data=request.data, headers={
                "signaturekey": Signaturekey,
                "version": '1.2.34',
                "origin": 'https://go.itab.link',
                'User-Agent': headers['User-Agent']
            }, timeout=2).json()
        except Exception:
            res = {'code': 501, 'msg': '请求错误', 'data': []}
        return JsonResponse(res)
