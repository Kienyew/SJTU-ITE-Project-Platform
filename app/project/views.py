from flask_login import login_required, current_user

from .. import db
from . import project_blueprint
from .models import Project


@project_blueprint.route('/like_project/<int:id>', methods=['POST'])
@login_required
def like_project(id: int):
    project = Project.query.get_or_404(id)
    current_user.liked_projects.append(project)
    db.session.add(current_user._get_current_object())
    db.session.commit()


@project_blueprint.route('/unlike_project/<int:id>', methods=['POST'])
@login_required
def like_project(id: int):
    project = Project.query.get_or_404(id)
    current_user.liked_projects.remove(project)
    db.session.add(current_user._get_current_object())
    db.session.commit()
