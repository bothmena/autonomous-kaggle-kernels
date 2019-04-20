from abc import abstractmethod
from lib.services.singleton import ABCSingleton


class IDataBase(metaclass=ABCSingleton):

    @abstractmethod
    def authenticate(self):
        """required method"""

    @abstractmethod
    def get_project(self, project_id):
        """required method"""

    @abstractmethod
    def new_project(self, project_id):
        """required method"""

    @abstractmethod
    def new_experience(self, project_id):
        """required method"""

    @abstractmethod
    def get_experience(self, project_id):
        """required method"""
