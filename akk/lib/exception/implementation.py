class ImplementationException(Exception):
    def __init__(self, message, status=None):
        super(ImplementationException, self).__init__(message, status)
        self.message = message
        self.status = status


class NoExperienceException(ImplementationException):
    def __init__(self, message: str = 'You must define an experience in a separate file and import it using a relative import', status=None):
        super(NoExperienceException, self).__init__(message, status)
        self.message = message
        self.status = status


class ManyExperiencesException(ImplementationException):
    def __init__(self, message: str = 'Every project must implement only a single experience.', status=None):
        super(ManyExperiencesException, self).__init__(message, status)
        self.message = message
        self.status = status


class HPNotDefinedException(ImplementationException):
    def __init__(self, message: str = 'A Hyper parameter is not defined in the experience', status=None, hp: str = None, net_id: str = None):
        if hp is not None:
            if net_id is None:
                self.message = 'the {} is not defined in the experience'.format(hp)
            else:
                self.message = 'the {} for network {} is not defined in the experience'.format(hp, net_id)
        else:
            self.message = message
        super(HPNotDefinedException, self).__init__(self.message, status)
        self.status = status
