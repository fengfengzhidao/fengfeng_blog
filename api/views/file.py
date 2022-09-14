import base64

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.http import JsonResponse
from django.views import View

from page.models import Avatars, Cover, UserInfo
from page.models import avatar_delete, cover_delete
from lib.api_qiniu import upload_data
from lib.permissions_control import is_super_method


# 头像
class AvatarView(View):
    @is_super_method
    def post(self, request: WSGIRequest):
        res = {
            "code": 345,
            'msg': '文件上传不合法！'
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)
        file: InMemoryUploadedFile = request.FILES.get('file')
        name: str = file.name
        # 使用白名单的方式，如果不在白名单就是不合法的文件
        white_file_type = [
            'jpg', 'jpeg', 'png', 'webp'
        ]
        if name.split('.')[-1] not in white_file_type:
            return JsonResponse(res)

        kb = file.size / 1024 / 1024
        if kb > 2:
            res['msg'] = '图片大小超过2MB'
            return JsonResponse(res)
        Avatars.objects.create(url=file)
        res['code'] = 0
        res['msg'] = 'success'
        return JsonResponse(res)

    @is_super_method
    def delete(self, request, nid):

        res = {
            'code': 322,
            'msg': '图片删除成功！'
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)
        avatar_query = Avatars.objects.filter(nid=nid)
        if not avatar_query:
            res['msg'] = '图片已被删除！'
            return JsonResponse(res)
        # 判断图片是不是有人在使用
        obj: Avatars = avatar_query.first()

        user_query = UserInfo.objects.filter(Q(sign_status=1) | Q(sign_status=2))
        for user in user_query:
            if obj.url.url == user.avatar_url:
                res['msg'] = '该图片有人使用！'
                return JsonResponse(res)
        avatar_delete(obj)
        avatar_query.delete()

        res['code'] = 0
        return JsonResponse(res)


# 封面
class CoverView(View):
    @is_super_method
    def post(self, request: WSGIRequest):
        res = {
            "code": 345,
            'msg': '文件上传不合法！'
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)
        file: InMemoryUploadedFile = request.FILES.get('file')
        name: str = file.name
        white_file_type = [
            'jpg', 'jpeg', 'png'
        ]
        if name.split('.')[-1] not in white_file_type:
            return JsonResponse(res)

        kb = file.size / 1024 / 1024
        if kb > 2:
            res['msg'] = '图片大小超过2MB'
            return JsonResponse(res)
        Cover.objects.create(url=file)
        res['code'] = 0
        res['msg'] = 'success'
        return JsonResponse(res)

    @is_super_method
    def delete(self, request, nid):

        res = {
            'code': 322,
            'msg': '图片删除成功！'
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)
        cover_query = Cover.objects.filter(nid=nid)
        if not cover_query:
            res['msg'] = '图片已被删除！'
            return JsonResponse(res)
        cover_delete(cover_query.first())
        cover_query.delete()

        res['code'] = 0
        return JsonResponse(res)


# 粘贴上传
class PasteUpload(View):
    @is_super_method
    def post(self, request):
        img = request.data.get('image')
        ines = img.split('base64,')
        imgData = base64.b64decode(ines[1])
        url = upload_data(imgData)
        return JsonResponse({'url': url})
