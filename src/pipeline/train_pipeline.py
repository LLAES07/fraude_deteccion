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
            
            # Transformacion
            data_transformation = DataTransformation()
            train_arr, test_bots_arr, test_norm_arr, preprocessor_path = data_transformation.initiate_data_transformation(
                train_path=train_data_path,
                test_bots_path=test_bots_path,
                test_norm_path=test_norm_path
            )
            
            # Entrenamiento
            model_trainer = ModelTrainer()
            metrics = model_trainer.iniciador_modelo_entrenamiento(
                train_array=train_arr,
                test_bots_array=test_bots_arr,
                test_norm_array=test_norm_arr
            )
            
            logging.info(f"Pipeline completado. Métricas: {metrics}")
            print(f"Métricas Finales: {metrics}")
            return metrics
            
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    pipeline = TrainPipeline()
    pipeline.run_pipeline()