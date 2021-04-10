from flask import render_template, redirect, url_for, flash

from . import user_blueprint
from .forms import RegistrationForm
from .models import User
from .. import db


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if not form.validate_on_submit():
        return render_template('user/register.html', form=form)

    user = User(email=form.email.data,
                username=form.username.data)

    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Successfully registered!')
    return redirect(url_for('root.index'))
