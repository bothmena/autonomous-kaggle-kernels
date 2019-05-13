import numpy as np
import torch
from akk.api.module import Module


class Saver:
    @classmethod
    def save_numpy(cls, filename: str, data: (np.ndarray, list)):
        if isinstance(data, list):
            data = np.array(data)
        np.save(filename, data)

    @classmethod
    def save_net_state_dict(cls, net: Module, cycle_id: str = None):
        if cycle_id:
            filename = '{}_{}.pt'.format(cycle_id, net.net_id)
        else:
            filename = net.net_id + '.pt'
        torch.save(net.state_dict(), filename)
