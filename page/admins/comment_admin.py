from django.contrib import admin
from django.utils.safestring import mark_safe
from page.models import Comment
import re


class CommentAdmin(admin.ModelAdmin):
    def get_content(self: Comment):
        content = self.content
        lis = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img style="width:15px; height:15px;margin: 0 5px;" src="\2" alt="\1">',
                     content, )
        return mark_safe(lis)

    get_content.short_description = '评论内容'
    list_display = ['user', get_content, 'article', 'create_time', 'comment_count']
