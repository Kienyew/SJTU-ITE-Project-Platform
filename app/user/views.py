from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from . import user_blueprint
from .forms import RegistrationForm, LoginForm, ForgetPassword
from .security import verify_user_login, register_new_user


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # TODO: requires email verification
    if current_user.is_authenticated:
        return redirect(url_for('main.discover'))

    form = RegistrationForm()
    if not form.validate_on_submit():
        return render_template('register.html', form=form)

    register_new_user(form.email.data, form.username.data, form.password.data)
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
    if not form.validate_on_submit():
        return render_template('login.html', form=form)

    if user := verify_user_login(form.email_or_username.data, form.password.data):
        login_user(user, remember=False)
        flash('Successfully logged in')
        if next_page := request.args.get('next'):
            return redirect(next_page)
        else:
            return redirect(url_for('main.discover'))
    else:
        flash('Invalid account or password')
        return redirect(url_for('user.login'))


@user_blueprint.route('/logout', methods=['POST'])
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
