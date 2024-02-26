import logging
from logging.handlers import RotatingFileHandler

CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET

def setup_logger(level=logging.INFO):
    # Configurar el logger
    logger = logging.getLogger('Rascal_logger')
    logger.setLevel(level)

    # Configurar el manejador de archivos rotativo
    log_file = 'rascal.log'
    max_size_bytes = 10485760  # Tamaño máximo del archivo en bytes
    backup_count = 3      # Número máximo de archivos de respaldo
    file_handler = RotatingFileHandler(log_file, maxBytes=max_size_bytes, backupCount=backup_count)

    # Configurar el formato del log
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Agregar el manejador al logger
    logger.addHandler(file_handler)
    
    # Devolvemos el logger creado
    return logger

# Configurar el logger al importar el módulo
logger = setup_logger()
