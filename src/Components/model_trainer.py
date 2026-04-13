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
