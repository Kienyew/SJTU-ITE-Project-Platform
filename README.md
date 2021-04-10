# upgraded-happiness
名字乱取的。

网页项目的后端，小组内共享代码用。（虽然是公开的，反正也没其他人会来看吧大概）

# 规划
项目主要在 `app/` 文件夹内：
```
app
├── __init__.py
├── root
│   ├── __init__.py
│   └── views.py
├── templates
│   ├── base.html
│   ├── index.html
│   └── user
│       ├── login.html
│       └── register.html
└── user
    ├── forms.py
    ├── __init__.py
    ├── models.py
    ├── security.py
    └── views.py
```
`templates/` 里是 html 文件。

除去 `templates/`，其余的文件夹为各个功能模块，如 `user/` 负责用户的注册、登入、登出等等。

`views.py` 文件负责所属模块下的 routing，指示有人进入该模块负责的网址时该怎么做。

`models.py` 是 SQLAlchemy 用来对应数据库里的数据的各个 class。

`forms.py` 指定用户提交给服务器的数据，如注册时需要提交的 email, username, password 等。

