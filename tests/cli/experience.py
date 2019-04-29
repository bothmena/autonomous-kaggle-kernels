from unittest import TestCase
from src.cli.experience import _get_experiences
import os


class ExperienceCLITest(TestCase):

    def test_get_experiences(self):
        experiences = _get_experiences('file_not_exist.py')
        self.assertIsNone(experiences)

        filename = os.path.join(os.getcwd(), 'tests/cli/samples/experiences.py')
        experiences = _get_experiences(filename)
        self.assertEqual(len(experiences), 3)
