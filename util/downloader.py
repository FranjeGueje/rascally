import requests
import os
from urllib.parse import urlparse

from . import logger

def download(url:str, dest: str, override=False) -> None:
    # Si es un directorio, el destino será el mismo nombre que el fichero de la url
    if os.path.isdir(dest):
        dest+=os.path.basename(urlparse(url).path)
    if os.path.isfile(dest) and not override:
        logger.debug(f'The file {dest} exists.')
    else:
        logger.debug(f'The file {dest} does not exist.')
        # Realizar la solicitud GET para obtener el contenido del archivo
        respuesta = requests.get(url)

        # Verificar si la solicitud fue exitosa (código de estado 200)
        if respuesta.status_code == 200:    
        # Abrir el archivo en modo binario y escribir el contenido descargado
            with open(dest, 'wb') as archivo:
                archivo.write(respuesta.content)
            logger.info(f'The file has been downloaded como {dest} from {url}')
        else:
            logger.error(f"It's not possible download from {url}. Code: {respuesta.status_code}")
