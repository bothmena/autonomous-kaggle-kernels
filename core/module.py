from abc import ABCMeta, abstractmethod
import torch


class Module(torch.nn.Module, metaclass=ABCMeta):

    @abstractmethod
    def pre_training(self, *args, **kwargs):
        """"""
