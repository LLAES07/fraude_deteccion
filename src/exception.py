import sys
from src.logger import logging



def mensaje_error_detalles(error: Exception):
    _, _, tb = sys.exc_info()
    
    if tb is not None:
        nombre_archivo = tb.tb_frame.f_code.co_filename
        linea = tb.tb_lineno
    else:
        nombre_archivo = 'Desconocido'
        linea = 'Desconocida'

    mensaje = (
        f"Un error ocurrió en el archivo {nombre_archivo} "
        f"en la línea {linea} con el mensaje: {str(error)}"
    )
    logging.error(mensaje, exc_info=True)
    return mensaje


class CustomException(Exception):
    def __init__(self, error):
        super().__init__(error)
        self.error = mensaje_error_detalles(error)

    def __str__(self):
        return self.error

if __name__ == '__main__':
    
    try:
        b = 1/0
    except Exception as e:
        logging.info(f'Error de division: {e}')
        raise CustomException(e)