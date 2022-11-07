from django.contrib import admin


class NavsAdmin(admin.ModelAdmin):
    list_display = ['title']
