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

import json
from .logger import logger

class Cacher():
    """ Class to instance a Cacher
    """
    def __init__(self,file_path:str) -> None:
        self.file_path=file_path
        self.data=self.load_cache()
        
    def load_cache(self) -> dict:
        logger.debug(f'[CACHER]Load cache from {self.file_path}')
        try:
            with open(self.file_path,"r") as file:
                json_data=file.read()
                logger.info(f'[CACHER]Cache is loaded from {self.file_path}')
            return json.loads(json_data)
        except:
            logger.warning(f'[CACHER]Cache can not be loaded from {self.file_path}. Making a new cache')
            return {}
        
    def save_cache(self) -> bool:
        logger.debug(f'[CACHER]Saving cache to {self.file_path}')
        try:
            json_data = json.dumps(self.data, indent=2)
            with open(self.file_path,"w") as file:
                file.write(json_data)
            logger.info(f'[CACHER]Cache is saved to {self.file_path}')
            return True
        except:
            logger.error(f'[CACHER]Error saving cache to {self.file_path}')
            return False
        
    def add(self, type:str, id:str, valor: object) -> None:
        logger.debug(f'[CACHER]Adding a object to cache.')
        if type in self.data:
            self.data[str(type)][str(id)] = valor
        else:
            self.data[str(type)] = {str(id):valor}
        logger.debug(f'[CACHER]Added a object to cache.')
        
    def get(self, type:str, id:str) -> object:
        try:
            logger.debug(f'[CACHER]Getting a object from cache.')
            """item = self.data[str(id)]"""
            item = self.data[type][str(id)]
        except:
            logger.debug(f'[CACHER]Item is not in cache.')
            item = None
        return item
