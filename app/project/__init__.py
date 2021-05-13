from flask import Blueprint

project_blueprint = Blueprint('project', __name__, template_folder='templates')

# activate the routing decorators
from . import views
