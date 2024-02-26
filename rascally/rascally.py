import os
import glob
import shutil
from datetime import datetime
from typing import Tuple,List

# Importaciones util
import util

util.logger.debug("Begin of import modules section")

util.logger.debug("Import module config")
from . import RascallyConfig
util.logger.debug("Import module gridder")
from util import GridManager,Grid
util.logger.debug("Import module Engines")
from .engines import LauncherEngine, BasicGame
from . import engines
util.logger.debug("Import module Steam utils")
from .steam_core import add_steam_game, get_all_games, discard_installed_games
util.logger.debug("Import module SteamGame")
from .steam_core import SteamGame

util.logger.debug("End of import modules section")

class RascalException(Exception):
    def __init__(self, msg="An error has occurred on Rascally"):
        self.msg = msg
        util.logger.fatal(f"[RASCALLY]FATAL ERROR => {msg}")
        super().__init__(self.msg)

class Rascally():
    def __init__(
        self,
        config_path=os.environ.get("HOME") + "/.config/rascally.conf"
    ) -> None:
        self.config_path=config_path
        self.config=self.load_config()
        if not os.path.exists(self.config.steam_path):
            util.logger.critical("[RASCALLY]Steam is not installed or the path is not correct")
            raise(RascalException("Steam is not installed or the path is not correct"))
        util.logger.setLevel(self.config.log_level)
        self.gridmanager=self.load_gridmanager()
        self.cache_dir=os.environ.get("HOME") + "/.cache/rascal"
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        self.cacher=util.Cacher(f'{self.cache_dir}/rascally.cache')
        self.grid_path=self.__path_grid_user()
        
#! Funciones de configuración
    def load_config(self) -> RascallyConfig:
        util.logger.debug("[RASCALLY]Loading Rascal Configuration from " + self.config_path)
        config=RascallyConfig.load_config(self.config_path)
        util.logger.info("[RASCALLY]Loading Rascal Configuration from " + self.config_path + " done.")
        return config
    
    def save_config(self) -> bool:
        util.logger.debug("[RASCALLY]Saving Rascal Configuration to " + self.config_path)
        save=self.config.save_config(self.config_path)
        if save:
            util.logger.info("[RASCALLY]Saving Rascal Configuration to " + self.config_path + " done.")
        else:
            util.logger.error("[RASCALLY]Saving Rascal Configuration to " + self.config_path + " on error...")
        return save

#! Funciones de Engines
    def get_engines(self) -> Tuple[LauncherEngine]:
        util.logger.debug("[RASCALLY]Getting all Engines to search games")
        return (
            engines.EngineEpic(),
            engines.EngineUbisoft(),
            engines.EngineLink()
        )
    
    def get_games(self, engine:LauncherEngine, discard=True) -> Tuple[BasicGame]:
        util.logger.debug(f'[RASCALLY]Getting all games from {engine.name}')
        games = engine.search_games(search_path=self.config.steam_path, excep=self.config.excep)
        if discard:
            util.logger.info(f'[RASCALLY]Got all games from {engine.name} and discarted some')
            return discard_installed_games(games, self.get_nonsteam_games())
        else:
            util.logger.info(f'[RASCALLY]Got all games from {engine.name} all without discarted')
            return games
    
    def run_adding_game(self, engine:LauncherEngine, game: BasicGame, mode:int) -> int:
        util.logger.info(f'[RASCALLY]***Entering to add to Steam the game: {engine.name}')
        util.logger.debug(f'[RASCALLY]Creating the MS link with {engine.name}')
        lnk = engine.create_link(game=game,destination=self.config.destination)
        if lnk:
            util.logger.info(f'[RASCALLY]Created the MS link for {game.AppName} from {engine.name}')
            id = add_steam_game(lnk)
            if not id:
                util.logger.warning(f'[RASCALLY]NOT added to Steam the game {game.AppName} from {engine.name}')
                return 0
            else:
                # en id el ID del nuevo juego de Steam
                dest = f'{self.config.steam_path}/steamapps/compatdata/{str(id)}'
                util.logger.info(f'[RASCALLY]Added the game to Steam {game.AppName} from {engine.name} with ID {id}')
                # TODO aquí poner el modo sacado de la configuración
                result = engine.clone_compatdata(
                    game=game,
                    destination=dest,
                    mode=mode
                )
                if result:
                    util.logger.info(f'[RASCALLY]Compatdata clonned for the game {game.AppName} and ID {id}')
                    return id
                else:
                    util.logger.error(f'[RASCALLY]Compatdata NOT clonned for the game {game.AppName} and ID {id}')
                    return 0
        return 0

        
