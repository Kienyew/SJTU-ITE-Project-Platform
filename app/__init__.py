from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_msearch import Search
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from config import Config


db = SQLAlchemy()
search = Search()
admin = Admin()
login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.login_message = '该操作需要登入权限'
login_manager.login_message_category = 'info'


def create_app(config: Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    login_manager.init_app(app)
    search.init_app(app)
    admin.init_app(app)
    
    from .main import main_blueprint
    from .user import user_blueprint
    from .project import project_blueprint
    from .errors import errors_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(project_blueprint, url_prefix='/project')
    app.register_blueprint(errors_blueprint, url_prefix='/errors')

    from .user.models import User
    from .project.models import Project
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Project, db.session))

    return app
