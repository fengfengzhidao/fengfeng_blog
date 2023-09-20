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


## gin-vue-blog

基于go+vue3的前后端分离博客

[gin-vue-blog后端教程部分](https://www.bilibili.com/video/BV1f24y1G72C)  
[gin-vue-blog前端教程部分](https://www.bilibili.com/video/BV1Fj411u7yk)  

完整教程请联系我

官方指定QQ：2974771769（枫枫知道）

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

### 系统默认管理员

```text
user: admin
password: root
```


## 技术支持

本项目源码开源

如果需要在此项目上进行二开，遇到问题可以联系我，我可以提供技术支持（付费）

如果本项目对您有所帮助，欢迎您请我喝杯咖啡，您的支持是我最大的动力。

### 支付宝：

<div>    
<img src="./doc/img.png" width="150" height="150" />
</div>  

### 微信：

<div>    
<img src="./doc/img_1.png" width="150" height="150" />
</div>



## 项目截图

### 首页
![](./doc/1.png)

![](./doc/2.png)

### 新闻
![](./doc/3.png)

### 心情
![](./doc/20221120135040.png)

### 文章搜索
![](./doc/20220902081114.png)

![](./doc/20221120135237.png)

### 网站导航
![](./doc/20220902081050.png)

### 登录注册
![](./doc/20220902100521.png)

### 个人中心
![](./doc/20220902100616.png)

### 后台系统
![](./doc/img_2.png)