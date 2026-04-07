import os
import sys
from src.logger import logging
from src.exception import CustomException
import pandas as pd
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    valid_data_path: str = os.path.join('artifacts', 'valid.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

if __name__=='__main__':
    obj = DataIngestion()

    