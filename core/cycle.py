import time
import numpy as np


class Cycle:

    def __init__(self):
        self.networks = None
        self.start = None
        self.end = None
        # todo, get number of steps from service container -> data loader (for shared data)
        self.steps = None

    def __enter__(self):
        self.start = time.time()
        for step in range(self.steps):
            yield step

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()

    def get_run_time(self) -> float:
        return self.end - self.start

    def get_data(self) -> np.ndarray:
        return np.array([self.start, self.end, self.get_run_time()])
