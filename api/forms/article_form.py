# @Time:2022/9/2 22:27
# @Author:fengfeng
# 添加文章或 编辑文章的验证
from django import forms
from markdown import markdown
from pyquery import PyQuery
import random
from page.models import Cover


class AddArticleForm(forms.Form):
    title = forms.CharField(error_messages={'required': '请输入文章标题'})
    content = forms.CharField(error_messages={'required': '请输入文章内容'})
    abstract = forms.CharField(required=False)  # 不进行为空验证
    cover_id = forms.CharField(required=False)  # 不进行为空验证
    category = forms.IntegerField(required=False)
    status = forms.IntegerField(required=False)
    pwd = forms.CharField(required=False)
    recommend = forms.BooleanField(required=False)
    word = forms.IntegerField(required=False)  # 文章字数

    # 文章简介
    def clean_abstract(self):
        abstract = self.cleaned_data['abstract']
        if abstract:
            return abstract
        # 截取正文的前30个字符
        content = self.cleaned_data.get('content')
        if content:
            abstract = PyQuery(markdown(content)).text()[:90]
            return abstract

    # 文章封面
    def clean_cover_id(self):
        cover_id = self.cleaned_data['cover_id']
        if cover_id:
            return cover_id
        cover_set = Cover.objects.all().values('nid')
        cover_id = random.choice(cover_set)['nid']
        return cover_id

    # 获取文章的字符个数
    def clean_word(self):
        return len(self.cleaned_data.get('content', ''))
