from unittest import TestCase
from akk.cli.project import init_project
import random
import string


def random_string(length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_letters + ' ' + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


class ProjectInitTestSuite(TestCase):

    project_temp = {
        'name': None,
        'alias': None,
        'path': None,
        'repository': None,
        'framework': 'pytorch',
        'cpu': False,
        'internet': False,
        'entrypoint': 'main.py',
        'datasets': [],
        'kernels': [],
        'competitions': [],
        'public': False,
        'k_type': 'notebook',
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
