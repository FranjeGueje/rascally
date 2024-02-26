# 
# Copyright (C) 2024 Paco Guerrero <fjgj1@hotmail.com>
# 
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
#############################################################################################
# Rascally
# https://github.com/FranjeGueje/rascally
#############################################################################################

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
