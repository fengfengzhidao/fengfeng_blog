from threading import Thread

from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail

from api.models import Email


class FeedBackAdmin(admin.ModelAdmin):
    list_display = ['email', 'content', 'status', 'processing_content']
    readonly_fields = ['email', 'content', 'status']

    def has_add_permission(self, request):
        return False

    def save_model(self, request, obj, form, change):  # change == True 编辑
        if not change:
            return
        # 编辑
        email = obj.email
        content = obj.content
        obj.status = True
        processing_content = form.data.get('processing_content')

        Thread(target=send_mail,
               args=(f'【枫枫知道】你反馈的信息：{content}被回复了！',
                     processing_content,
                     settings.EMAIL_HOST_USER,
                     [email, ],
                     False)).start()
        Email.objects.create(
            email=email,
            content=processing_content,
        )
        return super(FeedBackAdmin, self).save_model(request, obj, form, change)
