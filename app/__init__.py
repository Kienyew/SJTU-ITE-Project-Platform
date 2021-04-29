from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from config import Config


db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'user.login'


def create_app(config: Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    from .main import main_blueprint
    from .user import user_blueprint
    from .project import project_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(project_blueprint, url_prefix='/project')

    return app
