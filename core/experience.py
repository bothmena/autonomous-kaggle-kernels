from abc import ABCMeta, abstractmethod
from torch import nn
from torch import optim


class Experience(metaclass=ABCMeta):
    def __init__(self, batch_size: int, epochs: int, optimizer: str, loss: str, lr: float = None, lr_decay: float = None, lr_cycle: int = None, **kwargs):
        """
        :param batch_size: mini-batch size
        :param epochs: number of training epochs
        :param optimizer: name of the optimizer
        :param loss: name of the loss function, possible values: cross_entropy
        :param lr: initial value of the learning rate
        :param lr_decay: decay value that will affect the slope of the LR decay
        :param lr_cycle: after how many epochs learning rate should restart to the initial value
        :param loss_args: specify args specific to the chosen loss function
        :type loss_args: dict
        :param opt_args: specify args specific to the chosen optimizer
        :type opt_args: dict
        :param kwargs:
        """
        self.batch_size = batch_size
        self.epochs = epochs
        self.optimizer = optimizer
        self.loss = loss
        self.lr = lr
        self.lr_decay = lr_decay
        self.lr_cycle = lr_cycle
        self.opt_args = kwargs['opt_args'] if ('opt_args' in kwargs.keys() and isinstance(kwargs['opt_args'], dict)) else {}
        self.loss_args = kwargs['loss_args'] if ('loss_args' in kwargs.keys() and isinstance(kwargs['loss_args'], dict)) else {}

        self.current_epoch = 0

    @abstractmethod
    def get_optimizer(self, *args):
        """required method"""

    @abstractmethod
    def get_lr(self, *args):
        """
        required method
        in this method you need to implement how the learning rate decreases every step/epoch.
        By default, the learning rate is constant
        :return: float
        """

    @abstractmethod
    def get_loss(self):
        """required method"""


class PyTorchExperience(Experience):

    def __init__(self, *args, **kwargs):
        super(PyTorchExperience, self).__init__(*args, **kwargs)

    def get_lr(self):
        if self.lr_decay is not None and self.lr_decay > 0:
            self.current_epoch += 1
            if isinstance(self.lr_cycle, int) and self.lr_cycle > 0:
                iteration = self.current_epoch % self.lr_cycle
            else:
                iteration = self.current_epoch

            return self.lr / (1 + self.lr_decay * iteration)
        else:
            return self.lr

    def get_optimizer(self, parameters):

        if self.optimizer == 'adam':
            return optim.Adam(parameters, lr=self.get_lr(), **self.opt_args)
        elif self.optimizer == 'rmsprop':
            return optim.RMSprop(parameters, lr=self.get_lr(), **self.opt_args)
        else:
            raise NotImplementedError('This optimizer is not yet implemented')

    def get_loss(self):
        if self.loss == 'mse':
            return nn.MSELoss(**self.loss_args)
        elif self.loss == 'cross_entropy':
            return nn.CrossEntropyLoss(**self.loss_args)
        else:
            raise NotImplementedError('This loss function is not yet implemented')
