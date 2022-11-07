from django.contrib import admin
from django.utils.safestring import mark_safe

from page.models import UserInfo


class UserInfoAdmin(admin.ModelAdmin):
    def get_avatar(self: UserInfo):
        if self.sign_status in [1, 2]:
            return mark_safe(f'<img src="{self.avatar_url}" style="width:30px;height:30px;border-radius:50%;">')

        if self.avatar:
            return mark_safe(f'<img src="{self.avatar.url.url}" style="width:30px;height:30px;border-radius:50%;">')

    get_avatar.short_description = '头像'

    def get_user_name(self):
        if not self.sign_status:
            return self.username
        return '****'

    get_user_name.short_description = '用户名'

    list_display = [get_user_name, 'nick_name', get_avatar, 'sign_status', 'ip', 'addr', 'is_superuser', 'date_joined',
                    'last_login']

    # 获取头像
    def get_avatar_action(self, request, queryset):
        for obj in queryset:
            if not obj.sign_status:
                continue
            # 其他平台注册的

    get_avatar_action.short_description = '获取用户信息'

    actions = [get_avatar_action]
