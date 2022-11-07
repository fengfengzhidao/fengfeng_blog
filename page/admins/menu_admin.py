from django.contrib import admin
from django.utils.safestring import mark_safe
from page.models import Menu


class MenuAdmin(admin.ModelAdmin):
    add_form_template = 'simple_admin/add_form.html'

    change_form_template = 'simple_admin/add_form.html'

    def get_menu_url(self: Menu):
        lis = [f"<img src='{i.url.url}' style='height:60px; border-radius:5px; margin-right:5px; margin-bottom:5px;'>"
               for i in
               self.menu_url.all()]

        return mark_safe(''.join(lis))

    get_menu_url.short_description = '图片组'

    list_display = ['menu_title', 'menu_title_en',
                    'title', 'abstract',
                    'rotation', "abstract_time",
                    'menu_rotation', 'menu_time', get_menu_url]
