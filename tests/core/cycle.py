from unittest import TestCase
from core.cycle import Cycle
from torch.nn import Module


class MyCycle(Cycle):

    def __init__(self, net: Module, basename: str):
        super(MyCycle, self).__init__(net, basename)
        assert self.net is not None

    def loop(self):
        for i in self.cycles:
            print('epoch: ', i+1, '/', self.cycles)


class Net(Module):

    def forward(self, x):
        return x


class CycleTest(TestCase):

    def test_read_config(self):
        cycle = MyCycle(Net(), 'net')

        w_path = '/home/bothmena/Projects/PyCharm/BrighterAI/autonomous-kaggle-kernels/examples/weights'
        self.assertEqual(cycle.cycle, 2)
        self.assertEqual(cycle.cycles, 5)
        self.assertEqual(cycle.w_path, w_path)

