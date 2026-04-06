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