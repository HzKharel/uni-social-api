from functools import wraps
from flask import g, request
import services.AuthService as AuthService


def authenticate(usr):
    @wraps(usr)
    def auth(*args, **kwargs):
        token = request.headers.get('token')
        res = AuthService.verify_token(token)
        if res['verified'] and res['message']['user_id'] == request.headers.get('user_id'):
            return usr(*args, **kwargs)
        return {'code': 403, 'message': 'You must be logged in to perform this action'}

    return auth
