# @Time:2022/6/11 20:58
# @Author:fengfeng
import requests
from django.views import View
from django.http import JsonResponse

url = 'https://api.codelife.cc/api/top/list'


class NewsView(View):
    def post(self, request):
        headers = request.headers
        try:
            res = requests.post(url, data=request.data, headers={
                'signaturekey': headers['Signaturekey'],
                'version': '1.2.33',
            })
        except Exception:
            return {'code': 501, 'msg': '请求异常', 'data': []}
        return JsonResponse(res.json())
