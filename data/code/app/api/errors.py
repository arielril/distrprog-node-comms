from flask import jsonify, json
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException


def error_response(status_code, error=None):
    payload = {
        'name': HTTP_STATUS_CODES.get(status_code, 'Unknown error'),
    }
    response = {}
    if error:
        response = error.get_response()
        payload['description'] = error.description

        if not error.code is None:
            payload['code'] = error.code

    response.data = json.dumps(payload)
    response.content_type = 'application/json'
    response.status_code = status_code
    return response


def register_handlers(app):

    @app.errorhandler(400)
    def bad_request(error):
        return error_response(400, error)

    @app.errorhandler(404)
    def not_found_handler(error):
        return error_response(404, error)

    @app.errorhandler(418)
    def tea_pot(error):
        return error_response(418, error)

    @app.errorhandler(500)
    @app.errorhandler(HTTPException)
    def internal_server_error_handler(error):
        return error_response(500, error)
