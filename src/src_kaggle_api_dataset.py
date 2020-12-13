from kaggle.api.kaggle_api_extended import KaggleApi
from zipfile import ZipFile
import pandas as pd

def get_kaggle_dataset(dataset, d_file, used_dtypes, usecols):
    '''
    Pass Kaggle dataset URL (user/dataset) and dataset file
    Returns Pandas DataFrame for dataset
    '''
    # setup API connection
    api = KaggleApi()
    api.authenticate()

    # download file
    api.dataset_download_file(dataset, d_file)
    zf = ZipFile(d_file+'.zip')

    #extracted data is saved in the same directory as notebook
    zf.extractall() 
    zf.close()

    return pd.read_csv(d_file, dtype=used_dtypes, usecols=usecols)