#! Funciones de GridManager        
    def load_gridmanager(self) -> GridManager:
        util.logger.info("[RASCALLY]Loading Rascal gridmanager")
        gridmanager=GridManager(self.config.griddb_key)
        util.logger.debug("[RASCALLY]Loading Rascal gridmanager done.")
        return gridmanager
    
    def get_all_grids(self,juegos:Tuple[BasicGame]) -> bool:
        util.logger.debug("[RASCALLY]Getting all grids for a list of games.")
        for j in juegos:
            grid=self.cacher.get('grid',j.get_id())
            if grid == None:
                grid = self.gridmanager.get_all_images(j.AppName)
                if grid.id != 0:
                    self.cacher.add('grid',j.get_id(),grid.to_dict())
        return self.cacher.save_cache()
    
    def get_grid(self, game:BasicGame) -> bool:
        util.logger.debug("[RASCALLY]Getting the grids for a game.")
        grid=self.cacher.get('grid',game.get_id())
        if grid == None:
            grid = self.gridmanager.get_all_images(game.AppName)
            if grid.id != 0:
                self.cacher.add('grid',game.get_id(),grid.to_dict())
        return self.cacher.save_cache()
        
    def download_thumbnails(self, game: BasicGame) -> None:
        util.logger.debug(f"[RASCALLY]Downloading thumbnails grid for {game.AppName}.")
        grid = self.cacher.get('grid',game.get_id())
        if grid:
            grid = Grid.from_dict(grid)
            GridManager.download_thumbnails(grid,self.cache_dir,game.AppName)
    
    def download_images(self, game: BasicGame, id: int) -> None:
        util.logger.debug(f"[RASCALLY]Downloading big images grid for {game.AppName}.")
        grid = self.cacher.get('grid',game.get_id())
        if grid and self.grid_path:
            grid = Grid.from_dict(grid)
            GridManager.download_images(grid,self.grid_path,str(id))

#! Funciones sobre excepciones de ´compatData
    def add_exception(self, s: str) -> None:
        util.logger.debug(f'[RASCALLY]Adding CompatData exception ({self.config.steam_path})')
        if s not in self.config.excep:
            self.config.excep.append(s)
            util.logger.info(f'[RASCALLY]Added CompatData exception ({self.config.steam_path})')
    
    def del_exception(self, s: str) -> None:
        util.logger.debug(f'[RASCALLY]Removing CompatData exception ({self.config.steam_path})')
        if s in self.config.excep:
            self.config.excep.remove(s)
            util.logger.info(f'[RASCALLY]Removed CompatData exception ({self.config.steam_path})')

#! Funciones Avanzadas        
    def __path_grid_user(self) -> str:
        path = self.config.steam_path + "/userdata/"
        
        # Obtener la lista de carpetas en la ruta
        carpetas = [nombre for nombre in os.listdir(
            path) if os.path.isdir(os.path.join(path, nombre))]
        
        if len(carpetas) == 2:
            for c in carpetas:
                if c != '0':
                    return path + c + '/config/grid/'
        return None
    
    def get_nonsteam_games(self) -> Tuple[SteamGame]:
        util.logger.debug("[RASCALLY]Getting all games of all users.")
        return get_all_games(self.config.steam_path)
