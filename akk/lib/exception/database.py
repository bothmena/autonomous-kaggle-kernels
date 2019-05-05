class DataBaseException(Exception):
    def __init__(self, message, status=None):
        super(DataBaseException, self).__init__(message, status)
        self.message = message
        self.status = status


class ProjectExistsException(DataBaseException):
    def __init__(self, message='A project must have unique path and/or name', status=None):
        super(ProjectExistsException, self).__init__(message, status)
        self.message = message
        self.status = status


class ProjectNotFoundException(DataBaseException):
    def __init__(self, message='The project does not exist in the database', status=None):
        super(ProjectNotFoundException, self).__init__(message, status)
        self.message = message
        self.status = status


class ExperienceExistsException(DataBaseException):
    def __init__(self, message='Same experience for the same project already exists', status=None):
        super(ExperienceExistsException, self).__init__(message, status)
        self.message = message
        self.status = status


class ExperienceNotFoundException(DataBaseException):
    def __init__(self, message='The experience does not exist in the database', status=None):
        super(ExperienceNotFoundException, self).__init__(message, status)
        self.message = message
        self.status = status


class CommitExistsException(DataBaseException):
    def __init__(self, message='Same commit for the same experience already exists', status=None):
        super(CommitExistsException, self).__init__(message, status)
        self.message = message
        self.status = status
