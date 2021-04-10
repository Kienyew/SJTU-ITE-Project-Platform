from flask_migrate import Migrate

from config import Config
from app.user.models import User
from app import db, create_app


app = create_app(Config)
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User
    }
