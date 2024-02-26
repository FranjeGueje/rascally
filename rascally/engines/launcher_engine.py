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

from abc import ABC, abstractmethod
import os
from typing import Tuple
from util.mslink import create_lnk
from util import logger

from .engine_core import BasicGame, CLONE_SYMLINK, CLONE_BALANCED, CLONE_FULL, _run_bash_command
        
class LauncherEngine(ABC):
    
    def __init__(self, name:str):
        self.name = name
        self.empty_dir_list = (
            'pfx',
            'pfx/drive_c',
            'pfx/drive_c/ProgramData',
            'pfx/drive_c/users/steamuser/AppData/Local'
        )
        self.blank_files_list = (
            'tracked_files',
            'rascal_exclude'
        )
        self.copy_list = (
            'pfx/system.reg',
            'pfx/user.reg',
            'pfx/userdef.reg',
            'pfx/dosdevices'
        )
        self.symlink_list = (
            'pfx/drive_c/Program Files',
            'pfx/drive_c/Program Files (x86)',
            'pfx/drive_c/ProgramData/Package Cache'
        )
        self.copy_no_symlink_list = (
            'pfx/drive_c/windows',
        )
        

    # * Método abstracto que todo ENGINE tiene que implementar
    @abstractmethod
    def search_games(self, search_path=str,excep={}) -> Tuple[BasicGame]:
        pass
    
    # Método para crear link
    def create_link(self, game:BasicGame, destination:str) -> str:
        logger.debug(f'[LauncherEngine]Creating the link in {destination}')
        if os.path.isdir(destination):
            return game.create_link(destination=destination)
        logger.debug(f'[LauncherEngine]The {destination} is not directory or not exits')
        return None
    
    # Método de clonado
    def clone_compatdata(self, game:BasicGame, destination:str, mode=CLONE_BALANCED) -> bool:
        logger.debug(f'[LauncherEngine]Clonning the game {game.AppName} in {destination}')
        if mode == CLONE_SYMLINK:
            logger.debug(f'[LauncherEngine.clone_compatdata]Using CLONE_SYMLINK mode')
            try:
                # Verificar si la carpeta de destino existe, si no, crearla
                if not os.path.exists(destination):
                    os.makedirs(destination)

                # Recorrer todos los elementos de la carpeta de origen
                for elemento in os.listdir(game.CompatData):
                    ruta_elemento_origen = os.path.join(game.CompatData, elemento)
                    ruta_elemento_destino = os.path.join(destination, elemento)
                    
                    # Crear enlace simbólico en la carpeta de destino
                    logger.debug(f'[LauncherEngine.CLONE_SYMLINK]Clonning from {ruta_elemento_origen} to {ruta_elemento_destino}')
                    os.symlink(ruta_elemento_origen, ruta_elemento_destino)
                with open(f'{destination}/rascal_exclude', 'w'):
                    pass
            except:
                logger.critical(f'[LauncherEngine.CLONE_SYMLINK]NOT clonning. With errors.')
                return False
            logger.info(f'[LauncherEngine.clone_compatdata]Game "{game.AppName}" clonned in {destination}')
            return True
        
        elif mode == CLONE_FULL:
            logger.debug(f'[LauncherEngine.clone_compatdata]Using CLONE_FULL mode')
            try:
                result = _run_bash_command(command=f'cp -Rf "{game.CompatData}" "{destination}"')
                with open(f'{destination}/rascal_exclude', 'w'):
                    pass
            except:
                logger.critical(f'[LauncherEngine.CLONE_FULL]NOT clonning. With errors.')
                return False
            logger.info(f'[LauncherEngine.clone_compatdata]Game "{game.AppName}" clonned in {destination}')
            return True
        
        elif mode == CLONE_BALANCED:
            logger.debug(f'[LauncherEngine.clone_compatdata]Using CLONE_BALANCED mode')
            try:
                result = self.__run_empty_dir_list(destination=destination)
                result = result and self.__run_blank_files_list(destination=destination)
                result = result and self.__run_copy_list(source=f'{game.CompatData}',destination=destination)
                result = result and self.__run_symlink_list(source=f'{game.CompatData}',destination=destination)
                result = result and self.__run_copy_no_symlink_list(source=f'{game.CompatData}',destination=destination)
            except:
                logger.critical(f'[LauncherEngine.CLONE_BALANCED]NOT clonning. With errors.')
                return False
            if result:
                logger.info(f'[LauncherEngine.clone_compatdata]Game "{game.AppName}" clonned in {destination}')
            else:
                logger.warning(f'[LauncherEngine.clone_compatdata]Game "{game.AppName}" NOT clonned in {destination}')
            return result
        logger.critical(f'[LauncherEngine.clone_compatdata]Mode "{mode}" incorrect.')
        return False

    ########################################
    ####      Métodos de apoyo
    ########################################

    def __run_empty_dir_list(self, destination: str) -> bool:
        for dir in self.empty_dir_list:
            logger.debug(f'[LauncherEngine.CLONE_BALANCED]Creation dir empty "{destination}/{dir}"')
            try:
                result = _run_bash_command(command=f'mkdir -p \"{destination}/{dir}\"')
                logger.debug(f'[LauncherEngine.CLONE_BALANCED]STDOUT:\n{result.stdout}')
                logger.debug(f'[LauncherEngine.CLONE_BALANCED]STDERR:\n{result.stderr}')
            except:
                return False
        return True
    
    
    def __run_blank_files_list(self, destination: str) -> bool:
        for file in self.blank_files_list:
            logger.debug(f'[LauncherEngine.CLONE_BALANCED]Creation blank file "{destination}/{file}"')
            try:
                with open(f'{destination}/{file}', 'w'):
                    pass
            except:
                return False
        return True
    
    def __run_copy_list(self, source: str, destination: str) -> None:
        for file in self.copy_list:
            if not os.path.exists(f'{source}/{file}'):
                logger.warning(f'[LauncherEngine.CLONE_BALANCED]Copying {source}/{file} - NOT Exists.')
                continue
            logger.debug(f'[LauncherEngine.CLONE_BALANCED]Copy item: {source}/{file}')
            try:
                result = _run_bash_command(command=f'cp -Rf \"{source}/{file}\" \"{destination}/{file}\"')
                logger.debug(f'[LauncherEngine.CLONE_BALANCED]STDOUT:\n{result.stdout}')
                logger.debug(f'[LauncherEngine.CLONE_BALANCED]STDERR:\n{result.stderr}')
            except:
                return False
        return True
    
    def __run_symlink_list(self, source: str, destination: str) -> None:
        for symlink in self.symlink_list:
            if not os.path.exists(f'{source}/{symlink}'):
                logger.warning(f'[LauncherEngine.CLONE_BALANCED]Symlink {source}/{symlink} - NOT Exists.')
                continue
            logger.debug(f'[LauncherEngine.CLONE_BALANCED]Creation symbolic link from {source}/{symlink}')
            try:
                result = _run_bash_command(command=f'ln -s \"{source}/{symlink}\" \"{destination}/{symlink}\"')
                logger.debug(f'[LauncherEngine.CLONE_BALANCED]STDOUT:\n{result.stdout}')
                logger.debug(f'[LauncherEngine.CLONE_BALANCED]STDERR:\n{result.stderr}')
            except:
                return False
        return True
    
    def __run_copy_no_symlink_list(self, source: str, destination: str) -> None:
        for item in self.copy_no_symlink_list:
            if not os.path.exists(f'{source}/{item}'):
                logger.warning(f'[LauncherEngine.CLONE_BALANCED]Copy/Symlink {source}/{item} - NOT Exists.')
                continue
            try:
                logger.debug(f'[LauncherEngine.CLONE_BALANCED]Copying item: {source}/{item}')
                result = _run_bash_command(command=f'rsync -av --no-links \"{source}/{item}\" \"{destination}\"')
                logger.debug(f'[LauncherEngine.CLONE_BALANCED]STDOUT:\n{result.stdout}')
                logger.debug(f'[LauncherEngine.CLONE_BALANCED]STDERR:\n{result.stderr}')
            except:
                return False
        return True