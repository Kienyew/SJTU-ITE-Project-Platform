import os
import random
from email_validator import validate_email, EmailNotValidError
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import user_blueprint
from .forms import RegistrationForm, LoginForm, ForgetPassword, UpdateAccount
from .models import User
from .. import db


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # TODO: require email verification
    if current_user.is_authenticated:
        return redirect(url_for('main.discover'))

    form = RegistrationForm()
    if not form.validate_on_submit():
        return render_template('register.html', form=form)

    user = User(email=form.email.data, username=form.username.data, password_hash=generate_password_hash(form.password.data))
    db.session.add(user)
    db.session.commit()
    flash('Successfully registered!')
    
    return redirect(url_for('user.login'))


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route for user login.

    If the user has logged in, redirect it to the discover page.
    If the user hasn't logged in:
        If the request method is GET, send him the login page.
        If the request method is POST, check whether the provided information is valid and redirect it to appropriate page.

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
            flash('Successfully logged in')

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.discover'))
        else:
            flash('Invalid account or password')
    
    return render_template('login.html', form=form)


@user_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.home'))


@user_blueprint.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    # TODO: implement this together with automated email response

    form = ForgetPassword()
    if not form.validate_on_submit():
        return render_template('forgot password.html', form=form)

    return redirect(url_for('user.login'))


@user_blueprint.route('/update_account', methods=['GET', 'POST'])
def update_account():
    form = UpdateAccount()
    all_avatars = os.listdir("/Users/lunafreya/GitProjects/upgraded-happiness/app/static/resources/user avatars")
    form.avatars.choices = [(avatar, avatar) for avatar in random.sample(all_avatars, k=8)]
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
        flash("Your account has been updated", 'success')
        return redirect(url_for('main.discover'))
    
    # print(form.errors)
    
    return render_template('update account.html', form=form)
