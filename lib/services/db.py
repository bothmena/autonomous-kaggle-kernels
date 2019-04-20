from lib.services.idb import IDataBase
from pymongo import MongoClient


class MongoDB(IDataBase):

    def __init__(self, project_id, experience_id, *args, **kwargs):
        # todo ask for user username and password to protect database.
        self.client = MongoClient('localhost', 27017)
        self.project_id = project_id
        self.experience_id = experience_id

    def authenticate(self):
        pass

    def get_project(self, project_id):
        pass

    def new_project(self, project_id):
        pass

    def new_experience(self, project_id):
        pass

    def get_experience(self, project_id):
        pass
