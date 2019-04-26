from unittest import TestCase
from lib.services.db import MongodbORM


class MongoDBTest(TestCase):

    def test_singleton(self):
        a = MongodbORM()
        b = MongodbORM()

        self.assertEqual(a, b)

    def test_new_project(self):
        db = MongodbORM()
        project = {
            'name': 'test project',
            'path': '/workspace/BrighterAI/autonomous-kaggle-kernels',
            'repository': 'None',
            'framework': 'tensorflow',
            'cpu': False,
            'internet': False,
        }
        uid = db.new_project(project)

        project_db = db.projects.find_one({'_id': uid})

        self.assertEqual(project['name'], project_db['name'])
        self.assertEqual(project['path'], project_db['path'])
        self.assertEqual(project['repository'], project_db['repository'])
        self.assertEqual(project['framework'], project_db['framework'])
        self.assertEqual(project['cpu'], project_db['cpu'])
        self.assertEqual(project['internet'], project_db['internet'])

    def test_find_project(self):
        db = MongodbORM()
        project = {
            'name': 'test project',
            'path': '/workspace/BrighterAI/autonomous-kaggle-kernels',
            'repository': 'None',
            'framework': 'tensorflow',
            'cpu': False,
            'internet': False,
        }
        db.new_project(project)
        project_db = db.get_project(project['path'])

        self.assertEqual(project['name'], project_db['name'])
        self.assertEqual(project['path'], project_db['path'])
        self.assertEqual(project['repository'], project_db['repository'])
        self.assertEqual(project['framework'], project_db['framework'])
        self.assertEqual(project['cpu'], project_db['cpu'])
        self.assertEqual(project['internet'], project_db['internet'])
