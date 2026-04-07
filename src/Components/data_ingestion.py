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


    def iniciador_ingesta(self):

        logging.info('Iniciando el proceso de ingesta de datos')

        try:

            # 1. Lee los dataset crudos
            df = pd.read_csv('data/Fraud_Data.csv')
            df_ip = pd.read_csv('data/IpAddress_to_Country.csv')

            logging.info('Dataset cargados y leídos con exito')
        
            # 2. transforma los datsets
            logging.info('Iniciado el cruce de IP (merge asoft)')

            df_ordenado = df.sort_values(by='ip_address')
            df_ip_ordenado = df_ip.sort_values(by='lower_bound_ip_address')

            df_merged = pd.merge_asof(
                df_ordenado,
                df_ip_ordenado,
                left_on='ip_address',
                right_on='lower_bound_ip_address',
                direction='backward'
            )

            # 3. Imputar países nulos

            df_merged['country'].fillna('Unknown', inplace=True)

            logging.info("Cruce completado y nulos imputados")


            
        except:
            pass


if __name__=='__main__':
    obj = DataIngestion()

