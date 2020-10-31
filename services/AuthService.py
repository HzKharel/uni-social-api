from .DatabaseService import DatabaseService
import bcrypt
import jwt
import datetime
import uuid

__dbs = DatabaseService.get_instance()
secret_key = 'this is a super secret key'


def login_user(user_data):

    db_user = __dbs.get_user_account(user_data['email'])

    if db_user is None:
        return {'code': 404, 'message': 'An account with that email does not exist!'}
    elif bcrypt.checkpw(user_data['password'].encode('utf8'), db_user['password']):
        token = get_token(db_user['user_id'])
        profile = __dbs.get_user_data(db_user['user_id'])
        return {'code': 200, 'message': 'Login Successful', 'token': token, 'profile': profile}

    return {'code': 404, 'message': 'The Username and password combination do not match'}


def register(user_data, profile_data):

    db_usr = __dbs.get_user_account(user_data['email'])
    if __dbs.is_user_name_taken(profile_data['display_name']):
        return {'code': 409, 'message': 'Sorry that display name is already taken!'}

    if not db_usr:
        user_data['user_id'] = str(uuid.uuid4())
        user_data['creation_date'] = datetime.datetime.today().strftime('%d/%m/%Y')
        user_data['password'] = bcrypt.hashpw(user_data['password'].encode('utf8'), bcrypt.gensalt())

        profile_data['user_id'] = user_data['user_id']

        profile_data['followers'] = []
        profile_data['following'] = []
        profile_data['follow_request_received'] = []
        profile_data['follow_request_sent'] = []

        token = get_token(user_data['user_id'])

        if __dbs.register_user(user_data) and __dbs.set_user_data(profile_data):
            return {'code': 200, 'message': 'Registration Complete', 'token': token,
                    'data': __dbs.get_user_data(user_data['user_id'])}
        else:
            return {'code': 500, 'message': 'Failed to register, please try again'}
    else:
        return {'code': 409, 'message': 'Sorry an account with that email already exists'}


def get_token(user_id):
    exp_time = datetime.datetime.utcnow() + datetime.timedelta(hours=48)
    return jwt.encode({'user_id': user_id, 'exp': exp_time}, secret_key).decode('utf-8')


def get_token_refresh(credentials):
    exp_time = datetime.datetime.utcnow() + datetime.timedelta(days=90)
    credentials['exp'] = exp_time
    return jwt.encode(credentials, secret_key).decode('utf-8')


def verify_token(token):
    if token:
        try:
            decoded = jwt.decode(token, secret_key)
        except jwt.PyJWTError as e:
            return {'verified': False, 'message': str(e)}
        return {'verified': True, 'message': decoded}
    return {'verified': False, 'message': 'No token provided'}


def refresh_token(token,refresher_token):
    verification = verify_token(token)
    if verification['verified']:
        token_data = verification['message']
        return {'code': 200,
                'message': 'Token Refreshed',
                'token': get_token(token_data['user_id']),
                'refresh_token': refresher_token}

    elif not __dbs.is_token_black_listed(refresher_token):

        credentials = verify_token(refresher_token)
        if credentials['verified']:
            cred_data = credentials['message']
            login_details = login_user({'user_name': cred_data['user_name'], 'password': cred_data['password']})
            new_refresh_token = get_token_refresh(credentials)
            __dbs.black_list_token(refresher_token, cred_data['exp'])

            if login_details.get('code') == 200:
                return {'code': 200, 'message': 'Token Refreshed',
                        'token': login_details.get('token'),
                        'refresh_token': new_refresh_token}

    return {'code': 403, 'message': 'Unable to confirm identity'}


