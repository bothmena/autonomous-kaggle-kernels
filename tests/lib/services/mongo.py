from unittest import TestCase
from src.lib.services.db import MongodbORM
from src.lib.exception import ProjectExistsException, ExperienceExistsException


class MongoDBTest(TestCase):
    project = {
        'name'      : 'test project',
        'path'      : '/workspace/BrighterAI/SimGAN_Implementation',
        'repository': None,
        'framework' : 'tensorflow',
        'cpu'       : False,
        'internet'  : False,
    }
    experience = {
        'search_space': None,
        'batch_size'  : 64,
        'epochs'      : 40,
        'lr'          : 'cross_entropy',
        'lr_decay'    : 'cross_entropy',
        'lr_cycle'    : 'cross_entropy',
        'optimizer'   : 'adam',
        'opt_args'    : {'arg1': 5, 'arg2': 'str'},
        'loss'        : 'cross_entropy',
        'loss_args'   : {'arg1': 5, 'arg2': 'str'},
    }
    db = MongodbORM()

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
        self.experience['project'] = str(p_uid)

        e_uid = self.db.new_experience(self.experience)
        exp_db = self.db.experiences.find_one({'_id': e_uid})

        keys = list(self.experience.keys()) + ['project']
        keys.pop(keys.index('date'))
        for key in keys:
            self.assertEqual(self.experience[key], exp_db[key])

        self.db.experiences.delete_one({'_id': e_uid})
        self.db.projects.delete_one({'_id': p_uid})

    def test_unique_experience(self):
        p_uid = self.db.new_project(self.project)
        self.experience['project'] = str(p_uid)
        e_uid = self.db.new_experience(self.experience)

        self.assertRaises(ExperienceExistsException, self.db.new_experience, self.experience)

        self.experience['search_space'] = str(p_uid)
        self.assertRaises(ExperienceExistsException, self.db.new_experience, self.experience)

        self.db.experiences.delete_one({'_id': e_uid})
        self.db.projects.delete_one({'_id': p_uid})

    def test_get_experience(self):
        p_uid = self.db.new_project(self.project)
        self.experience['project'] = str(p_uid)
        e_uid = self.db.new_experience(self.experience)

        exp_db = self.db.get_experience(str(e_uid))

        keys = list(self.experience.keys()) + ['project']
        keys.pop(keys.index('date'))
        for key in keys:
            self.assertEqual(self.experience[key], exp_db[key])

        self.db.experiences.delete_one({'_id': e_uid})
        self.db.projects.delete_one({'_id': p_uid})
