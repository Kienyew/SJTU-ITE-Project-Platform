from flask import Blueprint

errors_blueprint = Blueprint('errors', __name__, template_folder='templates')

# activate the routing decorators
from . import views
