from flask import render_template, url_for, redirect, flash
from flask_login import login_required, current_user

from .. import db
from .forms import PublishProjectForm
from . import project_blueprint
from .models import Project
from ..utils import image


@project_blueprint.route('/my_project', methods=['GET', 'POST'])
@login_required
def my_project():  # Submit new post or update existing post
    form = PublishProjectForm()
    
    if form.validate_on_submit():
        pic_names = image.save_images(form)
        # TODO: Implement delete picture from the server before updating + remove pic in frontend
        # TODO: Fix front end data in picture form
        # TODO: Currently new picture get overwritten over the old one, need to fix it
        post = Project(team_name=form.team_name.data,
                       team_description=form.team_description.data,
                       teammates=form.teammates.data,
                       project_name=form.project_name.data,
                       project_pic1=pic_names[0],
                       project_pic2=pic_names[1],
                       project_pic3=pic_names[2],
                       project_pic4=pic_names[3],
                       project_description=form.project_description.data,
                       publisher=current_user
                       )
        db.session.add(post)
        db.session.commit()
        
        flash('Upload success')
        return redirect(url_for('main.discover'))
    
    try:  # If exist previous data
        project = current_user.published_projects[0]
        print(project)
        form.team_name.data = project.team_name
        form.team_description.data = project.team_description
        form.teammates.data = project.teammates
        form.project_name.data = project.project_name
        form.project_description.data = project.project_description
        
        # Pass as a dict because I can't make it work with changing label T_T
        pic_data = {
            "project_pic1": project.project_pic1,
            "project_pic2": project.project_pic2,
            "project_pic3": project.project_pic3,
            "project_pic4": project.project_pic4
        }
        print(project.project_pic1 + '\n' +  # Debug
              project.project_pic2 + '\n' +
              project.project_pic3 + '\n' +
              project.project_pic4)
    except:
        pic_data = {
            "project_pic1": None,
            "project_pic2": None,
            "project_pic3": None,
            "project_pic4": None
        }
    return render_template('submit project.html', form=form, pic_data=pic_data)


@project_blueprint.route('/post/<int:id>', methods=['GET'])
def post(id: int):
    project = Project.query.filter_by(id=id).first_or_404()
    print(project.project_pic1)  # DEBUG
    print(project.project_pic2)
    print(project.project_pic3)
    print(project.project_pic4)
    return render_template('single project.html', project=project)


@project_blueprint.route('/toggle_like/', defaults={'id': -1})
@project_blueprint.route('/toggle_like/<int:id>')
@login_required
def toggle_like(id: int):
    """
	Post to this route when a user like/unlike a project.
	If the user has already liked the project before, it will unlike the project.

	Parameters:
	id (int): Project id the user wanted to like
	
	Returns:
	json response
    """
    if id == -1:
        return 'forbidden access', 403
    print(f"THERE's request for toggling like for project:{id} from {current_user}")
    project = Project.query.get_or_404(id)
    if project in current_user.liked_projects:
        current_user.liked_projects.remove(project)
    else:
        current_user.liked_projects.append(project)
    
    db.session.add(current_user._get_current_object())
    db.session.commit()
    return 'success', 200
