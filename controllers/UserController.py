import json
from flask import Blueprint, request, send_file
from decorators.authDecorator import authenticate
import services.UserService as UserService

User = Blueprint('user_api', __name__)
UPLOAD_FOLDER = '../images/'


@User.route('profile', methods=['GET'])
@authenticate
def get_user_profile():
    user = request.headers.get('user_id')
    return UserService.get_user_data(user)


@User.route('update_profile', methods=['PUT'])
@authenticate
def update_user_profile():
    user = request.headers.get('user_id')
    data = json.loads(request.data)
    return UserService.update_user_data(user, data)


@User.route('upload_picture', methods=['POST'])
@authenticate
def update_profile_picture():
    user = request.headers.get('user_id')
    image = request.files['picture']
    return UserService.upload_profile_pic(user, image)


@User.route('follow', methods=['POST'])
@authenticate
def follow_user():
    user = request.headers.get('user_id')
    follow = json.loads(request.data)['follow_user']
    UserService.follow_user(user, follow)


@User.route('follow-metrics', methods=['POST'])
@authenticate
def follow_metrics():
    user = request.headers.get('user_id')
    UserService.follow_user(user, follow)



@User.route('follow_action', methods=['POST'])
@authenticate
def follow_user_action():
    user = request.headers.get('user_id')
    follow_data = json.loads(request.data)['target_user']
    UserService.handle_private_requests(user, follow_data)

