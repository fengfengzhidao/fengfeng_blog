import os
from hashlib import md5

from django.conf import settings
from django.template import Template, Context


def my_render(template_name, context):
    # template_name 模板文件的位置，父目录是template
    path = os.path.join(settings.BASE_DIR, 'templates/', template_name)

    with open(path, 'r', encoding='utf8')as f:
        html_data = f.read()
    c = Context(context)  # 添加变量
    t = Template(html_data)  # 渲染模板
    return t.render(c)  # 返回模板


def my_md5(string):
    # 待加密信息 string
    # 创建md5对象
    hl = md5(string.encode('utf8'))
    return hl.hexdigest()
