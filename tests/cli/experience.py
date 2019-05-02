from unittest import TestCase
from akk.cli.experience import get_experiences
import os


class ExperienceCLITest(TestCase):

    def test_get_experiences(self):
        experiences = get_experiences('file_not_exist.py')
        self.assertIsNone(experiences)

        filename = os.path.join(os.getcwd(), 'tests/cli/samples/experiences.py')
        experiences = get_experiences(filename)
        self.assertEqual(len(experiences), 3)
