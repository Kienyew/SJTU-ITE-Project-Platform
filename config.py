import os
from pathlib import Path


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{Path(__file__).parent.absolute() / "data.sqlite"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
