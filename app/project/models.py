from datetime import datetime
from .. import db


class Project(db.Model):
    __tablename__ = 'projects'
    __searchable__ = ['team_name', 'project_description', 'project_name']
    id = db.Column(db.Integer, primary_key=True)
    
    # From form ------------------------------------------------
    team_name = db.Column(db.String(16), index=True, nullable=False)
    team_description = db.Column(db.String(32), nullable=False)
    teammates = db.Column(db.String(16), nullable=False)
    project_name = db.Column(db.String(16), nullable=False)

    project_pic1 = db.Column(db.String(70), nullable=False)  # 64 hex encoded project name
    project_pic2 = db.Column(db.String(70))
    project_pic3 = db.Column(db.String(70))
    project_pic4 = db.Column(db.String(70))

    project_description = db.Column(db.Text(310), nullable=False)
    
    # Other important attribute ---------------------------------------------
    publish_time = db.Column(db.DateTime, index=True, nullable=False, default=datetime.utcnow)
    publisher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'Project({self.id}, {self.project_name}, {self.team_name}, {self.publish_time})'

    def get_liked_count(self) -> int:
        return self.liked_users.count()
