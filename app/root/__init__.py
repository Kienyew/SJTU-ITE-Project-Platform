from flask import Blueprint

root_blueprint = Blueprint('root', __name__)

# activate the routing decorators
from . import views
