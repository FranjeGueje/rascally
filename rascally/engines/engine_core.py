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
    return subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
