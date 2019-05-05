from .source_code import CodeSourceImporter
from kaggle.api_client import ApiClient


try:
    from kaggle.api.kaggle_api_extended import KaggleApi

    kaggle = KaggleApi(ApiClient())
    kaggle.authenticate()
except OSError:
    print('Could not find kaggle.json.')
