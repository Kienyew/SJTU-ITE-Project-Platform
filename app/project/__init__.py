'''
Logics and models for functioning of projects.
A project is a 工导项目 user submitted to our website,
as the initial objective of this website is to share projects.
'''

from flask import Blueprint

project_blueprint = Blueprint('project', __name__)

# activate the routing decorators
from . import views
