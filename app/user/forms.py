import re

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError
from werkzeug.security import check_password_hash

from .models import User

# Form validation and models

EMAIL_VALIDATORS = [DataRequired(), Email()]
PASSWORD_VALIDATORS = [DataRequired(), Length(8, 64)]
USERNAME_VALIDATORS = [DataRequired(), Length(
    4, 64), Regexp('^[a-zA-Z0-9_]+$', message='Username can contains only latin characters and digits')]


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=USERNAME_VALIDATORS)
    email = StringField('Email', validators=EMAIL_VALIDATORS)
    password = PasswordField('Password', validators=PASSWORD_VALIDATORS)
    password_confirm = PasswordField(
        'Confirm password', validators=PASSWORD_VALIDATORS + [EqualTo('password', "Password doesn't match!")])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already taken')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')


class LoginForm(FlaskForm):
    # Login Validation in security.py
    email_or_username = StringField('Email or username', validators=[DataRequired()])
    password = PasswordField('Password', validators=PASSWORD_VALIDATORS)
    submit = SubmitField('Log in')


class ForgetPassword(FlaskForm):
    email = StringField('Email address', validators=EMAIL_VALIDATORS)
    submit = SubmitField("Send reset request to my email")

    def validate_email(self, email):
        if not User.query.filter_by(email=email.data).first():
            raise ValidationError("Email does not exist")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=PASSWORD_VALIDATORS)
    confirm_password = PasswordField('Confirm Password', validators=PASSWORD_VALIDATORS + [EqualTo('password', "Password doesn't match!")])
    submit = SubmitField('Reset Password')


class UpdateAccount(FlaskForm):
    avatars = RadioField('Random avatar', choices=[], validate_choice=False)  # The choices are added dynamically
    new_username = StringField('Username', validators=[Length(0, 64)])
    old_password = PasswordField('Old Password', validators=PASSWORD_VALIDATORS)
    new_password = PasswordField('New Password', validators=[Length(0, 64)])
    new_password_confirm = PasswordField(
        'Confirm password', validators=[Length(0, 64), EqualTo('new_password', "New password doesn't match!")])
    submit = SubmitField('Update')

    def validate_username(self, field):
        # Keeps old username
        if len(field.data) == 0:
            return

        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken or too short')
        elif len(field.data) < 4:
            raise ValidationError('Username too short')
        elif len(field.data) > 63:
            raise ValidationError('Username too long')
        elif not re.match(r'^[a-zA-Z0-9_]+$', field.data):
            raise ValidationError('Username can contains only latin characters and digits')

    def validate_old_password(self, field):
        if not check_password_hash(current_user.password_hash, field.data):
            raise ValidationError('Wrong old Password')

    def validate_new_password(self, field):
        if field.data and len(field.data) < 8:
            raise ValidationError('Password too short')
