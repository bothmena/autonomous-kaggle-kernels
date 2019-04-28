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
