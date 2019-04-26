from unittest import TestCase
from lib.services.db import MongodbORM
from lib.exception.database import ProjectExistsException


class MongoDBTest(TestCase):

    project = {
        'name': 'test project',
        'path': '/workspace/BrighterAI/autonomous-kaggle-kernels',
        'repository': 'None',
        'framework': 'tensorflow',
        'cpu': False,
        'internet': False,
    }
    db = MongodbORM()

    def test_singleton(self):
        a = MongodbORM()
        b = MongodbORM()

        self.assertEqual(a, b)

    def test_new_project(self):
        uid = self.db.new_project(self.project)

        project_db = self.db.projects.find_one({'_id': uid})

        self.assertEqual(self.project['name'], project_db['name'])
        self.assertEqual(self.project['path'], project_db['path'])
        self.assertEqual(self.project['repository'], project_db['repository'])
        self.assertEqual(self.project['framework'], project_db['framework'])
        self.assertEqual(self.project['cpu'], project_db['cpu'])
        self.assertEqual(self.project['internet'], project_db['internet'])

        self.db.projects.delete_one({'_id': uid})

    def test_get_project(self):
        uid = self.db.new_project(self.project)
        project_db = self.db.get_project(self.project['path'])

        self.assertEqual(self.project['name'], project_db['name'])
        self.assertEqual(self.project['path'], project_db['path'])
        self.assertEqual(self.project['repository'], project_db['repository'])
        self.assertEqual(self.project['framework'], project_db['framework'])
        self.assertEqual(self.project['cpu'], project_db['cpu'])
        self.assertEqual(self.project['internet'], project_db['internet'])

        self.db.projects.delete_one({'_id': uid})

    def test_unique_name(self):
        uid = self.db.new_project(self.project)
        self.assertRaises(ProjectExistsException, self.db.new_project, self.project)

        self.db.projects.delete_one({'_id': uid})
