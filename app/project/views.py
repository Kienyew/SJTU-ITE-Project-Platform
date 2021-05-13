from flask_login import login_required, current_user

from .. import db
from . import project_blueprint
from .models import Project


@project_blueprint.route('/like_project/<int:id>', methods=['POST'])
@login_required
def like_project(id: int):
	"""
	Post to this route when a user like a project.
	If the user has already liked the project before, it does nothing.


	Parameters:
	id (int): Project id the user wanted to like
	"""
    project = Project.query.get_or_404(id)
    current_user.liked_projects.append(project)
    db.session.add(current_user._get_current_object())
    db.session.commit()


@project_blueprint.route('/unlike_project/<int:id>', methods=['POST'])
@login_required
def unlike_project(id: int):
	"""
	Post to this route when a user unlike a project.
	If the user have not liked the project before, it does nothing.


	Parameters:
	id (int): Project id the user wanted to unlike
	"""
    project = Project.query.get_or_404(id)
    current_user.liked_projects.remove(project)
    db.session.add(current_user._get_current_object())
    db.session.commit()
