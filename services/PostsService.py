from .DatabaseService import DatabaseService
from .GoogleCloudService import GoogleCloudService
import datetime
import uuid
import json

__dbs = DatabaseService.get_instance()
__gcs = GoogleCloudService.get_instance()


def upload_post(user, post_data):
    post_data['post_id'] = str(uuid.uuid4())
    post_data['date'] = datetime.datetime.now()
    post_data['user_id'] = user
    post_data['media'] = []
    post_data['hidden'] = False
    data = __dbs.upload_post(post_data)
    return {'code': 200, 'message': 'Post Created!', 'data': {'post_id': post_data['post_id']}}


def upload_post_media(user_id, post_id, media):
    post = __dbs.get_post(post_id)

    if post['user_id'] == user_id:
        for m in media.keys():
            file = media.get(m)
            file_name = f"posts/{post_id}_{m}.PNG"
            response = __gcs.upload_image(file_name, file)
            post['media'].append({'name': file_name, 'url': response})
            return __dbs.update_post(post_id, post)
    return {'code': 403, 'message': "You can't update media for this post!"}


def get_posts(user, requested_user):
    if user == requested_user:
        return __dbs.get_posts_for_user(requested_user, True)
    else:
        return __dbs.get_posts_for_user(requested_user, False)


def get_timeline(user, last_id=None):
    # get following
    follwing = __dbs.get_user_data(user)['following'] or []





