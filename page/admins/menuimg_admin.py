from django.contrib import admin
from django.utils.safestring import mark_safe
from page.models import MenuImg


class MenuImgAdmin(admin.ModelAdmin):
    def get_img(self: MenuImg):
        if self.url:
            return mark_safe(f"""<img src="{self.url.url}" style="height:60px; border-radius:5px">""")

    get_img.short_description = '背景图'
    list_display = ['url', get_img]
