from flask_migrate import Migrate

from config import Config
from app.user.models import User
from app.project.models import Project
from app import db, create_app
import os

app = create_app(Config)
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Project': Project,
    }


if __name__ == '__main__':
    # For debugging purpose, create database if not exist in current directory
    if not os.path.exists(Config.SQLALCHEMY_DATABASE_URI[10:]):
        print("creating database", Config.SQLALCHEMY_DATABASE_URI[10:])  # DEBUG
        with app.app_context():
            db.create_all()
    
    app.run(debug=Config.USER_DEBUG_MODE)


