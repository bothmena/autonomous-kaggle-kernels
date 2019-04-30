from abc import ABCMeta, abstractmethod
import torch


class Module(torch.nn.Module, metaclass=ABCMeta):

    n_modules = 0

    def __init__(self, net_id: str = None):
        super(Module, self).__init__()
        if net_id is None:
            self.net_id = 'net_' + str(Module.n_modules)
        else:
            self.net_id = net_id
        Module.n_modules += 1

    @abstractmethod
    def pre_training(self, *args, **kwargs):
        """"""
