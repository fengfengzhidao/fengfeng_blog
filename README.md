# FengfengBlog

🌍
[简体中文](README.md)

基于`python3.6.8`和`Django3.2.10`的博客。

[![image](https://img.shields.io/badge/fengfengblog-枫枫知道-orange.svg)](http://www.fengfengzhidao.com/) ![image](https://img.shields.io/badge/blog-5.0.1-yellow.svg)  ![image](https://img.shields.io/badge/license-Mysql5.7.26-blue.svg)

## 主要功能：

- 文章，页面，分类目录，标签的添加，删除，编辑等。文章及页面支持`Markdown`，支持代码高亮。
- 支持文章条件搜索。
- 主题切换功能，手机端适配。
- 完整的评论功能，包括发表回复评论，支持`Markdown`。
- 侧边栏功能，最新文章，最多阅读等。
- 支持Oauth登陆，现已有QQ登录，gitee登录。
- 集成了七牛云的图床功能。

## 线上版本新功能

- 网站异常告警，出现无法处理的异常将会自动发送提醒邮件或短信。
- 文章日历功能
- 网站更新历史
- 接入企业微信API，实时掌握用户动态
- es全文搜索，文章搜索功能更加强大
- 首页全文搜索，主打文章内容搜索，点击可直接跳转至对应位置
- 标签跳转功能，用户点击右侧标签即可显示对应标签下的文章列表
- 需要输入密码才能访问的文章，可自定义预览文章的内容

## 适用人群
1. 没有python-web开发经验的大学生
2. 想要拥有一款个人博客的人群


### 课程链接

[第一部分 1-200](https://www.bilibili.com/video/BV1yu411276D)

[第二部分 201-324](https://www.bilibili.com/video/BV1sL411T735)

### 项目不足之处

1. 没有更易于扩展的三方登录，内置的qq和 gitee 可以满足大部分需求（悄悄的告诉你，微信登录是要钱的）
2. 状态码返回很凌乱，打算在后期的过程中优化掉
3. css代码大段重复，没有发挥出scss它应有的作用，后期再开个分支处理一下
4. 不能支持用户发布文章，如果支持的话，审核这些就很麻烦了
5. 主题功能并不完善，后续打算在个人中心处做一个类似主题商店的东西（先画个饼）
6. 没有插件系统，后期做不了生态
7. 前后端不分离的项目，适合个人产品，开发虽然快，但非原作者对后期维护相对麻烦
## 捐赠

如果您觉得本项目对您有所帮助，欢迎您请我喝杯咖啡，您的支持是我最大的动力，您可以扫描下方二维码为我付款，谢谢。

### 支付宝：

<div>    
<img src="https://python.fengfengzhidao.com/pic/zhifubao_pay.jpg" width="150" height="150" />
</div>  

### 微信：

<div>    
<img src="http://python.fengfengzhidao.com/pic/weixin_pay.jpg" width="150" height="150" />
</div>

## 项目目录

```text
+---Fengfengblog  项目同名目录
|      +---__init__.py
|      +---asgi.py  asgi部署使用
|      +---wsgi.py  wsgi部署使用
|      +---settings.py  配置文件，重要
|      +---local_settings.py 本地运行时的配置
|      +---urls.py  项目路由，重要
|
+---lib  一些工具模块都在这里
|
+---api  api相关的app
|      +---migrations  数据库迁移文件
|      +---views  视图目录
|      |     +---admin_data.py  后台的一些数据接口  
|      |     +---api_email.py  邮件发送接口
|      |     +---article.py  文章接口
|      |     +---comment.py  评论接口
|      |     +---file.py  文件上传接口
|      |     +---history.py  回忆录接口
|      |     +---login.py  登录注册接口
|      |     +---mood.py  心情接口
|      |     +---sites.py  网站导航接口
|      |     +---user.py  修改密码接口
|      |
|      +---__init__.py
|      +---admin.py
|      +---models.py  表结构
|      +---tests.py
|      +---urls.py  api分发的路由
+---app01 与页面相关的app
|      +---migrations
|      +---templatetags  自定义标签和过滤器
|      |      +---my_filter.py  自定义过滤器
|      |      +---my_tag.py  自定义标签
|      |     
|      +---valid  验证相关
|      |      +---auth  重写django的authenticate方法
|      |
|      +---views  视图目录
|      +---__init__.py  app01的初始化文件
|      +---admin.py  admin结构
|      +---middleware_decode.py  用于转换axios数据的中间件
|      +---models.py  表结构
|      +---tests.py
|      
+---media  用户上传文件的目录
+---static  静态文件
+---templates  模板文件
|      +---backend  后台相关的模板
|      |      +---add_article.html  添加文章
|      |      +---avatar_list.html  头像列表
|      |      +---backend.html  个人中心
|      |      +---cover_list.html  文章封面列表
|      |      +---edit_article.html  编辑文章
|      |      +---edit_avatar.html  修改头像
|      |      
|      +---my_tag   自定义
|      |      +---headers.html  banner轮播图
|      |
|      +---simple_admin
|      |      +---add_form.html  后台选择封面的模板修改
|      |
|      +---about.html  网站关于
|      +---admin_home.html  后台的首页
|      +---article.html  文章详情页
|      +---article_lock.html  加锁的文章详情页
|      +---blog.html  博客项目
|      +---history.html  建站回忆录
|      +---index.html  首页
|      +---login.html  登录
|      +---moods.html  心情页面
|      +---news.html  新闻
|      +---search.html  搜索
|      +---sign.html  注册
|      +---sites.html  网址导航
|
+---.gitignore  git忽略文件
+---README.md  说明文档
+---blog.sql  项目的数据库文件
+---manage.py  启动文件
+---requirements.txt  第三方模块
```

## 安装

1. git 拉取代码
2. 安装所需的第三方模块
    ```bash
    pip install -r requirements.txt
    ```

## 运行

修改`Fengfengblog/setting.py` 修改数据库配置，如下所示：

- 数据库修改

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'host',
        'PORT': 3306,
    }
}
```

- 邮箱密码修改

```python

# 发送邮箱配置
EMAIL_HOST = 'smtp.qq.com'  # 对应邮箱的邮件服务器
EMAIL_PORT = 465  # 对应邮件服务器的端口
EMAIL_HOST_USER = '你的邮箱'
EMAIL_HOST_PASSWORD = '你的登录凭证'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_USE_SSL = True
EMAIL_USER_TLS = False

```

- 七牛云配置

```python
# 七牛云配置
QINIU_ACCESS_KEY = '七牛云AK'
QINIU_SECRET_KEY = '七牛云SK'
QINIU_BUCKET_NAME = '七牛云存储空间'
QINIU_DOMAIN = 'xxx.xxx.xxx'  # 访问的域名，按照这样的格式
```

- 第三方登录

```python
# QQ登录
QQ_APPID = '你的QQ appid'
QQ_KEY = '你的QQ_KEY'
QQ_REDIRECT = 'QQ登录之后的回调地址'

# gitee登录
GITEE_ID = 'GiteeID'
GITEE_SECRET = 'GiteeSECRET'
GITEE_REDIRECT = 'gitee登录之后的回调地址'
```

### 创建数据库

导入数据:

```bash
create database blog;
# 进入创建的库
use blog;
# 导入数据
source  blog.sql
```

导入数据库之后不需要进行数据库迁移

### 开始运行：

执行： `python manage.py runserver`

浏览器打开: http://127.0.0.1:8000/  就可以看到效果了。
   
### 默认管理员

```text
user: admin
password: root
```

## 服务器部署

- 导出第三方库

```bash
pip freeze > requirements.txt
```

- 导出mysql数据

```bash
mysqldump -u root -p blog > blog.sql
```

## 项目截图

### 首页
![](http://python.fengfengzhidao.com/pic/20220902080859.png)

![](http://python.fengfengzhidao.com/pic/20221120134737.png)

### 新闻
![](http://python.fengfengzhidao.com/pic/20220902080954.png)

### 心情
![](http://python.fengfengzhidao.com/pic/20221120135040.png)

### 文章搜索
![](http://python.fengfengzhidao.com/pic/20220902081114.png)
![](http://python.fengfengzhidao.com/pic/20221120135237.png)

### 网站导航
![](http://python.fengfengzhidao.com/pic/20220902081050.png)

### 登录注册
![](http://python.fengfengzhidao.com/pic/20220902100521.png)

### 个人中心
![](http://python.fengfengzhidao.com/pic/20220902100616.png)

### 后台系统
![](http://python.fengfengzhidao.com/pic/20221120135342.png)

## 问题相关

有任何问题欢迎提Issue,或者添加我的联系方式 2974771769（qq）.我会尽快解答.推荐提交Issue方式.

公测阶段遇到的任何项目相关的问题，都可以反馈于我。


---

## TODO
1. 全文搜索功能
2. golang专区
3. TODO专区
4. 插件功能

## 更新历史

### 2022 年 09 月 02 日

1. 筹备开源工作
2. 优化代码中的不合理地方
3. FengUI的开发，抽离公共css样式
4. 新增项目配置，用户可以使用配置控制页面组件的展示

### 2022 年 07 月 02 日

1. 优化目录结构

### 2022 年 05 月 13 日

1. 修改版本配置
2. 修改视图函数的文档注释

### 2022 年 05 月 11 日

1. 项目配置优化
2. 网站关于优化
3. 取消中间件中encoding的代码
4. editormd的标题bug修复
5. 文章悬浮目录首次加载异常bug修复
6. giteeREADME图片加载失败问题

### 2022 年 03 月 12 日

1. 完成项目录制工作
2. 源码上传（未开源）

