import requests
from django.http import JsonResponse
from django.views import View

url = "https://api.codelife.cc/api/top/list"


class NewsView(View):
    def post(self, request):

        headers = request.headers
        encryption_key: str = headers.get('Signaturekey')
        try:
            res = requests.post(url, data=request.data, headers={
                "signaturekey": encryption_key,
                "version": '1.2.34',
                "origin": 'https://go.itab.link',
                'User-Agent': headers['User-Agent']
            }, timeout=2).json()
        except Exception:
            res = {'code': 501, 'msg': '请求错误', 'data': []}
        return JsonResponse(res)
