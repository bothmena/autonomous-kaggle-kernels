from unittest import TestCase
from core.experience import PyTorchExperience
from torch import nn
from torch import optim


class Network(nn.Module):
    def __init__(self):
        super(Network, self).__init__()
        self.seq = nn.Sequential(
            nn.Linear(10, 100),
            nn.Linear(100, 10)
        )

    def forward(self, x):
        pass


class ExperienceTest(TestCase):

    def test_set_attributes(self):
        dic = {
            'batch_size': 64,
            'epochs': 40,
            'optimizer': 'rmsprop',
            'criterion': 'cross_entropy',
            'lr': 0.001,
            'lr_decay': False,
            'lr_cycle': None,
        }

        exp = PyTorchExperience(**dic)

        self.assertEqual(exp.batch_size, dic['batch_size'])
        self.assertEqual(exp.get_lr(), dic['lr'])
        self.assertEqual(exp.get_lr(), dic['lr'])
        self.assertIsInstance(exp.get_loss(), nn.CrossEntropyLoss)
        self.assertIsInstance(exp.get_optimizer(Network().parameters()), optim.RMSprop)

    def test_lr_decay(self):
        pass

    def test_lr_restarts(self):
        pass
