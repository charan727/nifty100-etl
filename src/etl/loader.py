import pandas as pd
from src.config import CORE_DATA_PATH


def load_excel(file_name):
    file_path = CORE_DATA_PATH / file_name
    df = pd.read_excel(file_path, header=1)
    return df