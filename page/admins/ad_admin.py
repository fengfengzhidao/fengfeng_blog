from django.contrib import admin
from django.utils.safestring import mark_safe
from page.models import Advert


class AdvertAdmin(admin.ModelAdmin):

    def get_href(self: Advert):
        return mark_safe(f"""<a href="{self.href}" target="_blank">跳转链接</a>""")

    get_href.short_description = '跳转链接'

    def get_img_list(self: Advert):
        # 解析分号;；
        # 解析换行符号\n
        html_s: str = self.img_list
        html_new = html_s.replace('；', ';').replace('\n', ';')
        img_list = html_new.split(';')

        html_str = ''
        for i in img_list:
            html_str += f'<img src="{i}" style="height:60px; border-radius:5px; margin-right:10px">'
        return mark_safe(html_str)

    get_img_list.short_description = '广告图组'

    def get_img(self: Advert):
        if self.img:
            return mark_safe(f"""<img src="{self.img.url}" style="height:60px; border-radius:5px">""")

    get_img.short_description = '用户上传'

    list_display = ['title', get_img, 'is_show', 'author', get_img_list, get_href]
