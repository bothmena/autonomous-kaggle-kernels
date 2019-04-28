from lib.services.idb import IDataBase
from pymongo import MongoClient
from lib.exception.database import ProjectExistsException
from datetime import datetime


class MongodbORM(IDataBase):

    def __init__(self):
        # todo ask for user username and password to protect database.
        self.client = MongoClient('172.18.0.100', 27017)
        self.database = self.client['akk']
        self.projects = self.database.project
        self.experiences = self.database.experience
        self.search_spaces = self.database.search_space

    def authenticate(self):
        pass

    def get_project(self, path):
        return self.projects.find_one({'path': path})

    def new_project(self, project: dict):
        prj_db = self.projects.find_one({"$and": [{"name": project['name']}, {"path": project['path']}]})

        if prj_db is not None:
            raise ProjectExistsException('A project must have unique path and/or name')

        project['date'] = datetime.utcnow()
        project_id = self.projects.insert_one(project).inserted_id

        return project_id

    def new_experience(self, project_id):
        pass

    def get_experience(self, project_id):
        pass
