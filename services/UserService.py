from .DatabaseService import DatabaseService
from .GoogleCloudService import GoogleCloudService
import json

dbs = DatabaseService.get_instance()
gcs = GoogleCloudService.get_instance()


def get_user_data(user_id):
    user_data = dbs.get_user_data(user_id)
    if user_data:
        return {'code': 200, 'message': 'User data fetched', 'data': user_data}
    else:
        return {'code': 404, 'message': 'Unable to fetch profile'}


def update_user_data(user_id, data):
    user_data = dbs.update_user_data(user_id, data)
    if user_data:
        return {'code': 200, 'message': 'User data updated'}
    else:
        return {'code': 404, 'message': 'Unable to update profile'}


def upload_profile_pic(user_id, image):
    file_name = f'profile/profile_pic_{user_id}.png'
    url = gcs.upload_image(file_name, image)
    data = dbs.update_user_data(user_id, {'profile_pic': url, 'profile_pic_name': file_name})
    return {'code': 200, 'message': 'Profile Picture Uploaded', 'data': data}


def follow_user(user_id, follow_user_id):
    # get if target profile is private
    target_profile = dbs.get_user_data(follow_user_id)
    my_profile = dbs.get_user_data(user_id)

    if follow_user_id in my_profile['following']:
        return {'code': 403, 'message': 'No need, you already follow this user!'}

    if target_profile['isPrivate']:
        if user_id not in target_profile['follow_request_received']:
            target_profile['follow_request_received'].append(user_id)
        if target_profile not in my_profile['follow_request_sent']:
            my_profile['follow_request_sent'].append(user_id)

    else:
        my_profile['following'].append(follow_user_id)
        target_profile['followers'].append(user_id)

    dbs.update_user_data(my_profile['user_id'], my_profile)
    dbs.update_user_data(target_profile['user_id'], target_profile)

    return {'code': 200, 'message': 'done'}


def handle_private_requests(user_id, follow_data):
    target_profile = dbs.get_user_data(follow_data['user_id'])
    my_profile = dbs.get_user_data(user_id)

    if follow_data['user_id'] in my_profile['follow_request_received']:
        if follow_data['accepted']:
            my_profile['follow_request_received'].remove(follow_data['user_id'])
            my_profile['followers'].append(follow_data['user_id'])

            target_profile['follow_request_sent'].remove(user_id)
            target_profile['following'].append(user_id)
        else:
            my_profile['follow_request_received'].remove(follow_data['user_id'])
            target_profile['follow_request_sent'].remove(user_id)
        dbs.update_user_data(my_profile['user_id'], my_profile)
        dbs.update_user_data(target_profile['user_id'], target_profile)
        return {'code': 200, 'message': 'done'}

    return {'code': 404, 'message': 'The request user has not sent a follow request'}


def unfollow_user(user_id, target_user):
    target_profile = dbs.get_user_data(target_user)
    my_profile = dbs.get_user_data(user_id)
    changed = False

    if target_user in my_profile['following']:
        my_profile['following'].remove(target_user)
        target_profile['followers'].remove(user_id)
        changed = True

    elif target_user in my_profile['follow_request_sent']:
        my_profile['follow_request_sent'].remove(target_user)
        target_profile['follow_request_received'].remove(user_id)
        changed = True

    if changed:
        dbs.update_user_data(my_profile['user_id'], my_profile)
        dbs.update_user_data(target_profile['user_id'], target_profile)
        return {'code': 200, 'message': 'done'}
    return {'code': 404, 'message': 'you do not follow the user or sent a request'}


def remove_follower(user_id, target_user):
    target_profile = dbs.get_user_data(target_user)
    my_profile = dbs.get_user_data(user_id)

    if target_user in my_profile['followers']:
        my_profile['followers'].remove(target_user)
        target_profile['following'].remove(user_id)

        dbs.update_user_data(my_profile['user_id'], my_profile)
        dbs.update_user_data(target_profile['user_id'], target_profile)

        return {'code': 200, 'message': 'done'}

    return {'code': 404, 'message': 'The user does not follow you currently'}

def get_follow_metrics():
    pass
    # profile pic, display name, user id