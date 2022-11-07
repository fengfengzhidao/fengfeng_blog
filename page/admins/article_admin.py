from django.contrib import admin
from django.utils.safestring import mark_safe

from page.models import Articles


class ArticleAdmin(admin.ModelAdmin):
    def get_cover(self: Articles):
        if self.cover:
            return mark_safe(f'<img src="{self.cover.url.url}" style="height:60px; border-radius:5px;">')
        return

    get_cover.short_description = '文章封面'

    def get_tags(self: Articles):
        tag_list = ', '.join([i.title for i in self.tag.all()])
        return tag_list

    get_tags.short_description = '文章标签'

    def get_title(self: Articles):
        return mark_safe(f'<a href="/article/{self.nid}/" target="_blank">{self.title}</a>')

    get_title.short_description = '文章'

    def get_edit_delete_btn(self: Articles):
        return mark_safe(f"""
        <a href="/backend/edit_article/{self.nid}/" target="_blank">编辑</a>
        <a href="/admin/app01/articles/{self.nid}/delete/">删除</a>
        """)

    get_edit_delete_btn.short_description = '操作'

    list_display = [get_title,
                    get_cover, get_tags,
                    'category',
                    'look_count', 'digg_count', 'comment_count', 'collects_count', 'word',
                    'change_date',
                    get_edit_delete_btn, ]
    list_display_links = ['change_date']

    def action_word(self, request, queryset):
        for obj in queryset:
            word = len(obj.content)
            obj.word = word
            obj.save()

    action_word.short_description = '获取文章字数'

    def delete_comment(self, request, queryset):
        for article in queryset:
            article: Articles = article
            article.comment_set.all().delete()
            article.comment_count = 0
            article.save()

    delete_comment.short_description = '删除文章评论'
    action_word.type = 'success'

    actions = [action_word, delete_comment]
