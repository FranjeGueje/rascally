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

import vdf
from typing import Tuple

from . import SteamGame
from util import logger


class SteamShortcuts():
    """ Class to instance a Steam Shortcuts file
    """
    def __init__(self, path_vdf:str):
        self.path_vdf=path_vdf
        self.data=SteamShortcuts.load_shortcuts(self.path_vdf)
        
    
    @staticmethod
    def load_shortcuts(file_path: str) -> dict:
        logger.debug(f'[SteamShortcuts]Loading Steam shortcuts from {file_path}')
        try:
            with open(file_path, 'rb') as file:
                data = vdf.binary_load(file)
        except FileNotFoundError:
            logger.error("[SteamShortcuts.load_shortcuts]:The file is missing, not found: " + file_path)
            data = None
        except vdf.VDFError as e:
            logger.error("[SteamShortcuts.load_shortcuts]VDFError: The format of " + file_path + " is incorrect")
            data = None
        return data
    
    @staticmethod
    def save_games(file_path: str, games: Tuple[SteamGame]) -> bool:
        logger.debug(f'[SteamShortcuts]Saving list of Steam games to {file_path}')
        data = {'shortcuts':{}}
        for i in range(len(games)):
            if games[i]:
                data['shortcuts'][str(i)] = games[i].get_SteamGame()
        try:
            with open(file_path, 'wb') as file:
                vdf_binary = vdf.binary_dumps(data)
                file.write(vdf_binary)
                logger.info("[SteamShortcuts.save_games]The file named " + file_path + "is saved correctly.")
                return True
        except vdf.VDFError as e:
            logger.error("[SteamShortcuts.save_games]VDFError: The format of " + file_path + " is incorrect")
            return False
    
    def get_game(self,id:int) -> SteamGame:
        games = self.get_games()
        for g in games:
            if id == g.get_appid_human():
                return g
        return None
        
    def get_games(self) -> Tuple[SteamGame]:
        logger.debug(f'[SteamShortcuts]Getting all games from this shortcuts.')
        games = []
        for k, v in self.data['shortcuts'].items():
            games.append(SteamGame.dict_to_game(v))
        return tuple(games)
    
    def save_shortcuts(self, file_path: str) -> bool:
        logger.debug(f'[SteamShortcuts]Saving Steam shortcuts to {file_path}')
        try:
            with open(file_path, 'wb') as file:
                vdf_binary = vdf.binary_dumps(self.data)
                file.write(vdf_binary)
                logger.info("[SteamShortcuts.save_shortcuts]The file named " + file_path + "is saved correctly.")
                return True
        except vdf.VDFError as e:
            logger.error("[SteamShortcuts.save_shortcuts]VDFError: The format of " + file_path + " is incorrect")
            return False
    
    def add_game_to_shortcut(self, game: SteamGame)-> bool:
        logger.debug(f'[SteamShortcuts]Adding {game.AppName} to shortcut')
        try:
            pos = len(self.data['shortcuts'])
            self.data['shortcuts'][str(pos)] = game.get_SteamGame()
            return True
        except:
            return False
    
    def modify_game(self, game: SteamGame)-> bool:
        logger.debug(f'[SteamShortcuts]Modifing {game.AppName} in shortcuts')
        try:
            game_list = self.data['shortcuts']
            for key, game_data in game_list.items():
                if game_data.get('appid') == game.appid:
                    game_data['AppName'] = game.AppName
                    game_data['Exe'] = game.Exe
                    game_data['StartDir'] = game.StartDir
                    game_data['icon'] = game.icon
                    game_data['ShortcutPath'] = game.ShortcutPath
                    game_data['LaunchOptions'] = game.LaunchOptions
                    game_data['IsHidden'] = game.IsHidden
                    game_data['AllowDesktopConfig'] = game.AllowDesktopConfig
                    game_data['AllowOverlay'] = game.AllowOverlay
                    game_data['OpenVR'] = game.OpenVR
                    game_data['Devkit'] = game.Devkit
                    game_data['DevkitGameID'] = game.DevkitGameID
                    game_data['DevkitOverrideAppID'] = game.DevkitOverrideAppID
                    game_data['LastPlayTime'] = game.LastPlayTime
                    game_data['FlatpakAppID'] = game.FlatpakAppID
                    game_data['tags'] = game.tags
                    return True
            return False
        except:
            return False
        
    def remove(self, appid: int)-> bool:
        logger.debug(f'[SteamShortcuts]Removing {appid} game from shortcut')
        try:
            pos = len(self.data['shortcuts'])
            for i in range(pos):
                if self.data['shortcuts'][str(i)]['appid'] == appid :
                    for j in range(i,pos -1):
                        self.data['shortcuts'][str(j)] = self.data['shortcuts'][str(j+1)]
                    del(self.data['shortcuts'][str(pos-1)])
                    return True
        except:
            return False


    def modify_game_name(self, original_name:str, new_name:str) -> bool:
        logger.debug(f'[SteamShortcuts]Modifing a name of game from {original_name} to {new_name}')
        try:
            game_list = self.data['shortcuts']
            for key, game_data in game_list.items():
                if game_data.get('AppName') == original_name:
                    game_data['AppName'] = new_name
                    logger.info("[SteamShortcuts.modify_game_name] Change name the game from {} to {}", original_name, new_name)
                    return True
            logger.warning("[SteamShortcuts.modify_game_name] The game with name {}, not found", original_name)
            return False
        except:
            logger.error("[modify_game_name]VDFError: The format of file is incorrect")
            return False
    
    def find_game(self, exe:str) -> bool:
        logger.debug(f'[SteamShortcuts]Finding a game with exe {exe}')
        try:
            game_list = self.data['shortcuts']
            for key, game_data in game_list.items():
                if game_data.get('Exe') == exe:
                    logger.info(f'[SteamShortcuts.find_game] Exe {exe} found')
                    return True
            logger.warning(f'[SteamShortcuts.find_game] The game with exe {exe}, not found')
            return False
        except:
            logger.error("[SteamShortcuts.find_game]VDFError: The format of file is incorrect")
            return False
    