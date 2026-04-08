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
