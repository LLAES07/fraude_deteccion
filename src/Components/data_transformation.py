import os
import sys
import numpy as np
import pandas as pd
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join('artifacts', 'preprocessor.pkl')

class TimeFeaturesExtractor(BaseEstimator, TransformerMixin):
    """
    Transformador para crear features de tiempo a partir de signup_time y purchase_time.
    """
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        try:
            X_copy = X.copy()
            X_copy['signup_time'] = pd.to_datetime(X_copy['signup_time'])
            X_copy['purchase_time'] = pd.to_datetime(X_copy['purchase_time'])
            
            diferencia_dias = (X_copy['purchase_time'] - X_copy['signup_time']) / np.timedelta64(1, 'D')
            X_copy['time_to_purchase_sec'] = diferencia_dias * 86400
            
            X_copy['log_time_to_purchase_sec'] = np.log1p(X_copy['time_to_purchase_sec'].clip(lower=0))
            X_copy['is_ultra_fast'] = (X_copy['time_to_purchase_sec'] <= 3).astype(int)
            
            # Se eliminan las columnas originales y la temporal no logarítmica para limpiar el dataframe
            X_copy.drop(columns=['signup_time', 'purchase_time', 'time_to_purchase_sec'], inplace=True, errors='ignore')
            return X_copy
        except Exception as e:
            raise CustomException(e, sys)



class HistoricalFeaturesExtractor(BaseEstimator, TransformerMixin):
    """
    Transformador para crear features basadas en el histórico (ip, device).
    Aprende solo del conjunto de entrenamiento (fit) para evitar data leakage.
    """
    def __init__(self):
        self.ip_count_map = {}
        self.device_count_map = {}
        self.users_per_ip_map = {}
        self.users_per_device_map = {}

    def fit(self, X, y=None):
        try:
            logging.info("Calculando mapeos históricos desde datos de entrenamiento")
            self.ip_count_map = X.groupby('ip_address').size().to_dict()
            self.device_count_map = X.groupby('device_id').size().to_dict()
            self.users_per_ip_map = X.groupby('ip_address')['user_id'].nunique().to_dict()
            self.users_per_device_map = X.groupby('device_id')['user_id'].nunique().to_dict()
            return self
        except Exception as e:
            raise CustomException(e, sys)

    def transform(self, X):
        try:
            X_copy = X.copy()
            # Mapeamos usando lo aprendido en fit. Si no existe (nuevo en test), rellenamos con 0
            X_copy['ip_count'] = X_copy['ip_address'].map(self.ip_count_map).fillna(0)
            X_copy['device_count'] = X_copy['device_id'].map(self.device_count_map).fillna(0)
            X_copy['users_per_ip'] = X_copy['ip_address'].map(self.users_per_ip_map).fillna(0)
            X_copy['users_per_device'] = X_copy['device_id'].map(self.users_per_device_map).fillna(0)
            
            # Eliminamos las columnas de IDs y país que concluiste que no aportan
            X_copy.drop(columns=['ip_address', 'device_id', 'user_id', 'country'], inplace=True, errors='ignore')
            return X_copy
        except Exception as e:
            raise CustomException(e, sys)
        
        

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        """
        Este método crea el pipeline de preprocesamiento uniendo nuestras 
        transformaciones personalizadas y el ColumnTransformer final.
        """
        try:
            logging.info("Iniciando construcción del Data Transformer Object")
            
            # Definición de las columnas finales según tu notebook
            features_numericas = [
                'purchase_value',
                'age',
                'log_time_to_purchase_sec',
                'ip_count',
                'device_count',
                'users_per_ip',
                'users_per_device'
            ]
            
            features_binarias = ['is_ultra_fast']
            
            features_categoricas = ['source', 'browser', 'sex']

            # 1. Pipeline numérico (Escalado)
            numerical_pipeline = Pipeline(steps=[
                ("scaler", StandardScaler())
            ])

            # 2. Pipeline categórico (One Hot Encoding)
            categorical_pipeline = Pipeline(steps=[
                ("one_hot_encoder", OneHotEncoder(drop='first', handle_unknown='ignore', sparse_output=False))
            ])

            # 3. Column Transformer para aplicar escalado/OHE a las columnas respectivas
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', numerical_pipeline, features_numericas),
                    ('bin', 'passthrough', features_binarias),
                    ('cat', categorical_pipeline, features_categoricas)
                ],
                remainder='drop' # Elimina automáticamente cualquier columna residual
            )

            # 4. PIPELINE COMPLETO
            # Primero crea las features (Feature Engineering) y luego las preprocesa
            full_pipeline = Pipeline(steps=[
                ("time_features", TimeFeaturesExtractor()),
                ("historical_features", HistoricalFeaturesExtractor()),
                ("preprocessor", preprocessor)
            ])

            logging.info("Pipeline de transformación de datos construido exitosamente")
            return full_pipeline

        except Exception as e:
            raise CustomException(e, sys)
