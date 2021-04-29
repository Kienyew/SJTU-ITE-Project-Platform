from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ProjectPublishForm(FlaskForm):
    name = StringField('Project name', validators=[
                       DataRequired(), Length(1, 128)])
    short_description = StringField(
        'Short description', validators=[Length(0, 256)])

    submit = SubmitField('Publish')
