from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, Length


class PublishProjectForm(FlaskForm):
    team_name = StringField('Team name', validators=[DataRequired(), Length(1, 16)])
    team_description = StringField('Team description', validators=[DataRequired(), Length(1, 32)])
    teammates = StringField('Teammates', validators=[DataRequired(), Length(1, 16)])
    project_name = StringField('Project name', validators=[DataRequired(), Length(1, 16)])
    
    project_pic1 = FileField('', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])  # Must have at least one picture
    project_pic2 = FileField('', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    project_pic3 = FileField('', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    project_pic4 = FileField('', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    
    pic1_delete = StringField()  # Act as a boolean for delete picture
    pic2_delete = StringField()
    pic3_delete = StringField()
    pic4_delete = StringField()
    
    project_description = TextAreaField('Project description', validators=[DataRequired(), Length(1, 300)])
    submit = SubmitField('Publish')

