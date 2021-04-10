from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from . import user_blueprint
from .forms import RegistrationForm, LoginForm
from .security import verify_user_login, register_new_user


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if not form.validate_on_submit():
        return render_template('user/register.html', form=form)

    register_new_user(form.email.data, form.username.data, form.password.data)
    flash('Successfully registered!')
    return redirect(url_for('root.index'))


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('root.index'))

    form = LoginForm()
    if not form.validate_on_submit():
        return render_template('user/login.html', form=form)

    if user := verify_user_login(form.email_or_username.data, form.password.data):
        login_user(user, remember=False)
        flash('Successfully logged in')
        if next_page := request.args.get('next'):
            return redirect(next_page)
        else:
            return redirect(url_for('root.index'))

    else:
        flash('Invalid account or password')
        return redirect(url_for('user.login'))


@user_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('root.index'))
