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

import os
from typing import Tuple
import shutil

from . import LauncherEngine
from . import BasicGame
from util import logger

class EngineLink(LauncherEngine):
    
    def __init__(self):
        super().__init__('Link')
        
        #! Añandimos los directorios, ficheros, y enlaces EXTRAS
        self.empty_dir_list = self.empty_dir_list + \
            ('pfx/drive_c/users/steamuser/AppData/Local/EpicGamesLauncher/Intermediate/Config/CoalescedSourceConfigs',)
            
        self.copy_list = self.copy_list + \
            ('pfx/drive_c/users/steamuser/AppData/Local/Origin',
             'pfx/drive_c/users/steamuser/AppData/Local/EADesktop',
             'pfx/drive_c/users/steamuser/AppData/Local/Electronic Arts',
             'pfx/drive_c/ProgramData/EA Desktop',
             'pfx/drive_c/ProgramData/Electronic Arts'
            )
        
    
    def search_games(self, search_path=os.environ.get("HOME") + "/.local/share/Steam", excep={})-> Tuple[BasicGame]:
    
        # Establecemos la ruta donde están los compatdata
        path = search_path + "/steamapps/compatdata/"
        
        # Obtener la lista de carpetas en la ruta
        carpetas = [nombre for nombre in os.listdir(
            path) if os.path.isdir(os.path.join(path, nombre))]
        
        # A las carpetas le quitamos las excepciones
        carpetas = [item for item in carpetas if item not in excep]
        
        juegos = []

        # Iterar sobre cada carpeta y realizar la acción deseada
        for carpeta in carpetas:
            path_exclude = os.path.join(path, carpeta + "/rascal_exclude")
            if os.path.isfile(path_exclude):
                continue
            
            path_lnk = os.path.join(
                path, carpeta + "/pfx/drive_c/users/steamuser/Desktop/")
            if os.path.isdir(path_lnk):
                for file in os.listdir(path_lnk):
                    if file.endswith(".lnk"):
                        filename = os.path.splitext(file)[0]
                        exe_completed = f'{path_lnk}{file}'
                        logger.info(f'[EngineLink]Found this link in {exe_completed}')
                        g = BasicGame(
                            AppName=filename,
                            Exe=exe_completed,
                            CompatData=f'{path}{carpeta}'
                        )
                        juegos.append(g)

            path_lnk = os.path.join(
                path, carpeta + "/pfx/drive_c/users/Public/Desktop/")
            if os.path.isdir(path_lnk):
                for file in os.listdir(path_lnk):
                    if file.endswith(".lnk"):
                        filename = os.path.splitext(file)[0]
                        exe_completed = f'{path_lnk}{file}'
                        logger.info(f'[EngineLink]Found this link in {exe_completed}')
                        g = BasicGame(
                            AppName=filename,
                            Exe=exe_completed,
                            CompatData=f'{path}{carpeta}'
                        )
                        juegos.append(g)
        logger.info(f'[EngineLink]Found {len(juegos)} games')
        return tuple(juegos)
    
    # Método para crear link
    def create_link(self, game:BasicGame, destination:str) -> str:
        logger.debug(f'[EngineLink]Entering in create_link.')
        if os.path.isdir(destination):
            try:
                logger.debug(f'[EngineLink]Coping the link from {game.Exe} to {destination}/{game.AppName}.lnk')
                returned = shutil.copy2(
                    src=f'{game.Exe}',
                    dst=f'{destination}/{game.AppName}.lnk',
                    follow_symlinks=True
                )
                logger.info(f'[EngineLink]Link created (copied) correctly in {destination}/{game.AppName}.lnk')
                return returned
            except:
                logger.warning(f'[EngineLink]Link not created (copied) correctly in {destination}/{game.AppName}.lnk')
                return None
        return None
