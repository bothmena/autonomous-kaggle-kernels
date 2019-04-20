import numpy as np
import torch
from torch import nn


class Saver:
    @classmethod
    def save_numpy(cls, path: str, data: (np.ndarray, list)):
        if isinstance(data, list):
            data = np.array(data)
        np.save(path, data)

    @classmethod
    def save_net_weights(cls, net: nn.Module, path: str):
        torch.save(net.state_dict(), path)
