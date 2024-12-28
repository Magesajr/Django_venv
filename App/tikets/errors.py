from flask import redirect,render_template,jsonify,request
from .import tickets

from flask_httpauth import HTTPBasicAuth

auth=HTTPBasicAuth()

@tickets.app_errorhandler(404)
def page_not_found(e):
    response=jsonify({'error':'page not found'})
    response.status_code=404
    return response

@tickets.app_errorhandler(500)
def server_error(e):
    if request.accept_mimetypes.accept_json\
        and not request.accept_mimetypes.accept_html:
        response=jsonify({'error':'internal server error'})
        response.status_code=500
        return response
    return render_template('errors/500.html'),500

@tickets.app_errorhandler(403)
def forbidden(e):
    response=jsonify({'error':'forbidden'})
    response.status_code=403
    return render_template('errors/403.html'),403
    


def unauthorized(message):
    response=jsonify({'error':message})
    response.status_code=401
    return response