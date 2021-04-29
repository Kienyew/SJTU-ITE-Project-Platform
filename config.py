import os
from pathlib import Path


class Config:
    """General Configuration
    
    Remember to set secret key in the environmental variable !
    """
    SECRET_KEY = os.getenv('SECRET_KEY', '$2y$18$lhZAs2L8CBs67X8AIMaa?xbmm7H0h3gnrCE6JdSWnwPDq2NZWAmq')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{Path(__file__).parent.absolute()}/data.sqlite'
    # print(SQLALCHEMY_PARENT_DIR, SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
