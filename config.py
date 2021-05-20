import os
from pathlib import Path


class Config:
    """General Configuration

    Remember to set the secret key for real production in environmental variable !
    """
    # Essential configuration ------------------------------------------------------------------------------------
    SECRET_KEY = os.getenv('SECRET_KEY', '$2y$18$lhZAs2L8CBs67X8AIMaa?xbmm7H0h3gnrCE6JdSWnwPDq2NZWAmq')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{Path(__file__).parent.absolute()}/data.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # User Global configuration (should probably split this into different class in the future --------------------
    USER_DEBUG_MODE = True  # REMEMBER to turn this off during real production
    POSTS_PER_PAGE = 9
    IMAGE_COMPRESSION_DESIRE_WIDTH = 1280
    IMAGE_COMPRESSION_DESIRE_HEIGHT = 1920

