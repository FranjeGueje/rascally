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

import subprocess
import os
from util.mslink import create_lnk
from util import logger

CLONE_SYMLINK = 10
CLONE_BALANCED = 20
CLONE_FULL = 30


class BasicGame():
    """ Class to instance a Game
    """

    def __init__(
        self,
        AppName: str,
        Exe: str,
        CompatData: str
    ) -> None:

        self.AppName = AppName
        self.Exe = Exe
        self.CompatData = CompatData[:-
                                     1] if CompatData.endswith("/") else CompatData

    def __eq__(self, game: 'BasicGame'):
        if isinstance(game, BasicGame):
            return self.AppName == game.AppName and self.Exe == game.Exe and self.CompatData == game.CompatData
        return False
    
    def __ne__(self, game: 'BasicGame'):
        if isinstance(game, BasicGame):
            return not self == game
        return False
    
    def create_link(self,destination: str) -> str:
        logger.debug(f'[BasicGame]Creating the link in {destination}')
        if os.path.isdir(destination):
            logger.debug(f'[BasicGame]Launching mslink -l {self.Exe} -o "{destination}/{self.AppName}.lnk"')
            create_lnk('-l', f'{self.Exe}', '-o', f'"{destination}/{self.AppName}.lnk"')
            logger.debug(f'[BasicGame]mslink should be created in "{destination}/{self.AppName}.lnk"')
            return os.path.abspath(f'{destination}/{self.AppName}.lnk')
        logger.debug(f'[BasicGame]The {destination} is not directory or not exits')
        return None
    
    def get_id(self) -> str:
        return f'f{self.CompatData}_{self.AppName}'
    

def _run_bash_command(command: str):
    # Ejecutar el comando bash y capturar la salida
    try:
        return subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        return e
    
