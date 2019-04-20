from lib.services.db import MongoDB
from lib.services.singleton import Singleton
from bson.objectid import ObjectId
import configparser
import os


class ServiceContainer(metaclass=Singleton):
    def __init__(self, config_path: str = None, config_fn: str = 'akk.ini'):
        self._config = configparser.ConfigParser()
        if config_path is None:
            config_path = os.path.join(os.getcwd(), '.akk')
        if config_fn is None:
            config_fn = 'config.ini'
        file_path = os.path.join(config_path, config_fn)
        assert os.path.isfile(file_path)
        self._config.read(file_path)
        project_id = self.get_parameter('database', 'project_id')
        experience_id = self.get_parameter('database', 'experience_id')
        self._database = MongoDB(ObjectId(project_id), ObjectId(experience_id))

    @property
    def database(self):
        return self._database

    def get_parameter(self, section: str, key: str, p_type: str = 'str'):
        if p_type == 'str':
            return self._config.get(section, key)
        elif p_type == 'bool':
            return self._config.getboolean(section, key)
        elif p_type == 'int':
            return self._config.getint(section, key)
        elif p_type == 'float':
            return self._config.getfloat(section, key)
