# SJTU Introduction-To-Engineering Project: Platform
上海交通大学工程学导论项目共享平台。

# 规划
项目主要在 `app/` 文件夹内，这是一个树状图，你可以大概知道每一个部分是在干嘛：
```
app
├── README.md
├── _static webpage（静态页面）
├── app（主要逻辑）
│   ├── __init__.py
│   ├── errors（报错逻辑）
│   ├── main（主要界面）
│   │   ├── __init__.py
│   │   ├── templates
│   │   │   ├── discover.html
│   │   │   └── home.html
│   │   └── views.py
│   ├── project
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── models.py
│   ├── static （CSS，JS和其他的静态资源都在这里）
│   │   ├── css
│   │   ├── resources
│   │   ├── scripts
│   │   └── user\ resources
│   ├── templates （通用模版）
│   ├── testing （DEBUG生成和调试）
│   ├── user （用户逻辑）
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── security.py
│   │   ├── templates
│   │   │   ├── forgot password.html
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── views.py
│   └── utils （通用的工具）
│       └── image.py
├── config.py（主要的设置）
├── data.sqlite（跑过一遍后就会出现的数据库）
├── migrations（Alembic自动生成）
├── requirements.txt
└── run.py（入口程序）
```
这是一个典型的Flask蓝图处理结构

`templates/` 里是 html 文件。

除去 `templates/`，其余的文件夹为各个功能模块，如 `user/` 负责用户的注册、登入、登出等等。

`views.py` 文件负责所属模块下的 routing，指示有人进入该模块负责的网址时该怎么做。

`models.py` 是 SQLAlchemy 用来对应数据库里的数据的各个 class。

`forms.py` 指定用户提交给服务器的数据，如注册时需要提交的 email, username, password 等。

