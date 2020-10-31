import pymongo


class DatabaseService:
    __instance = None
    __database_uri = "mongodb://localhost:27017/"
    __db_name = 'uniSocial'

    @staticmethod
    def get_instance():
        if DatabaseService.__instance is None:
            DatabaseService.__instance = DatabaseService()

        return DatabaseService.__instance

    def __init__(self):
        if DatabaseService.__instance is not None:
            raise Exception("This class is a singleton, access via .instance() method!")
        else:
            self.client = pymongo.MongoClient(self.__database_uri)
            self.client.drop_database('test_db')
            self.db = self.client[self.__db_name]

    def get_user_account(self, user_name):
        data = self.db['user_accounts'].find_one({'email': user_name})
        if data is not None:
            del data['_id']
        return data

    def register_user(self, data):
        return self.db['user_accounts'].insert_one(data)

    def get_user_data(self, user_id):
        data = self.db['user_profile'].find_one({'user_id': user_id})
        if data is not None:
            del data['_id']
        return data

    def set_user_data(self, user_data):
        return self.db['user_profile'].insert_one(user_data)

    def update_user_data(self, user_id, data):
        data = self.db['user_profile'].find_one_and_update(
            {'user_id': user_id},
            {'$set': data},
            upsert=True,
            return_document=pymongo.ReturnDocument.AFTER)
        del data['_id']
        return data

    def upload_post(self, post_data):
        return self.db['posts'].insert_one(post_data)

    def get_post(self, post_id):
        return self.db['posts'].find_one({'post_id': post_id})

    def update_post(self, post_id, data):
        data = self.db['posts'].find_one_and_update(
            {'post_id': post_id},
            {'$set': data},
            upsert=True,
            return_document=pymongo.ReturnDocument.AFTER)
        del data['_id']
        return data

    def black_list_token(self, token, expiry):
        return self.db['black_list'].insert_one({'token': token, 'expiresAt': expiry})

    def is_token_black_listed(self, token):
        return True if self.db['black_list'].find_one({'token': token}) else False

    def is_user_name_taken(self, display_name):
        return True if self.db['user_account'].find_one({'display_name': display_name}) else False

    def is_profile_private(self, user_id):
        data = self.db['user_profile'].find_one({'user_id': user_id})
        return True if data['isPrivate'] else False

    def update_follow_request(self, target_id, follow_data):
        return self.db['user_profile'].find_one_and_update(
            {'user_id': target_id},
            {'$set': follow_data},
            upsert=True,
            return_document=pymongo.ReturnDocument.AFTER)

    def get_posts_for_user(self, user, show_hidden):
        posts = []
        for post in self.db['posts'].find({'user_id': user, 'hidden': not show_hidden}):
            del post['_id']
            post['date'] = str(post['date'])
            posts.append(post)

        return posts

    def get_post_db_id(self, post_id):
        post = self.db['posts'].find_one({'post_id': post_id})
        if post:
            return post['_id']
        return None

    def get_timeline_posts(self, following_users, last_id=None):
        posts = []
        if last_id is None:
            # When it is first page
            cursor = self.db['posts'].find({'user_id': {'$in': following_users}})
        else:
            cursor = self.db['posts'].find({'_id': {'$gt': last_id}, 'user_id': {'$in': following_users}}).limit(50)

        for p in cursor:
            del p['_id']
            p['date'] = str(p['date'])
            posts.append(p)
        return posts

    def get_follow_metrics(self, user_id):
        pass


# use minio for local image storage
