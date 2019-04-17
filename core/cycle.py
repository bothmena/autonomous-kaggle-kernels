from abc import ABCMeta, abstractmethod
import torch
from torch.nn import Module
import os
import configparser


class Cycle(metaclass=ABCMeta):

    def __init__(self, net: Module, basename='net', config_path=None, config_fn=None):
        self.net = net
        self.config = configparser.ConfigParser()
        if config_path is None:
            config_path = os.getcwd()
        if config_fn is None:
            config_fn = 'akk.ini'
        self.config.read(os.path.join(config_path, config_fn))
        self.basename = basename
        self.cycle = self.config.getint('cycle', 'current')
        self.cycles = self.config.getint('cycle', 'total')
        self.w_path = self.config.get('paths', 'weights_dir')

    def load_weights(self):
        file_path = os.path.join(self.w_path, '{}_{}_{}'.format(self.basename, self.cycle, self.cycles))
        if os.path.isfile(file_path):
            state_dict = torch.load(file_path)
            self.net.load_state_dict(state_dict)

    def pre_training(self):
        if torch.cuda.is_available():
            self.net.cuda()

    def save_weights(self):
        pass

    @abstractmethod
    def loop(self):
        """
        required method.
        This is where you implement the for loop in range(self.cycles)
        """

    def __call__(self, *args, **kwargs):
        self.loop()
