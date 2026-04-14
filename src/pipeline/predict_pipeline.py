import sys
import pandas as pd
from src.exception import CustomException
from src.utils import load_object
import os

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            model_path = os.path.join("artifacts", "model.pkl")
            preprocessor_path = os.path.join("artifacts", "preprocessor.pkl")
            
            # Carga del modelo y el preprocesador
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            
            # Transformación de los datos
            data_scaled = preprocessor.transform(features)
            
            # Predicción
            preds = model.predict(data_scaled)
            preds_proba = model.predict_proba(data_scaled)[:, 1]
            
            return preds, preds_proba
            
        except Exception as e:
            raise CustomException(e, sys)

class CustomData:
    """
    Clase para mapear los inputs y convertirlos en un DataFrame
    con los nombres de columnas que espera el preprocesador.
    """
    def __init__(self,
                 user_id: int,
                 signup_time: str,
                 purchase_time: str,
                 purchase_value: float,
                 device_id: str,
                 source: str,
                 browser: str,
                 sex: str,
                 age: int,
                 ip_address: float,
                 country: str = "Unknown"):
        self.user_id = user_id
        self.signup_time = signup_time
        self.purchase_time = purchase_time
        self.purchase_value = purchase_value
        self.device_id = device_id
        self.source = source
        self.browser = browser
        self.sex = sex
        self.age = age
        self.ip_address = ip_address
        self.country = country

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "user_id": [self.user_id],
                "signup_time": [self.signup_time],
                "purchase_time": [self.purchase_time],
                "purchase_value": [self.purchase_value],
                "device_id": [self.device_id],
                "source": [self.source],
                "browser": [self.browser],
                "sex": [self.sex],
                "age": [self.age],
                "ip_address": [self.ip_address],
                "country": [self.country]
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
