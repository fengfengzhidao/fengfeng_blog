# @Auth:fengfeng
# @Time:2021/12/31 19:51

"""
主体表结构
UserInfo
Avatars
...
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_delete  # 删除文件
from django.dispatch.dispatcher import receiver  # 删除文件
from django.utils.html import format_html


# 用户表
class UserInfo(AbstractUser):
    """
    nick:昵称
    avatar_url:用户头像
    tel:手机号
    integral：用户积分
    token:第三方登录的ID
    ip:IP地址
    addr:用户的地址
    sign_status:注册来源
    account_status:账号的状态
    avatar：头像表
    collects：收藏的文章
    navs:用户收藏的网站
    """
    nid = models.AutoField(primary_key=True)
    nick_name = models.CharField(max_length=16, verbose_name='昵称', null=True, blank=True)
    avatar_url = models.URLField(verbose_name='用户头像', help_text='可能是其他平台的头像', null=True, blank=True)
    tel = models.CharField(verbose_name='手机号', max_length=12, null=True, blank=True)
    integral = models.IntegerField(default=20, verbose_name='用户积分')
    token = models.CharField(verbose_name='id', help_text='其他平台的唯一登录id', max_length=64, null=True, blank=True)
    ip = models.GenericIPAddressField(verbose_name='ip地址', default='120.228.2.238')
    addr = models.TextField(verbose_name='用户地址信息', null=True, blank=True)
    sign_choice = (
        (0, '用户名注册'),
        (1, 'QQ注册'),
        (2, 'gitee注册'),
        (3, '手机号注册'),
        (4, '邮箱注册'),
    )
    sign_status = models.IntegerField(default=0, choices=sign_choice, verbose_name='注册方式')
    account_status_choice = (
        (0, '账号正常'),
        (1, '账号异常'),
        (2, '账号被封禁'),
    )
    account_status = models.IntegerField(default=0, choices=account_status_choice, verbose_name='账号状态')
    avatar = models.ForeignKey(
        to='Avatars',
        to_field='nid',
        on_delete=models.SET_NULL,
        verbose_name='用户头像',
        null=True,
        blank=True,
    )
    collects = models.ManyToManyField(
        to='Articles',
        verbose_name='收藏的文章',
        blank=True
    )
    navs = models.ManyToManyField(
        to='Navs',
        verbose_name='收藏的网站',
        blank=True
    )

    class Meta:
        verbose_name_plural = '用户'


# 用户头像表
class Avatars(models.Model):
    """
    url: 头像的链接，完整url: .url
    """
    nid = models.AutoField(primary_key=True)
    url = models.FileField(verbose_name='用户头像地址', upload_to='avatars/')

    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name_plural = '用户头像'


# 删除头像
@receiver(pre_delete, sender=Avatars)  # sender=你要删除或修改文件字段所在的类**
def avatar_delete(instance, **kwargs):  # 函数名随意
    # print('进入文件删除方法，删的是', instance.url)  # 用于测试
    instance.url.delete(False)  # file是保存文件或图片的字段名**


# 文章表
class Articles(models.Model):
    """
    title：文章标题
    abstract：文章简介
    content：文章内容
    create_date：创建日期
    change_date：编辑的最新日期
    status：文章的状态，默认都是已发布
    recommend：是否上推荐
    cover：文章封面  一对多
    look_count：浏览量
    comment_count：评论数
    digg_count：点赞数
    collects_count：收藏数
    category：文章分类
    tag：文章标签 多对多
    pwd：文章密码
    author：文章的作者  后续可以做一对多，关联用户表
    source：文章的来源
    link：来源地址
    word：文章字数
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标题', max_length=32, null=True, blank=True)
    abstract = models.CharField(verbose_name='文章简介', max_length=128, null=True, blank=True)
    content = models.TextField(verbose_name='文章内容', null=True, blank=True)
    create_date = models.DateTimeField(verbose_name='文章发布日期', auto_now_add=True, null=True)
    change_date = models.DateTimeField(verbose_name='文章修改日期', auto_now=True, null=True)
    status_choice = (
        (0, '未发布'),
        (1, '已发布'),
    )
    status = models.IntegerField(verbose_name='文章保存状态', choices=status_choice)
    recommend = models.BooleanField(verbose_name='是否上推荐', default=True)
    cover = models.ForeignKey(
        to='Cover',
        to_field='nid',
        on_delete=models.SET_NULL,
        verbose_name='文章封面', null=True, blank=True
    )
    look_count = models.IntegerField(verbose_name='文章阅读量', default=0)
    comment_count = models.IntegerField(verbose_name='文章评论量', default=0)
    digg_count = models.IntegerField(verbose_name='文章点赞量', default=0)
    collects_count = models.IntegerField(verbose_name='文章收藏数', default=0)
    category_choice = (
        (1, '前端'),
        (2, '后端'),
        (3, '项目相关'),
    )
    category = models.IntegerField(verbose_name='文章分类', choices=category_choice, null=True, blank=True)
    tag = models.ManyToManyField(
        to='Tags',
        verbose_name='文章标签',
        blank=True
    )
    pwd = models.CharField(max_length=32, verbose_name='文章密码', null=True, blank=True)
    author = models.CharField(max_length=16, verbose_name='作者', null=True, blank=True)
    source = models.CharField(max_length=32, verbose_name='来源', null=True, blank=True)

    link = models.URLField(verbose_name='文章链接', null=True, blank=True)
    word = models.IntegerField(verbose_name='文章字数', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '文章'


# 项目分类
class Project(models.Model):
    """
    title：项目的标题
    article：项目关联的文章  多对多
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标题', max_length=32, null=True, blank=True)
    article = models.ManyToManyField(
        verbose_name='文章',
        to='Articles'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '项目相关'


# 评论表
class Comment(models.Model):
    """
    digg_count：点赞数
    article：关联的文章  一对多
    user：关联的用户  一对多
    content： 评论内容
    comment_count： 子评论数
    drawing：配图
    create_time： 创建时间
    parent_comment： 父评论，根评论的父评论为None
    """
    nid = models.AutoField(primary_key=True)
    digg_count = models.IntegerField(verbose_name='点赞', default=0)
    article = models.ForeignKey(verbose_name='评论文章', to='Articles', to_field='nid', on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='nid', on_delete=models.CASCADE, null=True)
    content = models.TextField(verbose_name='评论内容')
    comment_count = models.IntegerField(verbose_name='子评论数', default=0)
    drawing = models.TextField(verbose_name='配图', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name='是否是父评论')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = '评论'


# 文章封面
class Cover(models.Model):
    nid = models.AutoField(primary_key=True)
    url = models.FileField(verbose_name='文章封面地址', upload_to='article_img/')
    dominant_hue = models.CharField(verbose_name='封面主色调', max_length=16, null=True, blank=True)
    is_dark = models.BooleanField(verbose_name='是否是深色系', null=True, blank=True)

    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name_plural = '文章封面'


# 删除封面
@receiver(pre_delete, sender=Cover)  # sender=你要删除或修改文件字段所在的类**
def cover_delete(instance, **kwargs):  # 函数名随意
    # print('进入文件删除方法，删的是', instance.url)  # 用于测试
    instance.url.delete(False)  # file是保存文件或图片的字段名**


# 标签表
class Tags(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=16, verbose_name='标签名字')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '文章标签'


# 回忆录
class History(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='事件名称')
    content = models.TextField(verbose_name='事件内容')
    create_date = models.DateField(verbose_name='创建时间', null=True)
    drawing = models.TextField(verbose_name='配图组，以;隔开', null=True, blank=True)

    class Meta:
        verbose_name_plural = '回忆录'


# 心情
class Moods(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='发布人', max_length=16)
    ip = models.GenericIPAddressField(verbose_name='ip地址', default='120.228.2.238')
    addr = models.TextField(verbose_name='用户地址信息', null=True)
    create_date = models.DateTimeField(verbose_name='发布时间', auto_now=True)
    content = models.TextField(verbose_name='心情内容')
    drawing = models.TextField(verbose_name='配图组，以;隔开', null=True, blank=True)
    comment_count = models.IntegerField(verbose_name='评论数', default=0)
    digg_count = models.IntegerField(verbose_name='点赞数', default=0)
    avatar = models.ForeignKey(
        to='Avatars',
        to_field='nid',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='心情的发布头像'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '心情'


# 心情评论
class MoodComment(models.Model):
    nid = models.AutoField(primary_key=True)
    avatar = models.ForeignKey(
        to='Avatars',
        to_field='nid',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='心情的发布头像'
    )
    name = models.CharField(verbose_name='评论人', max_length=16, null=True)
    content = models.TextField(verbose_name='评论内容')
    digg_count = models.IntegerField(verbose_name='点赞数', default=0)
    ip = models.GenericIPAddressField(verbose_name='ip地址', default='120.228.2.238')
    addr = models.TextField(verbose_name='用户地址信息', null=True)
    mood = models.ForeignKey(
        to='Moods',
        to_field='nid',
        on_delete=models.SET_NULL,
        verbose_name='评论的心情',
        null=True
    )
    create_date = models.DateTimeField(
        verbose_name='评论时间', auto_now=True
    )

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = '心情评论'


# 网站导航
class Navs(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='网站标题')
    abstract = models.CharField(max_length=128, verbose_name='网站简介', null=True)
    href = models.URLField(verbose_name='网站链接')
    icon_href = models.URLField(
        verbose_name='图标链接', help_text='在线链接', null=True, blank=True
    )
    create_date = models.DateTimeField(
        verbose_name='创建时间', auto_now=True
    )

    collects_count = models.IntegerField(verbose_name='文章收藏数', default=0)
    digg_count = models.IntegerField(verbose_name='点赞数', default=0)

    status_choice = (
        (0, '待审核'),
        (1, '已通过'),
        (2, '被驳回'),
    )
    status = models.IntegerField(verbose_name='导航状态', choices=status_choice, default=0)

    def color_state(self):
        if self.status == 0:
            assign_state_name = '待审核'
            color_code = '#ec921e'
        elif self.status == 1:
            color_code = 'green'
            assign_state_name = '已通过'
        else:
            color_code = 'red'
            assign_state_name = '被驳回'
        return format_html(
            '<span style="color:{};">{}</span>',
            color_code,
            assign_state_name,
        )

    color_state.short_description = '导航状态'

    tag = models.ManyToManyField(
        to='NavTags',
        verbose_name='网站标签',
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '网站导航'


# 网站标签
class NavTags(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=16)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '网站标签'


# 站点背景
class Menu(models.Model):
    nid = models.AutoField(primary_key=True)
    menu_title = models.CharField(verbose_name='菜单名称', max_length=16, null=True)
    menu_title_en = models.CharField(verbose_name='菜单英文名称', max_length=32, null=True)
    title = models.CharField(verbose_name='slogan', max_length=32, null=True)
    abstract = models.TextField(verbose_name='slogan介绍', help_text='多个之间按分号区分', null=True)
    abstract_time = models.IntegerField(verbose_name='slogan切换时间', help_text='单位秒，默认是8秒', default=8)
    rotation = models.BooleanField(verbose_name='是否轮播slogan介绍', default=True)
    menu_url = models.ManyToManyField(
        to='MenuImg',
        verbose_name='菜单图片',
        help_text='可以多选，多选就会轮播',
    )
    menu_rotation = models.BooleanField(verbose_name='是否轮播banner图', help_text='多选默认会轮播', default=False)
    menu_time = models.IntegerField(verbose_name='背景图切换时间', help_text='单位秒，默认是8秒', default=8)

    class Meta:
        verbose_name_plural = '站点背景'


# 站点背景
class MenuImg(models.Model):
    nid = models.AutoField(primary_key=True)
    url = models.FileField(verbose_name='图片地址', upload_to='site_bg/')
    dominant_hue = models.CharField(verbose_name='封面主色调', max_length=16, null=True, blank=True)
    is_dark = models.BooleanField(verbose_name='是否是深色系', null=True, blank=True)

    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name_plural = '站点背景图'


# 广告表
class Advert(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='产品名称', max_length=32, null=True)
    href = models.URLField(verbose_name='跳转链接')
    img = models.FileField(verbose_name='图片地址', null=True, blank=True, help_text='单图', upload_to='advert/')
    img_list = models.TextField(verbose_name='图片组', null=True, blank=True, help_text='上传图片请用线上地址，使用；隔开多张图片')
    is_show = models.BooleanField(verbose_name='是否展示', default=False)
    author = models.CharField(verbose_name='广告主', max_length=32, null=True, blank=True)
    abstract = models.CharField(verbose_name='产品简介', max_length=128, null=True, blank=True)

    class Meta:
        verbose_name_plural = '广告'


# 反馈信息
class Feedback(models.Model):
    nid = models.AutoField(primary_key=True)
    email = models.EmailField(verbose_name='邮箱')
    content = models.TextField(verbose_name='反馈信息')
    status = models.BooleanField(verbose_name='是否处理', default=False)
    processing_content = models.TextField(verbose_name='回复的内容', null=True, blank=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = '用户反馈'
