# 第一个网站

## 简介

这是一个类似于知乎的问答网站, 用户可以发布问答和评论, 但前提是需要注册账户并且登录, 网站还支持搜素功能, 可以根据关键词搜索相应的问答

>框架: bootstrap(前端) + flask(后端)

### 前端

前端用到了[bootstrap](https://v4.bootcss.com/)框架, 采用jinja2的模板语法, 定义了一个父类模板, 子文件有首页, 登录页, 注册页, 发布问答页和问答详情页等

### 后端

后端用到了python的[flask](https://dormousehole.readthedocs.io/en/latest/)框架, 其中又用到了flask_sqlalchemy进行数据库存储, flask_mail发送邮件验证码.