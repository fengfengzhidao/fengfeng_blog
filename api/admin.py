from django.contrib import admin
from api.models import Email


class EmailAdmin(admin.ModelAdmin):
    list_display = ['email', 'content', 'create_date']


admin.site.register(Email, EmailAdmin)
