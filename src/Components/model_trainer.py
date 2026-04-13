import os
import sys
from dataclasses import dataclass
from lightgbm import LGBMClassifier
from sklearn.metrics import roc_auc_score, average_precision_score

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def iniciador_modelo_entrenamiento(self, train_array, test_array):
        try:
            logging.info("Dividiendo los datos de entrenamiento y prueba (features y target)")
            
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )
        finally:
            pass