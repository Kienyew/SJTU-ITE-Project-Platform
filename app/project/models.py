from datetime import datetime
from .. import db



class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    short_description = db.Column(db.Text)
    publish_time = db.Column(db.DateTime, index=True, nullable=False, default=datetime.utcnow)
    publisher_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'Project({self.id}, {self.name})'

    def get_liked_count(self) -> int:
        return self.liked_users.count()
