from django.http import JsonResponse
from django.views import View
from django.core.handlers.wsgi import WSGIRequest
from django.utils.datastructures import MultiValueDict


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
        return JsonResponse({"data": f"/{file_name}", "code": 0, "msg": "上传成功"})
