import os
from datetime import datetime
from unittest import TestCase

from bson import ObjectId
from slugify import slugify

from akk.lib.exception import ProjectExistsException, ExperienceExistsException
from akk.lib.services import MongodbORM


class MongoDBTest(TestCase):
    project = {
        'name'        : 'test project',
        'alias'       : 'test project',
        'path'        : '/tmp/test_akk_project',
        'repository'  : None,
        'entrypoint'  : 'main.py',
        'framework'   : 'tensorflow',
        'datasets'    : [],
        'kernels'     : [],
        'competitions': [],
        'cpu'         : False,
        'internet'    : False,
        'private'     : False,
        'type'        : 'notebook',
        'date'        : datetime.now(),
    }
    # todo: update experience attributes
    experience = {
        'search_space': None,
        'batch_size'  : 64,
        'status'      : 'running',
        'git_commit'  : 'a654as4df5',
        'optimizer'   : 'adam',
        'opt_args'    : {'arg1': 5, 'arg2': 'str'},
        'networks'    : {
            'main_net': {
                'lr'       : 'cross_entropy',
                'lr_decay' : 'cross_entropy',
                'lr_cycle' : 'cross_entropy',
                'loss'     : 'cross_entropy',
                'loss_args': {'arg1': 5, 'arg2': 'str'},
            }
        },
        'cycles'      : {
            "main_cycle": {
                "steps"            : 200,
                "unit_running_time": None
            }
        },
        'date'        : datetime.now(),
    }
    db = MongodbORM()

    if not os.path.isdir(project['path']):
        os.mkdir(project['path'])
    prj = db.get_project(project['path'])
    if prj is not None:
        db.projects.delete_one({'_id': prj['_id']})

    def test_singleton(self):
        a = MongodbORM()
        b = MongodbORM()

        self.assertEqual(a, b)

    def test_new_project(self):
        uid = self.db.new_project(self.project)

        project_db = self.db.projects.find_one({'_id': uid})

        keys = list(self.project.keys())
        keys.pop(keys.index('date'))
        for key in keys:
            self.assertEqual(self.project[key], project_db[key])

        self.db.projects.delete_one({'_id': uid})

    def test_get_project(self):
        uid = self.db.new_project(self.project)
        project_db = self.db.get_project(self.project['path'])

        keys = list(self.project.keys())
        keys.pop(keys.index('date'))
        for key in keys:
            self.assertEqual(self.project[key], project_db[key])

        self.db.projects.delete_one({'_id': uid})

    def test_unique_name(self):
        uid = self.db.new_project(self.project)
        self.assertRaises(ProjectExistsException, self.db.new_project, self.project)

        self.db.projects.delete_one({'_id': uid})

    def test_new_experience(self):
        p_uid = self.db.new_project(self.project)
        self.experience['project'] = p_uid

        e_uid = self.db.new_experience(self.experience)
        exp_db = self.db.experiences.find_one({'_id': e_uid})
        project = self.db.projects.find_one({'_id': p_uid})

        keys = list(self.experience.keys()) + ['project']
        keys.pop(keys.index('date'))
        for key in keys:
            self.assertEqual(self.experience[key], exp_db[key])

        name = project['alias'] + ' ' + str(exp_db['_id'])
        self.assertIsInstance(exp_db['project'], ObjectId)
        self.assertEqual(exp_db['kernel_name'], name)
        self.assertEqual(exp_db['kernel_id'], 'bothmena/' + slugify(name))

        self.db.experiences.delete_one({'_id': e_uid})
        self.db.projects.delete_one({'_id': p_uid})

    def test_unique_experience(self):
        p_uid = self.db.new_project(self.project)
        self.experience['project'] = p_uid
        e_uid = self.db.new_experience(self.experience)

        self.assertRaises(ExperienceExistsException, self.db.new_experience, self.experience)

        self.experience['search_space'] = p_uid
        self.assertRaises(ExperienceExistsException, self.db.new_experience, self.experience)

        self.db.experiences.delete_one({'_id': e_uid})
        self.db.projects.delete_one({'_id': p_uid})

    def test_get_experience(self):
        p_uid = self.db.new_project(self.project)
        self.experience['project'] = p_uid
        e_uid = self.db.new_experience(self.experience)

        exp_db = self.db.get_experience(str(e_uid))

        keys = list(self.experience.keys()) + ['project']
        keys.pop(keys.index('date'))
        for key in keys:
            self.assertEqual(self.experience[key], exp_db[key])

        self.db.experiences.delete_one({'_id': e_uid})
        self.db.projects.delete_one({'_id': p_uid})
