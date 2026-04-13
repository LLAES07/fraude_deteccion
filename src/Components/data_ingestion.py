import os
import sys
from src.logger import logging
from src.exception import CustomException
import pandas as pd
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    valid_data_path: str = os.path.join('artifacts', 'test_bots.csv')
    test_data_path: str = os.path.join('artifacts', 'test_norm.csv')
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

            # 4. Conversión fechas al formato correcto 
            df_merged['purchase_time'] = pd.to_datetime(df_merged['purchase_time'], format='%Y-%m-%d %H:%M:%S')
            df_merged['signup_time'] = pd.to_datetime(df_merged['signup_time'], format='%Y-%m-%d %H:%M:%S')

            df_merged = df_merged.sort_values('purchase_time').reset_index(drop=True)
            
            # Asegurarse que la carpeta artifacts existe
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            
            # Guardar la raw data combinada
            df_merged.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            # 5. Split Modelo 3: Detector de Bots
            logging.info("Iniciando el split específico para el Detector de Bots")
            
            from sklearn.model_selection import train_test_split
            
            df_enero = df_merged[df_merged['purchase_time'].dt.month == 1]
            enero_train, enero_holdout = train_test_split(
                df_enero, test_size=0.20, random_state=42, stratify=df_enero['class']
            )

            df_resto = df_merged[df_merged['purchase_time'].dt.month != 1]
            n_resto = len(df_resto)
            resto_train = df_resto.iloc[:int(n_resto * 0.70)]
            resto_test = df_resto.iloc[int(n_resto * 0.70):]

            # Train total = 80% enero + Feb–Ago (ordenado cronológicamente)
            train_total = pd.concat([enero_train, resto_train]).sort_values('purchase_time')

            # 6. Guardado de los splits en artifacts
            train_total.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            enero_holdout.to_csv(self.ingestion_config.valid_data_path, index=False, header=True)
            resto_test.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Data Ingestion completada con éxito")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.valid_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)




if __name__=='__main__':
    obj = DataIngestion()
    train_data, valid_data, test_data = obj.iniciador_ingesta()

