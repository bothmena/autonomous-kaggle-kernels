from unittest import TestCase
from core.cycle import Cycle
import os
import numpy as np


class CycleTest(TestCase):

    def test_read_config(self):
        os.chdir(os.path.join(os.getcwd(), 'examples'))
        cycle = Cycle()

        self.assertIsNone(cycle.run_time)

        for _ in cycle.loop():
            pass

        self.assertIsNotNone(cycle.run_time)
        self.assertGreater(cycle.run_time, 0)
        self.assertIsInstance(cycle.profiling_data, np.ndarray)

# for loop:                                     0.6962621927261352  /  10000000 = 10M steps
# while: check only steps:                      3.5596400260925294  /  10000000 = 10M steps
# while: checks step + remaining time:          5.3298518657684330  /  10000000 = 10M steps
