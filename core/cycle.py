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

    def __init__(self):
        self.container = ServiceContainer()
        # todo, get number of steps from service container -> database
        self.steps = 10000000
        self.max_seconds = 100
        self.run_time = None
        self.profiling_data = None

    def cont(self, step: int, start_time: float):
        if self.max_seconds is None:
            return step < self.steps
        else:
            return ((time.time() - start_time) < self.max_seconds) and step < self.steps

    def loop(self):
        with Profiler() as p:
            step = 0
            while self.cont(step, p.start):
                step += 1
                yield step

        self.run_time = p.end - p.start
        self.profiling_data = np.array([p.start, p.end, self.run_time])
