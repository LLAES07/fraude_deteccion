import logging
import os
from datetime import datetime

# Nombre archivo log
LOG_NAME = f'{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.log'

# Ruta del directorio

lod_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(lod_dir, exist_ok=True)

# Jerarquía por día
current_day_dir = os.path.join(lod_dir, f'{datetime.now().strftime("%d_%m_%Y")}')
os.makedirs(current_day_dir, exist_ok=True)

# Ruta del archivo log
LOG_FILE_PATH = os.path.join(current_day_dir, LOG_NAME)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode='w',
    format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    logging.info('logging comienza')
    
