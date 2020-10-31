import json
from flask import Blueprint, request, jsonify
import services.PostsService as PostsService
from decorators.authDecorator import authenticate

Post = Blueprint('posts_api', __name__)


@Post.route('/newpost', methods=['POST'])
@authenticate
def new_post():
    user = request.headers.get('user_id')
    data = json.loads(request.data)
    return PostsService.upload_post(user, data)


@Post.route('/postmedia', methods=['POST'])
@authenticate
def post_media():
    images = request.files
    user = request.headers.get('user_id')
    post_id = request.headers.get('post_id')
    return PostsService.upload_post_media(user, post_id, images)


@Post.route('/getposts', methods=['GET'])
@authenticate
def get_posts():
    requested_for = json.loads(request.data)['requested_for']
    user = request.headers.get('user_id')
    return jsonify(PostsService.get_posts(user, requested_for))
