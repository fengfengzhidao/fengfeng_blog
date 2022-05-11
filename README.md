# FengfengBlog

🌍
 [简体中文](README.md)

基于`python3.6.8`和`Django3.2.10`的博客。   

![image](https://img.shields.io/badge/blog-5.0.1-yellow.svg)
[![image](https://img.shields.io/badge/fengfengblog-枫枫知道-orange.svg)](http://www.fengfengzhidao.com/)
![image](https://img.shields.io/badge/license-Mysql5.7.26-blue.svg)

## 主要功能：
- 文章，页面，分类目录，标签的添加，删除，编辑等。文章及页面支持`Markdown`，支持代码高亮。
- 支持文章全文搜索。
- 主题切换功能，手机端适配。
- 完整的评论功能，包括发表回复评论，支持`Markdown`。
- 侧边栏功能，最新文章，最多阅读等。
- 支持Oauth登陆，现已有QQ登录，gitee登录。
- 集成了简单的图床功能。
- 网站异常邮件提醒，若有未捕捉到的异常会自动发送提醒邮件。


## 安装

1. git 拉取代码
2. 安装所需的第三方模块
    ```bash
    pip install -r requirements.txt
    ```

## 运行

 修改`v4_blog/setting.py` 修改数据库配置，如下所示：

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
QINIU_ACCESS_KEY = '你的AK'
QINIU_SECRET_KEY = '你的SK'
```

- 第三方登录
```python
# QQ登录
QQ_KEY = 'QQ登录的key'

# gitee登录
GITEE_ID = 'Gitee登录的ID'
GITEE_SECRET = 'Gitee登录的SECRET'
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

### 开始运行：
执行： `python manage.py runserver`


浏览器打开: http://127.0.0.1:8000/  就可以看到效果了。  

### 默认管理员

```python
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



## 问题相关

有任何问题欢迎提Issue,或者添加我的联系方式 2974771769（qq）.我会尽快解答.推荐提交Issue方式.  

公测阶段遇到的任何项目相关的问题，都可以反馈于我。

## 捐赠
如果您觉得本项目对您有所帮助，欢迎您请我喝杯咖啡，您的支持是我最大的动力，您可以扫描下方二维码为我付款，谢谢。

### 支付宝：
<div>    
<img src="./doc/play/zhifubao_pay.jpg" width="150" height="150" />
</div>  

### 微信：
<div>    
<img src="./doc/play/weixin_pay.jpg" width="150" height="150" />
</div>

---

感谢jetbrains
<div>    
<a href="https://www.jetbrains.com/?from=DjangoBlog"><img src="https://resource.lylinux.net/image/2020/07/01/logo.png" width="150" height="150"></a>
</div>

## 更新历史

### 2022年5月11日
1. 项目配置优化
2. 网站关于优化
3. 取消中间件中encoding的代码
4. editormd的标题bug修复
5. 文章悬浮目录首次加载异常bug修复

### 2022年3月12日
1. 完成项目录制工作
2. 源码上传（未开源）

