from werkzeug.security import generate_password_hash
from flask import render_template, url_for, redirect, flash, current_app, abort
from flask_login import login_required, current_user

from .. import db
from .forms import PublishProjectForm
from . import project_blueprint
from .models import Project
from ..user.models import User
from ..utils import image
import pandas as pd
from ast import literal_eval
from datetime import datetime
import os


@project_blueprint.route('/my_project', methods=['GET', 'POST'])
@login_required
def my_project():
    """The main gateway for user to submit and update their post
    update if exist or create a new one if not
    
    :return: redirect to main.discover if success otherwise return this page with an error message
    """
    
    # TODO: Fix paragraph tag wrapping issue + Better solution + delete pictures + file upload pre-populate solution
    
    form = PublishProjectForm()
    
    if form.validate_on_submit():
        try:  # If exist previous data
            project = current_user.published_projects[0]
            image.delete_unused_image(form, [project.project_pic1, project.project_pic2, project.project_pic3,
                                             project.project_pic4])
            has_previous = True
        except:  # Create new if old one doesn't exist
            project = Project()
            has_previous = False
        pic_names = image.save_images(form)  # Compress and save
        
        project.team_name = form.team_name.data
        project.team_description = form.team_description.data
        project.teammates = form.teammates.data
        project.project_name = form.project_name.data
        project.project_pic1 = pic_names[0]
        project.project_pic2 = pic_names[1]
        project.project_pic3 = pic_names[2]
        project.project_pic4 = pic_names[3]
        project.project_description = form.project_description.data
        project.publisher = current_user
        
        if not has_previous:
            db.session.add(project)
        db.session.commit()
        
        flash('成功上传', 'success')
        return redirect(url_for('main.discover'))
    
    try:  # If exist previous data
        project = current_user.published_projects[0]
        print(project)
        form.team_name.data = project.team_name
        form.team_description.data = project.team_description
        form.teammates.data = project.teammates
        form.project_name.data = project.project_name
        print(type(form.project_pic1), type(project.project_pic1))
        form.project_pic1.data = project.project_pic1
        form.project_pic2.data = project.project_pic2
        form.project_pic3.data = project.project_pic3
        form.project_pic4.data = project.project_pic4
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
    """Visitor can click on individual post in discovery webpage and redirect to here (single project view)
    
    :param id: primary id in the project field
    :return: a single project webpage view
    """
    
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
    """Post to this route when a user like/unlike a project.
    If the user has already liked the project before, it will unlike the project.
    
    :param id: The primary key in Project model
    :return: json response with http status
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


@project_blueprint.route('/generate_dummies')
def generate_dummies():
    """A route created only for testing purpose, should NEVER be used in real production environment
    
    :return: redirect to main.discover after generating dummies data
    """
    
    if not current_app.config['USER_DEBUG_MODE']:  # Prevent unauthorised access
        abort(403)
    
    users = []
    projects = []
    
    fake_data = pd.read_csv(os.path.join(current_app.root_path, 'testing', 'fake_data.csv'))
    for row in fake_data.itertuples():
        user = User(email=row.email, user_avatar=row.user_avatar, username=row.username,
                    password_hash=generate_password_hash(row.password))
        print(f'Generating user: \n  Email:{row.email}\n  Name:{row.username}\n  Password:{row.password}')
        project_pictures = literal_eval(row.project_pictures)
        project_pictures = project_pictures + ['' for _ in range(len(project_pictures), 4)]
        print(f'  Pictures: {project_pictures}')
        project = Project(
            team_name=row.team_name,
            team_description=row.team_description,
            teammates=",".join(literal_eval(row.teammates)),
            project_name=row.project_name,
            project_pic1=project_pictures[0],
            project_pic2=project_pictures[1],
            project_pic3=project_pictures[2],
            project_pic4=project_pictures[3],
            project_description="\n".join(literal_eval(row.project_description)),
            publisher=user,
            publish_time=datetime.strptime(row.project_date, '%Y-%m-%d')
        )
        
        users.append(user)
        projects.append(project)
    
    db.session.add_all(users + projects)
    db.session.commit()
    # TODO: Randomize like + record existing dummy account
    print("WARNING!!! Only use this for testing purpose")
    
    flash('测试用户及作品已生成', 'success')
    return redirect(url_for('main.discover'))
