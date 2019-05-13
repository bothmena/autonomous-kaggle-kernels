from unittest import TestCase
from akk.api import Cycle
from akk.api import Module
from torch import nn
import os
import numpy as np


class CycleTest(TestCase):

    class Network(Module):

        def __init__(self):
            super().__init__()
            self.linear = nn.Linear(10, 100)

        def forward(self, *input):
            pass

    net = Network()

    def test_01_cycles_names(self):

        cycle_1 = Cycle(None, self.net)
        self.assertEqual(cycle_1.cycle_id, 'cycle_0')
        cycle_2 = Cycle(None, self.net)
        self.assertEqual(cycle_2.cycle_id, 'cycle_1')
        cycle_3 = Cycle(None, self.net)
        self.assertEqual(cycle_3.cycle_id, 'cycle_2')

    def test_02_cycle_iter(self):

        dic = {'cycle_3': 100000, 'cycle_4': 1000000}

        cycle = Cycle(None, self.net)

        self.assertIsNone(cycle.steps)
        self.assertIsNone(cycle.max_duration)
        with self.assertRaises(ValueError) as _:
            for _ in cycle.loop():
                pass

        cycle.steps = dic[cycle.cycle_id]

        for _ in cycle.loop():
            pass

        cycle2 = Cycle(None, self.net)
        cycle2.steps = dic[cycle2.cycle_id]

        for _ in cycle2.loop():
            pass

        self.assertTrue(os.path.isfile(os.path.join(os.getcwd(), cycle.cycle_id + '.npy')))
        self.assertTrue(os.path.isfile(os.path.join(os.getcwd(), cycle2.cycle_id + '.npy')))

        self.assertTrue(os.path.isfile(os.path.join(os.getcwd(), '{}_{}.pt'.format(cycle.cycle_id, self.net.net_id))))
        self.assertTrue(os.path.isfile(os.path.join(os.getcwd(), '{}_{}.pt'.format(cycle2.cycle_id, self.net.net_id))))

        arr = np.load(os.path.join(os.getcwd(), cycle.cycle_id + '.npy'))
        arr2 = np.load(os.path.join(os.getcwd(), cycle2.cycle_id + '.npy'))

        self.assertIsInstance(arr, np.ndarray)
        self.assertIsInstance(arr2, np.ndarray)

        self.assertGreater(arr[0], 0)
        self.assertGreater(arr[1], 0)
        self.assertGreater(arr[2], 0)

        self.assertGreater(arr2[0], 0)
        self.assertGreater(arr2[1], 0)
        self.assertGreater(arr2[2], 0)

        os.remove(os.path.join(os.getcwd(), cycle.cycle_id + '.npy'))
        os.remove(os.path.join(os.getcwd(), cycle2.cycle_id + '.npy'))

        os.remove(os.path.join(os.getcwd(), '{}_{}.pt'.format(cycle.cycle_id, self.net.net_id)))
        os.remove(os.path.join(os.getcwd(), '{}_{}.pt'.format(cycle2.cycle_id, self.net.net_id)))
