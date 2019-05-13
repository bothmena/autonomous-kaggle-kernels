from unittest import TestCase
from akk.lib.services.singleton import Singleton


class Service(metaclass=Singleton):
    def __init__(self):
        self.x = 5


class IServiceTest(TestCase):

    def test_is_singleton(self):
        a = Service()
        b = Service()

        b.x = 10

        self.assertEqual(a.x, b.x, 'Attribute values are not equal!')
        self.assertEqual(a, b, 'Objects are not equal!')
