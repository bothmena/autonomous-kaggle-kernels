from src.lib.services.db import MongodbORM
from src.lib.services import Singleton


# todo make sure you need this. after all you only using 2 (or even only one) services: db + config parser
class ServiceContainer(metaclass=Singleton):
    def __init__(self, config_path: str = None, config_fn: str = 'akk.ini'):
        # self._config = configparser.ConfigParser()
        # if config_path is None:
        #     config_path = os.path.join(os.getcwd(), '.akk')
        # if config_fn is None:
        #     config_fn = 'config.ini'
        # file_path = os.path.join(config_path, config_fn)
        # assert os.path.isfile(file_path)
        # self._config.read(file_path)
        # project_id = self.get_parameter('database', 'project_id')
        # experience_id = self.get_parameter('database', 'experience_id')
        self._orm = MongodbORM()

    @property
    def orm(self):
        return self._orm

    # def get_parameter(self, section: str, key: str, p_type: str = 'str'):
    #     if p_type == 'str':
    #         return self._config.get(section, key)
    #     elif p_type == 'bool':
    #         return self._config.getboolean(section, key)
    #     elif p_type == 'int':
    #         return self._config.getint(section, key)
    #     elif p_type == 'float':
    #         return self._config.getfloat(section, key)
