from flask import Blueprint

project_blueprint = Blueprint('project', __name__)

# activate the routing decorators
from . import views
