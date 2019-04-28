class GitException(Exception):
    def __init__(self, message, status=None):
        super(GitException, self).__init__(message, status)
        self.message = message
        self.status = status


class NoRepoException(GitException):
    def __init__(self, message: str = 'AKK uses git internally to keep track of project changes, please initialize you repository first.', status=None):
        super(NoRepoException, self).__init__(message, status)
        self.message = message
        self.status = status


class UncommitedChangesException(GitException):
    def __init__(self, message: str = 'Before assemble your code, please make sure to commit the changes you made.', status=None):
        super(UncommitedChangesException, self).__init__(message, status)
        self.message = message
        self.status = status
