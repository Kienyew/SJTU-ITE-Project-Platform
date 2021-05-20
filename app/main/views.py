from flask import render_template, request
from . import main_blueprint
from ..project.models import Project
# This is the main entry, contain webpage with general purpose


@main_blueprint.route('/')
@main_blueprint.route('/home')
def home():
    # Home page, main entry
    return render_template('home.html')

@main_blueprint.route('/discover')
def discover():
    # Place to display projects
    page = request.args.get('page', 1, type=int)
    projects = Project.query.order_by(Project.publish_time.desc()).paginate(page=page, per_page=7)  # projects / page
    return render_template('discover.html', projects=projects)

@main_blueprint.route('/about')
def about():
    return render_template('about.html')

@main_blueprint.route('/error')
def error():
    # TODO: error page
    return render_template('discover.html')
