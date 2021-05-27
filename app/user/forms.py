from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError
from werkzeug.security import check_password_hash

import re
from .models import User

# Form validation and models

EMAIL_VALIDATORS = [DataRequired(message='邮箱未填'), Email(message='邮箱填写错误')]
PASSWORD_VALIDATORS = [DataRequired(message='密码未填'), Length(8, 64, message='密码长度太长或太短')]
USERNAME_VALIDATORS = [DataRequired(message='用户名未填'), Length(4, 64), Regexp('^[a-zA-Z0-9_]+$', message='用户名只能包含拉丁文和数字')]


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=USERNAME_VALIDATORS)
    email = StringField('Email', validators=EMAIL_VALIDATORS)
    password = PasswordField('Password', validators=PASSWORD_VALIDATORS)
    password_confirm = PasswordField('Confirm password', validators=PASSWORD_VALIDATORS + [EqualTo('password', message="两个密码不匹配")])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经被注册')


class LoginForm(FlaskForm):
    # Login Validation in security.py
    email_or_username = StringField('Email or username', validators=[DataRequired(message='用户名或邮箱不能为空')])
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
    confirm_password = PasswordField('Confirm Password', validators=PASSWORD_VALIDATORS + [EqualTo('password', "密码不匹配")])
    submit = SubmitField('Reset Password')


class UpdateAccount(FlaskForm):
    avatars = RadioField('Random avatar', choices=[], validate_choice=False)  # The choices are added dynamically
    new_username = StringField('Username', validators=[Length(0, 64)])
    old_password = PasswordField('Old Password', validators=PASSWORD_VALIDATORS)
    new_password = PasswordField('New Password', validators=[Length(0, 64)])
    new_password_confirm = PasswordField(
        'Confirm password', validators=[Length(0, 64), EqualTo('new_password', "两个密码不匹配")])
    submit = SubmitField('Update')

    def validate_username(self, field):
        # Keeps old username
        if len(field.data) == 0:
            return

        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被注册')
        elif len(field.data) < 4:
            raise ValidationError('用户名过短')
        elif len(field.data) > 63:
            raise ValidationError('用户名过长')
        elif not re.match(r'^[a-zA-Z0-9_]+$', field.data):
            raise ValidationError('用户名只能包含拉丁文和数字')

    def validate_old_password(self, field):
        if not check_password_hash(current_user.password_hash, field.data):
            raise ValidationError('旧密码不正确')

    def validate_new_password(self, field):
        if field.data and len(field.data) < 8:
            raise ValidationError('密码过短')
