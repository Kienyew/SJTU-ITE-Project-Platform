from flask import render_template
from . import main_blueprint
# This is the main entry, contain webpage with general purpose


@main_blueprint.route('/')
@main_blueprint.route('/home')
def home():
    # Home page, main entry
    return render_template('home.html')

@main_blueprint.route('/discover')
def discover():
    # Place to display projects
    return render_template('discover.html')

def about():
    # TODO: About page
    pass

def contact():
    # TODO: Contact page
    pass
