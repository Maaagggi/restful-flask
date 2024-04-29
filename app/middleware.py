from flask import jsonify


class MissingCredentialsError(Exception):
    def __init__(self, message="Missing username or password"):
        self.message = message


class UsernameExistsError(Exception):
    def __init__(self, message="Username already exists"):
        self.message = message


class InvalidUsernameOrPassword(Exception):
    def __init__(self, message="Invalid username or password"):
        self.message = message


def error_handling_middleware(app):
    def middleware_wrapper(environ, start_response):
        try:
            return app(environ, start_response)
        except (MissingCredentialsError, UsernameExistsError, InvalidUsernameOrPassword) as e:
            response = jsonify({'error': e.message})
            return response(environ, start_response)

    return middleware_wrapper
