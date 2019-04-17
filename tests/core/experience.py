from unittest import TestCase
from core.experience import Experience


class ExperienceTest(TestCase):

    def test_get_attributes(self):
        v1 = 0.001
        v2 = 64
        v3 = 0.9
        exp = Experience(lr=v1, batch_size=v2, momentum=v3)

        self.assertIsNone(getattr(exp, 'epoch'))
        self.assertEqual(getattr(exp, 'lr'), v1)
        self.assertEqual(getattr(exp, 'lr'), exp.lr_decay())
        self.assertEqual(getattr(exp, 'batch_size'), v2)
        self.assertEqual(getattr(exp, 'momentum'), v3)
