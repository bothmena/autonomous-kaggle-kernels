from abc import ABCMeta, abstractmethod
from torch import nn
from torch import optim
from lib.exception.implementation import HPNotDefinedException


class Experience(metaclass=ABCMeta):
    def __init__(self, batch_size: int, networks: dict, cycles: dict, lr: float = None, lr_decay: float = None, lr_cycle: int = None, optimizer: str = None, opt_args: dict = None,
                 loss: str = None, loss_args: dict = None, steps: int = None, **kwargs):
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
        self.networks = networks
        self.cycles = cycles

        self._lr = lr
        self._lr_decay = lr_decay
        self._lr_cycle = lr_cycle

        self._optimizer = optimizer
        if opt_args is None:
            self._opt_args = {}
        else:
            self._opt_args = opt_args

        self._loss = loss
        if loss_args is None:
            self._loss_args = {}
        else:
            self._loss_args = loss_args

        self._steps = steps
        self.custom_hps = kwargs

        self.current_epoch = 0

    @abstractmethod
    def get_optimizer(self, net_id: str, *args):
        """required method"""

    def get_hp(self, name: str):
        try:
            return self.custom_hps[name]
        except KeyError:
            raise KeyError(name + ' is not defined in this experience')

    def lr(self, net_id: str):
        v = self.networks[net_id].get('lr', self._lr)
        if v is None:
            raise HPNotDefinedException(hp='learning rate')
        return v

    def optimizer(self, net_id: str):
        v = self.networks[net_id].get('optimizer', self._optimizer)
        if v is None:
            raise HPNotDefinedException(hp='optimizer')
        return v

    def loss(self, net_id: str):
        v = self.networks[net_id].get('loss', self._loss)
        if v is None:
            raise HPNotDefinedException(hp='loss')
        return v

    def steps(self, cycle_id: str):
        v = self.cycles[cycle_id].get('steps', self._steps)
        if v is None:
            raise HPNotDefinedException(message='the steps for cycle {} are not defined in the experience')
        return v

    def lr_decay(self, net_id: str):
        return self.networks[net_id].get('lr_decay', self._lr_decay)

    def lr_cycle(self, net_id: str):
        return self.networks[net_id].get('lr_cycle', self._lr_cycle)

    def opt_args(self, net_id: str):
        return self.networks[net_id].get('opt_args', self._opt_args)

    def loss_args(self, net_id: str):
        return self.networks[net_id].get('loss_args', self._loss_args)

    def get_lr(self, net_id: str = 'net_0'):
        """
        in this method you need to implement how the learning rate decreases every step/epoch.
        By default, the learning rate is constant
        :return: float
        """
        lr = self.lr(net_id)
        lr_decay = self.lr_decay(net_id)
        lr_cycle = self.lr_cycle(net_id)

        if lr_decay is not None and lr_decay > 0:
            self.current_epoch += 1
            if isinstance(lr_cycle, int) and lr_cycle > 0:
                iteration = self.current_epoch % lr_cycle
            else:
                iteration = self.current_epoch

            return lr / (1 + lr_decay * iteration)
        else:
            return lr

    @abstractmethod
    def get_loss(self, net_id: str):
        """required method"""

    @abstractmethod
    def get_steps(self, cycle_id: int):
        """required method"""


class PyTorchExperience(Experience):

    def __init__(self, *args, **kwargs):
        super(PyTorchExperience, self).__init__(*args, **kwargs)

    def get_optimizer(self, parameters, net_id: str = 'net_0'):
        opt = self.optimizer(net_id)
        if opt == 'adam':
            return optim.Adam(parameters, lr=self.get_lr(net_id), **self.opt_args(net_id))
        elif opt == 'rmsprop':
            return optim.RMSprop(parameters, lr=self.get_lr(net_id), **self.opt_args(net_id))
        else:
            raise NotImplementedError('This optimizer is not yet implemented')

    def get_loss(self, net_id: str = 'net_0'):
        loss = self.loss(net_id)
        if loss == 'mse':
            return nn.MSELoss(**self.loss_args(net_id))
        elif loss == 'cross_entropy':
            return nn.CrossEntropyLoss(**self.loss_args(net_id))
        elif loss == 'custom':
            return None
        else:
            raise NotImplementedError('This loss function is not yet implemented')

    def get_steps(self, cycle_id: str):
        return self.steps(cycle_id)
