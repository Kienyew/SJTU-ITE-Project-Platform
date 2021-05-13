"""
Logics and model for users of our websites.
We allow users to register on our website, as in many social networks.
"""

from flask import Blueprint

user_blueprint = Blueprint('user', __name__, template_folder='templates')

# activate the routing decorators
from . import views
