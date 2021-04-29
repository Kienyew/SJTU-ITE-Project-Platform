from datetime import datetime

from flask import url_for, redirect, render_template, flash
from flask_login import current_user, login_required

from .. import db
from . import project_blueprint
from .models import Project
from .forms import ProjectPublishForm


@project_blueprint.route('/publish', methods=['GET', 'POST'])
@login_required
def publish():
    form = ProjectPublishForm()
    if not form.validate_on_submit():
        return render_template('project/publish.html', form=form)

    project = Project(name=form.name.data,
                      short_description=form.short_description.data,
                      publisher_id=current_user.id)

    db.session.add(project)
    db.session.commit()

    flash('Project published successfully')
    return redirect(url_for('root.index'))
