from django.views import View
from django.core.handlers.wsgi import WSGIRequest
from lib.response.response import *

class ImageView(View):
    """
    图片上传
    """

    def post(self, request: WSGIRequest):
        file = request.FILES.get('file')
        file_name = f'media/uploads/{file.name}'
        with open(file_name, 'wb+') as pic:
            for c in file.chunks():
                pic.write(c)
        return ok(f"/{file_name}", "上传成功")
