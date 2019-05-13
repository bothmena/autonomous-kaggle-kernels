import numpy as np
import torch
import os

from akk.api.module import Module


def save_numpy(filename: str, data: (np.ndarray, list), dir_path: str = ''):
    if isinstance(data, list):
        data = np.array(data)

    path = os.path.join(dir_path, filename)
    np.save(path, data)


def save_net_state_dict(net: Module, cycle_id: str = None, dir_path: str = ''):
    if cycle_id:
        filename = '{}_{}.pt'.format(cycle_id, net.net_id)
    else:
        filename = net.net_id + '.pt'

    print(filename, os.path.join(dir_path, filename))
    path = os.path.join(dir_path, filename)
    torch.save(net.state_dict(), path)


def load_net_state_dict(net: Module, dir_path: str = 'input', cycle_id: str = None):
    if cycle_id:
        filename = '{}_{}.pt'.format(cycle_id, net.net_id)
    else:
        filename = net.net_id + '.pt'

    path = os.path.join(dir_path, filename)
    if os.path.isfile(path):
        net.load_state_dict(torch.load(path))
        net.eval()
