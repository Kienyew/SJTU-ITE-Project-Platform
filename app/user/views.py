import os
import random
import smtplib
from email_validator import validate_email, EmailNotValidError
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from email.mime.text import MIMEText
from email.utils import formataddr
from random import randint

from . import user_blueprint
from .forms import RegistrationForm, LoginForm, ForgetPassword, UpdateAccount
from .models import User
from .. import db

# Account and verification of email sender
mailsender = 'sjtu-ite-platform@qq.com'
mailsendpass = 'xqjdixlzltvmdhif'

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """A route for new user to register a new account
    
    :return: redirect to login page if successfully registered otherwise register page
    """
    
    # TODO: require email verification
    if current_user.is_authenticated:
        flash('你已登陆', 'info')
        return redirect(url_for('main.discover'))

    form = RegistrationForm()
    if not form.validate_on_submit():
        return render_template('register.html', form=form)

    user = User(email=form.email.data, username=form.username.data, password_hash=generate_password_hash(form.password.data))
    ret = {'flag': True, 'captcha': randint(100000, 999999)}
    try:
        msg = MIMEText(f"您正在注册上海交通大学学生实践项目展示网，验证码：{ret['captcha']}。如果您未注册，请忽略本邮件。", 'plain', 'utf-8')
        msg['From'] = formataddr(["SJTU-ITE-Project-Platform", mailsender])
        msg['To'] = formataddr([user.username, user.email])
        msg['Subject'] = "Captcha of SJTU-ITE-Project-Platform"
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(mailsender, mailsendpass)
        server.sendmail(mailsender, user.email, msg.as_string())
        server.quit()
    except Exception as e:  #if failed to send captcha
        ret = False
    if ret['flag']:
        flash('激活码已发至邮箱', 'info')
    else:
        flash('邮件发送失败，请检查邮箱地址', 'danger')

    db.session.add(user)
    db.session.commit()

    flash('成功注册用户账号', 'success')
    return redirect(url_for('user.login'))


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """A route for existing user to login
    If the user has logged in, redirect it to the discover page.
    If the user hasn't logged in:
        If the request method is GET, send him the login page.
        If the request method is POST, check whether the provided information is valid and redirect it to appropriate page.

    :return: next page (if exist) / main.discover / login page
    """
    
    if current_user.is_authenticated:
        return redirect(url_for('main.discover'))

    form = LoginForm()

    if form.validate_on_submit():
        try:
            validate_email(form.email_or_username.data)
            user = User.query.filter_by(email=form.email_or_username.data).first()
        except EmailNotValidError:
            user = User.query.filter_by(username=form.email_or_username.data).first()

        if user := (user if user and check_password_hash(user.password_hash, form.password.data) else None):
            login_user(user, remember=False)
            flash('成功登入', 'success')

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.discover'))
        else:
            flash('用户名或密码不正确', 'danger')

    return render_template('login.html', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    """A simple route to perform logout
    
    :return: redirect to main.home
    """
    
    logout_user()
    flash('成功登出', 'success')
    return redirect(url_for('main.home'))


@user_blueprint.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    """A route for user to reset their password if they have forgotten
    
    :return: user.login if success otherwise 'forgot_password' form
    """
    
    # TODO: implement this together with automated email response

    form = ForgetPassword()
    if not form.validate_on_submit():
        return render_template('forgot password.html', form=form)
    
    flash('重新激活密码请求已发至邮箱', 'info')
    return redirect(url_for('user.login'))


@user_blueprint.route('/update_account', methods=['GET', 'POST'])
def update_account():
    """A route for existing user to update their account info,
    it can be either username, avatar, password or all of them
    
    :return: update account form view / redirect to main.discover
    """
    
    form = UpdateAccount()
    all_avatars = os.listdir(os.path.join(current_app.root_path, 'static', 'resources', 'user avatars'))
    form.avatars.choices = [(avatar, avatar) for avatar in random.sample(all_avatars, k=7)]
    # print(form.avatars.data, form.new_username.data, form.old_password.data)

    if form.validate_on_submit():
        # print("PASSED validation")
        if form.avatars.data:
            current_user.user_avatar = form.avatars.data
        if form.new_username.data:
            current_user.username = form.new_username.data
        if form.new_password.data:
            current_user.password_hash = generate_password_hash(form.new_password.data)

        db.session.commit()
        flash("用户资料成功更新", 'success')
        return redirect(url_for('main.discover'))

    return render_template('update account.html', form=form)
