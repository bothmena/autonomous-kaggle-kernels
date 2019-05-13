import time

import numpy as np

from akk.api import save_load as sl
from akk.api import Module


class Profiler:
    def __init__(self, cycle_id: str, steps: int, *networks):
        self.cycle_id = cycle_id
        self.steps = steps
        if len(networks) == 0:
            raise ValueError('You should list all the networks that will be trained in the cycle')
        for network in networks:
            if not isinstance(network, Module):
                raise ValueError('All networks should be of type: ' + str(Module)[8:-2])
        self.networks = networks
        self.start = None
        self.end = None

    def __enter__(self):
        self.start = time.time()
        for network in self.networks:
            if isinstance(network, Module):
                sl.load_net_state_dict(network, cycle_id=self.cycle_id)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        sl.save_numpy(self.cycle_id, np.array([self.start, self.end, self.end - self.start]))
        for network in self.networks:
            if isinstance(network, Module):
                sl.save_net_state_dict(network, cycle_id=self.cycle_id)


class Cycle:
    n_cycles = 0

    def __init__(self, cycle_id: str = None, *networks):
        self._steps = None
        self._max_duration = None
        if len(networks) == 0:
            raise ValueError('You should list all the networks that will be trained in the cycle')
        for network in networks:
            if not isinstance(network, Module):
                raise ValueError('All networks should be of type: ' + str(Module)[8:-2])
        self.networks = networks
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
        with Profiler(self.cycle_id, self.steps, *self.networks) as p:
            step = 0
            while self.cont(step, p.start):
                step += 1
                yield step
