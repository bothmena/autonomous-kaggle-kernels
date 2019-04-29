import time
import numpy as np
from lib.services.container import ServiceContainer


class Profiler:
    def __init__(self):
        self.start = None
        self.end = None

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()


class Cycle:

    n_cycles = 0

    def __init__(self, cycle_id: str = None):
        self.container = ServiceContainer()
        self._steps = None
        self._max_duration = None
        self.run_time = None
        self.profiling_data = None
        if cycle_id is None:
            self.cycle_id = 'cycle_' + str(self.n_cycles)
        else:
            self.cycle_id = cycle_id
        self.n_cycles += 1

    @property
    def step(self):
        return self._steps

    @step.setter
    def step(self, value):
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
        with Profiler() as p:
            step = 0
            while self.cont(step, p.start):
                step += 1
                yield step

        self.run_time = p.end - p.start
        self.profiling_data = np.array([p.start, p.end, self.run_time, step])
