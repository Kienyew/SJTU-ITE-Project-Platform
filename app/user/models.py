from typing import Optional

from flask_login import UserMixin

from .. import db
from .. import login_manager


# Required for many-to-many relationship of database.
# Contains data of like relationships between users and projects.
# Allowing two-way references. ie: Project.liked_users and User.liked_projects
like_registrations = db.Table('like_registrations',
                              db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                              db.Column('project_id', db.Integer, db.ForeignKey('projects.id'))
                              )


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    published_projects = db.relationship('Project', backref='publisher')
    liked_projects = db.relationship('Project', secondary=like_registrations,
                                     backref=db.backref('liked_users', lazy='dynamic'), lazy='dynamic')
    
    def __repr__(self):
        return f'User({self.id}, {self.username}, {self.email})'


@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    '''
    A required function for Flask-Login module
    '''
    return User.query.get(int(user_id))
