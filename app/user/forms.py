from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from .models import User

EMAIL_VALIDATORS = [DataRequired(), Email()]
PASSWORD_VALIDATORS = [DataRequired()]
USERNAME_VALIDATORS = [DataRequired(), Length(
    4, 64), Regexp('^[a-zA-Z_][a-zA-Z0-9_]+$')]


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=EMAIL_VALIDATORS)
    username = StringField('Username', validators=USERNAME_VALIDATORS)
    password = PasswordField('Password', validators=PASSWORD_VALIDATORS)
    password_confirm = PasswordField(
        'Confirm password', validators=PASSWORD_VALIDATORS + [EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email exists')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username exists')
