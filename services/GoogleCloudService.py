from google.cloud import storage
from os import path

SERVICEKEY = path.join(path.dirname(__file__), '../gcpkey.json')


class GoogleCloudService:
    __instance = None
    __storage_client = None
    __profile_pic_bucket = None

    @staticmethod
    def get_instance():
        if GoogleCloudService.__instance is None:
            GoogleCloudService.__instance = GoogleCloudService()

        return GoogleCloudService.__instance

    def __init__(self):
        if GoogleCloudService.__instance is not None:
            raise Exception("This class is a singleton, access via .instance() method!")
        else:
            self.__storage_client = storage.Client.from_service_account_json(SERVICEKEY)
            self.__profile_pic_bucket = self.__storage_client.get_bucket('pics-webtech')

    def upload_image(self, file_name, file):
        picture = self.__profile_pic_bucket.blob(file_name)
        picture.upload_from_file(file)
        return picture.public_url
