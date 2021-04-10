from typing import Optional

from email_validator import validate_email, EmailNotValidError
from werkzeug.security import generate_password_hash, check_password_hash

from .. import db
from .models import User


def register_new_user(email: str, username: str, password: str):
    user = User(email=email, username=username)
    user_set_password(user, password)
    db.session.add(user)
    db.session.commit()


def user_set_password(user: User, password: str):
    user.password_hash = generate_password_hash(password)


def verify_user_login(username_or_email: str, password: str) -> Optional[User]:
    '''
    Verify a user when they submit the login form, return the corresponding
    user if verification success or else 'None'.
    '''
    try:
        validate_email(username_or_email)
        user = User.query.filter_by(email=username_or_email).first()
    except EmailNotValidError:
        user = User.query.filter_by(username=username_or_email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return None
    else:
        return user
