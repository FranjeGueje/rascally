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
import json
from typing import Tuple

from . import LauncherEngine
from . import BasicGame
from util import logger


class EngineEpic(LauncherEngine):

    def __init__(self):
        super().__init__('Epic')
        
        #! Añandimos los directorios, ficheros, y enlaces EXTRAS
        self.empty_dir_list = self.empty_dir_list + \
            ('pfx/drive_c/users/steamuser/AppData/Local/EpicGamesLauncher/Intermediate/Config/CoalescedSourceConfigs',)
            
        self.copy_list = self.copy_list + \
            ('pfx/drive_c/ProgramData/Epic',
             'pfx/drive_c/users/steamuser/AppData/Local/Epic Games',
             'pfx/drive_c/users/steamuser/AppData/Local/EpicGamesLauncher/Intermediate/Config/CoalescedSourceConfigs/PortalRegions.ini'
             )
        
        self.symlink_list = self.symlink_list + \
            ('pfx/drive_c/users/steamuser/AppData/Local/EpicGamesLauncher/Saved',)

    def search_games(self, search_path=os.environ.get("HOME") + "/.local/share/Steam", excep={}) -> Tuple[BasicGame]:

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
            path_exe = os.path.join(
                path, carpeta + "/pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Engine/Binaries/Win64/EpicGamesLauncher.exe")
            path_exclude = os.path.join(path, carpeta + "/rascal_exclude")
            if os.path.isfile(path_exe) and not os.path.isfile(path_exclude):
                logger.info(
                    f'[EngineEpic]Found this prefix {path}/{carpeta} with Epic Games Launcher installed')
                path_json = os.path.join(
                    path, carpeta + "/pfx/drive_c/ProgramData/Epic/UnrealEngineLauncher/LauncherInstalled.dat")
                if os.path.isfile(path_json):
                    # Abrir el archivo JSON en modo lectura
                    with open(path_json, 'r') as archivo:
                        # Cargar el contenido del archivo en una variable Python
                        data = json.load(archivo)

                    for jueguecito in data['InstallationList']:
                        title = os.path.basename(jueguecito['InstallLocation'])
                        exe = jueguecito['AppName']
                        exe_completed = f'"com.epicgames.launcher://apps/{exe}?action=launch&silent=true"'
                        logger.info(
                            f'[EngineEpic]Found the game {title} with Exe {exe_completed}')
                        g = BasicGame(
                            AppName=title,
                            Exe=exe_completed,
                            CompatData=f'{path}{carpeta}'
                        )
                        juegos.append(g)

        logger.info(f'[EngineEpic]Found {len(juegos)} games')
        return tuple(juegos)
