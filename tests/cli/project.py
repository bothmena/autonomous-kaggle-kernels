import os
import shutil
import random
import string
from unittest import TestCase

from git import Repo
from akk.cli.project import init_project
from akk.lib.exception import NoRepoException
from akk.lib.services import MongodbORM


def random_string(length: int = 10, spaces: bool = True, digits: bool = True) -> str:
    """Generate a random string of fixed length """
    letters = string.ascii_letters
    if spaces:
        letters += ' '
    if digits:
        letters += string.digits
    return ''.join(random.choice(letters) for _ in range(length))


orm = MongodbORM()
abs_path = '/home/bothmena/Projects/PyCharm/BrighterAI/autonomous-kaggle-kernels/examples'
project_dir = 'test_project'
project_path = os.path.join(abs_path, project_dir)


class ProjectInitTestSuite(TestCase):
    project_temp = {
        'name'        : None,
        'alias'       : None,
        'path'        : None,
        'repository'  : None,
        'framework'   : 'pytorch',
        'cpu'         : False,
        'internet'    : False,
        'entrypoint'  : 'main.py',
        'datasets'    : [],
        'kernels'     : [],
        'competitions': [],
        'public'      : False,
        'k_type'      : 'notebook',
    }

    def test_project_name_length(self):
        project = self.project_temp.copy()
        project['name'] = random_string(4)
        self.assertRaises(ValueError, init_project, **project)

        project['name'] = random_string(51)
        self.assertRaises(ValueError, init_project, **project)

    def test_project_alias_length(self):
        project = self.project_temp.copy()
        project['name'] = random_string(40)
        project['alias'] = random_string(26)
        self.assertRaises(ValueError, init_project, **project)

    def test_project_repository(self):
        project = self.project_temp.copy()
        project['name'] = random_string(40)
        dirname = random_string(25, spaces=False, digits=False)
        path = os.path.join(abs_path, dirname)
        os.mkdir(path)
        project['path'] = path
        self.assertRaises(NoRepoException, init_project, **project)

        Repo.init(path)
        init_project(**project)

        project_db = orm.get_project(path)

        self.assertEqual(project_db['path'], path)
        self.assertIsNone(project_db['repository'])

        shutil.rmtree(path, ignore_errors=True)
        orm.projects.delete_one({'_id': project_db['_id']})

        self.assertFalse(os.path.isdir(path))

    def test_init_project_values(self):

        project = self.project_temp.copy()
        project['name'] = 'Test Project'
        project['path'] = project_path

        init_project(**project)

        project['alias'] = project['name'][:25]
        project['private'] = not project['public']
        project['type'] = project['k_type']
        del project['public']
        del project['k_type']

        project_db = orm.get_project(project_path)

        for key, value in project.items():
            self.assertEqual(project[key], project_db[key])

        orm.projects.delete_one({'_id': project_db['_id']})
