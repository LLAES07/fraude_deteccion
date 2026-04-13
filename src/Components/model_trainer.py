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

    def iniciador_modelo_entrenamiento(self, train_array, test_bots_array, test_norm_array):
        try:
            logging.info("Dividiendo los datos de entrenamiento y prueba (features y target)")
            
            X_train, y_train = train_array[:, :-1], train_array[:, -1]
            X_bots, y_bots = test_bots_array[:, :-1], test_bots_array[:, -1]
            X_norm, y_norm = test_norm_array[:, :-1], test_norm_array[:, -1]

            # Calcular scale_pos_weight para lidiar con el desbalance de clases
            negativos = len(y_train[y_train == 0])
            positivos = len(y_train[y_train == 1])
            scale = negativos / positivos if positivos > 0 else 1.0

            logging.info(f"Configurando el modelo LGBMClassifier con scale_pos_weight: {scale:.2f}")
            
            # Modelo 3: Detector de Bots, según lo concluido en el notebook
            model = LGBMClassifier(
                scale_pos_weight=scale,
                n_estimators=500,
                learning_rate=0.05,
                num_leaves=31,
                random_state=42,
                n_jobs=-1
            )

            logging.info("Entrenando el modelo LGBMClassifier...")
            model.fit(X_train, y_train)

            logging.info("Guardando el modelo entrenado en la carpeta artifacts...")
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=model
            )

            logging.info("Evaluando el modelo en el conjunto de prueba BOTS (Enero Holdout)...")
            y_prob_bots = model.predict_proba(X_bots)[:, 1]

            roc_auc_bots = roc_auc_score(y_bots, y_prob_bots)
            pr_auc_bots = average_precision_score(y_bots, y_prob_bots)

            logging.info(f"Rendimiento en Test BOTS - AUC-ROC: {roc_auc_bots:.4f}")
            logging.info(f"Rendimiento en Test BOTS - AUC-PR: {pr_auc_bots:.4f}")
            
            logging.info("Evaluando el modelo en el conjunto de prueba NORMAL (Resto de meses)...")
            y_prob_norm = model.predict_proba(X_norm)[:, 1]

            roc_auc_norm = roc_auc_score(y_norm, y_prob_norm)
            pr_auc_norm = average_precision_score(y_norm, y_prob_norm)

            logging.info(f"Rendimiento en Test NORMAL - AUC-ROC: {roc_auc_norm:.4f}")
            logging.info(f"Rendimiento en Test NORMAL - AUC-PR: {pr_auc_norm:.4f}")

            return {
                "bots_roc_auc": roc_auc_bots,
                "bots_pr_auc": pr_auc_bots,
                "norm_roc_auc": roc_auc_norm,
                "norm_pr_auc": pr_auc_norm
            }

        except Exception as e:
            raise CustomException(e, sys)
