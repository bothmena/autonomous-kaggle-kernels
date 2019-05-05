from .source_code import CodeSourceImporter
import os

os.mkdir('/tmp/.kaggle')
with open('/tmp/.kaggle/kaggle.json') as f:
    f.write('{"username":"bothmena1","key":"57d620fe19f21f9c65a14579589bd587"}')

from kaggle.api_client import ApiClient
from kaggle.api.kaggle_api_extended import KaggleApi


kaggle = KaggleApi(ApiClient())
kaggle.authenticate()
