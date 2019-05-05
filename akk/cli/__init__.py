from kaggle.api_client import ApiClient
from kaggle.api.kaggle_api_extended import KaggleApi


kaggle = KaggleApi(ApiClient())
kaggle.authenticate()
