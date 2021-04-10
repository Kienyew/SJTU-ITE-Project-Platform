from flask import Blueprint

user_blueprint = Blueprint('user', __name__)

# activate the routing decorators
from . import views
