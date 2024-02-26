import os
import json
from typing import Iterable 
from .engines import CLONE_BALANCED, CLONE_FULL, CLONE_SYMLINK

from util import logger,CRITICAL,WARNING,ERROR,INFO,DEBUG


class RascallyConfig():
    """ Class to instance a RascallyConfig
    """

    def __init__(
        self,
        steam_path=os.environ.get("HOME") + "/.local/share/Steam",
        griddb_key='',
        destination=os.path.abspath(os.getcwd()),
        mode=CLONE_BALANCED,
        discard_repeats=True,
        excep=[],
        log_level=WARNING
    ) -> None:
        """Constructor

        Args:
            steam_path (str, optional): Path to Steam directory. Defaults to os.environ.get("HOME")+"/.local/share/Steam".
            excep (list, optional): List of exceptions to search on compatdata. Defaults to [].
            griddb_key (str, optional): key of SteamGridDB API to download images. Defaults to ''.
        """
        self.steam_path = steam_path
        
        self.griddb_key = griddb_key
        self.destination = destination
        self.mode = mode
        self.discard_repeats = discard_repeats
        self.excep = list(excep)
        self.log_level=log_level

    def save_config(self,fichero_config=os.environ.get("HOME") + "/.config/rascally.conf") -> bool:
        logger.debug("[RascallyConfig]Enter in saving config in file " + fichero_config)
        try:
            with open(fichero_config, 'w') as file:
                f = self.__dict__
                file.write(json.dumps(self.__dict__, indent=2))
        except:
            logger.error("[RascallyConfig]Cannot save the config in " + fichero_config)
            return False
        logger.info("[RascallyConfig]File saved in " + fichero_config)
        return True
    
    @staticmethod
    def load_config(fichero_config=os.environ.get("HOME") + "/.config/rascally.conf") -> 'RascallyConfig':
        logger.debug("[RascallyConfig]Enter in \"loading the config\" from file " + fichero_config)
        try:
            # La configuración existe
            with open(fichero_config, 'r') as file:
                c_file = json.load(file)
                config = RascallyConfig()
                for c in c_file:
                    if c == 'steam_path':
                        config.steam_path = c_file[c]
                    elif c == 'griddb_key':
                        config.griddb_key = c_file[c]
                    elif c == 'destination':
                        config.destination = c_file[c]
                    elif c == 'mode':
                        config.mode = c_file[c]
                    elif c == 'discard_repeats':
                        config.discard_repeats = c_file[c]
                    elif c == 'excep':
                        config.excep = c_file[c]
                    elif c == 'log_level':
                        config.log_level = c_file[c]
                logger.info("[RascallyConfig]Loading configuration correctly " + fichero_config)
                return config
        except:
            # No existe configuración, devolvemos una nueva
            logger.warning("[RascallyConfig]Load default configuration. The config file is missing or has errors.")
            return RascallyConfig()
