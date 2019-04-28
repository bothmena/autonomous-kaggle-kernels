class DataBaseException(Exception):
    def __init__(self, message, status=None):
        super(DataBaseException, self).__init__(message, status)
        self.message = message
        self.status = status


class ProjectExistsException(DataBaseException):
    def __init__(self, message, status=None):
        super(ProjectExistsException, self).__init__(message, status)
        self.message = message
        self.status = status


class ExperienceExistsException(DataBaseException):
    def __init__(self, message, status=None):
        super(ExperienceExistsException, self).__init__(message, status)
        self.message = message
        self.status = status
