from typing import Optional

from email_validator import validate_email, EmailNotValidError
from werkzeug.security import generate_password_hash, check_password_hash

from .. import db
from .models import User


def register_new_user(email: str, username: str, password: str):
    user = User(email=email, username=username, password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()


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

    return user if user and check_password_hash(user.password_hash, password) else None
