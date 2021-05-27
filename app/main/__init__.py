from flask import Blueprint

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates')

# activate the routing decorators
from . import views
