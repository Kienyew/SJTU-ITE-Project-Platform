from flask import render_template, request, current_app
from . import main_blueprint
from ..project.models import Project
# This is the main entry, contain webpage with general purpose


@main_blueprint.route('/')
@main_blueprint.route('/home')
def home():
    """main entry
    
    :return: a simple animated homepage
    """
    
    return render_template('home.html')

@main_blueprint.route('/discover')
def discover():
    """Display projects in grid view, sorting results from the newest to the oldest
    
    :return: discover webpage
    """
    
    page = request.args.get('page', 1, type=int)
    projects = Project.query.order_by(Project.publish_time.desc()).paginate(page=page, per_page=current_app.config['POSTS_PER_PAGE'])  # projects / page
    
    return render_template('discover.html', projects=projects)

@main_blueprint.route('/search/', defaults={'query': ''}, methods=['POST', 'GET'])
@main_blueprint.route('/search/<string:query>', methods=['POST', 'GET'])
def search(query: str):
    """Simple search engine that search in Project ['team_name', 'project_description', 'project_name'] fields
    
    :param query: the keyword for search engine to perform search
    :return: search result display in discover webpage layout
    """
    
    print(f"Searching for: {query}")  # Debug
    page = request.args.get('page', 1, type=int)
    projects = Project.query.msearch(query).order_by(Project.publish_time.desc()).paginate(page=page, per_page=current_app.config['POSTS_PER_PAGE'])
    
    return render_template('discover.html', projects=projects, query=query)
    

@main_blueprint.route('/about')
def about():
    """A page for us to write about our motive, plans and credits
    
    :return: about.html
    """
    
    return render_template('about.html')


