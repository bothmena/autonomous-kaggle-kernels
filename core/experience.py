from abc import ABCMeta


class Experience(metaclass=ABCMeta):
    def __init__(self, **hyper_params):
        self.__hp = {}
        for key, value in hyper_params.items():
            self.__hp[key] = value

    def __getattr__(self, item):
        if item in self.__hp.keys():
            return self.__hp.get(item)
        return None

    def lr_decay(self, method=None, epoch=None, *args, **kwargs):
        """
        required method
        in this method you need to implement how the learning rate decreases every step/epoch.
        By default, the learning rate is constant
        :param method: str
        :param epoch: int
        :return: float
        """

        return getattr(self, 'lr')
