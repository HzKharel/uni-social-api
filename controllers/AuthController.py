import json
from flask import Blueprint, request
import services.AuthService as AuthService

Auth = Blueprint('auth_api', __name__)


@Auth.route('/login', methods=['POST'])
def login():
    try:
        data = json.loads(request.data)
        return AuthService.login_user(data)
    except:
        return {'code': 500, 'message': "He's dead, Jim!"}


@Auth.route('/register', methods=['POST'])
def register():
    data = json.loads(request.data)
    return AuthService.register(data['reg_data'], data['profile_data'])


@Auth.route('/verify-token', methods=['GET'])
def verify_token():
    return AuthService.verify_token(request.headers.get('token'))


@Auth.route('/refresh-token', methods=['POST'])
def swap_token():
    token = request.headers.get('token')
    refresher_token = request.headers.get('refresher')
    return AuthService.refresh_token(token, refresher_token)

