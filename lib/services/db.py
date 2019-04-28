from lib.services.idb import IDataBase
from pymongo import MongoClient
from lib.exception.database import ProjectExistsException, ExperienceExistsException
from datetime import datetime
from bson import ObjectId


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

    def new_experience(self, experience: dict):
        experience_cp = experience.copy()
        del experience_cp['search_space']
        exp_db = self.experiences.find_one(experience_cp)
        if exp_db is not None:
            raise ExperienceExistsException('same experience for the same project already exists')

        experience['date'] = datetime.utcnow()
        experience_id = self.experiences.insert_one(experience).inserted_id

        return experience_id

    def get_experience(self, exp_id: str, project_id: str = None):
        """
        :param exp_id: the first 10 characters of the experience ObjectId
        :param project_id: experience's project id
        :return: experience or None
        :rtype: dict
        """
        # cond = "this._id.str.match(/^{}*/)".format(exp_id)
        if project_id is None:
            criteria = {"_id": ObjectId(exp_id)}
        else:
            criteria = {"_id": ObjectId(exp_id), 'project': project_id}
        exp = self.experiences.find_one(criteria)
        return exp
