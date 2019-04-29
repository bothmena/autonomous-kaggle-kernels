import time

import numpy as np

from src.api.saver import Saver


class Profiler:
    def __init__(self, cycle_id: str, steps: int):
        self.cycle_id = cycle_id
        self.steps = steps
        self.start = None
        self.end = None

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        Saver.save_numpy(self.cycle_id, np.array([self.start, self.end, self.end - self.start]))


class Cycle:
    n_cycles = 0

    def __init__(self, cycle_id: str = None):
        self._steps = None
        self._max_duration = None
        if cycle_id is None:
            self.cycle_id = 'cycle_' + str(Cycle.n_cycles)
        else:
            self.cycle_id = cycle_id
        Cycle.n_cycles += 1

    @property
    def steps(self):
        return self._steps

    @steps.setter
    def steps(self, value):
        self._steps = value

    @property
    def max_duration(self):
        return self._max_duration

    @max_duration.setter
    def max_duration(self, value):
        self._max_duration = value

    def cont(self, step: int, start_time: float):
        if self._max_duration is None:
            return step < self._steps
        else:
            return ((time.time() - start_time) < self._max_duration) and step < self._steps

    def loop(self):
        if self.steps is None:
            raise ValueError('You need to set the number of steps first.')
        with Profiler(self.cycle_id, self.steps) as p:
            step = 0
            while self.cont(step, p.start):
                step += 1
                yield step
