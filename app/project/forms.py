from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TextField, FileField, TextAreaField
from wtforms.validators import DataRequired, Length


class PublishProjectForm(FlaskForm):
    team_name = StringField('Team name', validators=[DataRequired(), Length(1, 16)])
    team_description = StringField('Team description', validators=[DataRequired(), Length(1, 32)])
    teammates = StringField('Teammates', validators=[DataRequired(), Length(1, 16)])
    project_name = StringField('Project name', validators=[DataRequired(), Length(1, 16)])
    
    project_pic1 = FileField('', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png'])])
    project_pic2 = FileField('', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    project_pic3 = FileField('', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    project_pic4 = FileField('', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    
    project_description = TextAreaField('Project description', validators=[DataRequired(), Length(1, 120)])

    submit = SubmitField('Publish')
