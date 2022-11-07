from django.contrib import admin
from django.utils.safestring import mark_safe

from page.models import Project


class ProjectAdmin(admin.ModelAdmin):

    def get_article(self: Project):
        article_list = []
        for i in self.article.all():
            article_list.append(i.title)
        return mark_safe(' ,  '.join(article_list))

    get_article.short_description = '文章列表'
    list_display = ['title', get_article]