from datetime import datetime

from bson import ObjectId
from pymongo import MongoClient

from akk.lib.exception import ProjectExistsException, ExperienceExistsException, CommitExistsException
from akk.lib.services.idb import IDataBase


class MongodbORM(IDataBase):

    def __init__(self):
        # todo ask for user username and password to protect database.
        self.client = MongoClient('172.18.0.100', 27017)
        self.database = self.client['akk']
        self.projects = self.database.project
        self.experiences = self.database.experience
        self.commits = self.database.commit
        self.search_spaces = self.database.search_space

    def authenticate(self):
        pass

    def get_project(self, path):
        return self.projects.find_one({'path': path})

    def new_project(self, project: dict):
        prj_db = self.projects.find_one({"$and": [{"name": project['name']}, {"path": project['path']}]})

        if prj_db is not None:
            raise ProjectExistsException()

        project['date'] = datetime.utcnow()
        project_id = self.projects.insert_one(project).inserted_id

        return project_id

    def new_experience(self, experience: dict):
        experience_cp = experience.copy()
        del experience_cp['search_space']
        exp_db = self.experiences.find_one(experience_cp)
        if exp_db is not None:
            raise ExperienceExistsException()

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

    def new_commit(self, commit: dict, prev_commit: dict = None):
        # commit = { experience: ObjectId, cycles: {steps, max_runtime: optional}
        # index: int (0: profiling, 1+: real commits)
        if prev_commit is None:
            commit['index'] = 0
        else:
            commit['index'] = prev_commit['index'] + 1
        commit_cp = commit.copy()
        del commit_cp['cycles']

        commit_db = self.commits.find_one(commit_cp)
        if commit_db is not None:
            return commit_db['_id']

        commit['date'] = datetime.utcnow()
        # status: unstarted|running|completed|failed|queued
        commit['status'] = 'unstarted'
        commit['next'] = None
        # focus: True when a commit is running or finished (success of failure) and the next commit did not started yet.
        # it makes it easier to find the running experience status and the commit for next run .find_one({experience: id, focus: True})
        commit['focus'] = commit['index'] == 0

        commit_id = self.commits.insert_one(commit).inserted_id

        return commit_id

    def get_commit(self, commit_id: str):
        return self.commits.find_one({"_id": ObjectId(commit_id)})

    def get_exp_commit(self, exp_id):
        return self.commits.find({'experience': ObjectId(exp_id)})
