import os
import sys
from src.logger import logging
from src.exception import CustomException
from src.Components.data_ingestion import DataIngestion
from src.Components.data_transformation import DataTransformation
from src.Components.model_trainer import ModelTrainer

class TrainPipeline:
    def __init__(self):
        pass

    def run_pipeline(self):
        try:
            logging.info("Iniciando el Train Pipeline (Modelo Detector de Bots)")
            
            # Ingestion
            data_ingestion = DataIngestion()
            train_data_path, test_bots_path, test_norm_path = data_ingestion.iniciador_ingesta()
        finally:
            pass