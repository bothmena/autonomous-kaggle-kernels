from unittest import TestCase
from src.api.cycle import Cycle
import os
import numpy as np


class CycleTest(TestCase):

    def test_01_cycles_names(self):
        cycle_1 = Cycle()
        self.assertEqual(cycle_1.cycle_id, 'cycle_0')
        cycle_2 = Cycle()
        self.assertEqual(cycle_2.cycle_id, 'cycle_1')
        cycle_3 = Cycle()
        self.assertEqual(cycle_3.cycle_id, 'cycle_2')

    def test_02_cycle_iter(self):

        dic = {'cycle_3': 100000, 'cycle_4': 1000000}

        cycle = Cycle()

        self.assertIsNone(cycle.steps)
        self.assertIsNone(cycle.max_duration)
        with self.assertRaises(ValueError) as _:
            for _ in cycle.loop():
                pass

        cycle.steps = dic[cycle.cycle_id]

        for _ in cycle.loop():
            pass

        cycle2 = Cycle()
        cycle2.steps = dic[cycle2.cycle_id]

        for _ in cycle2.loop():
            pass

        self.assertTrue(os.path.isfile(os.path.join(os.getcwd(), cycle.cycle_id + '.npy')))
        self.assertTrue(os.path.isfile(os.path.join(os.getcwd(), cycle2.cycle_id + '.npy')))

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

# for loop:                                     0.6962621927261352  /  10000000 = 10M steps
# while: check only steps:                      3.5596400260925294  /  10000000 = 10M steps
# while: checks step + remaining time:          5.3298518657684330  /  10000000 = 10M steps
