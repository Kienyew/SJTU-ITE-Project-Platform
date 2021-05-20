from flask import render_template
from . import errors_blueprint

@errors_blueprint.app_errorhandler(404)
def error_404(error):
    """404 means not found
    
    :param error:
    :return: a custom error webpage and http status
    """
    
    return render_template('404.html'), 404

@errors_blueprint.app_errorhandler(403)
def error_403(error):
    """403 means forbidden access
    
    :param error:
    :return: a custom error webpage and http status
    """
    
    return render_template('403.html'), 403

@errors_blueprint.app_errorhandler(500)
def error_500(error):
    """500 means Internal Server Error
    
    :param error:
    :return: a custom error webpage and http status
    """
    
    return render_template('500.html'), 500


