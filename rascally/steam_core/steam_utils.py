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
import urllib.parse
import subprocess
from typing import Tuple
import time

import util
from . import SteamGame, SteamShortcuts

def add_steam_game(game_exe_path: str) -> bool:
    all_games = get_all_games()
    
    """if exe_in_games(all_games, game_exe_path):
        return 0"""
    
    mimeapps_list_path = os.path.expanduser("~/.config/mimeapps.list")

    # Check if "x-scheme-handler/steam=" exists in mimeapps.list
    with open(mimeapps_list_path, "r") as file:
        mimeapps_content = file.read()

    if "x-scheme-handler/steam=" not in mimeapps_content.lower():
        with open(mimeapps_list_path, "a") as file:
            file.write("x-scheme-handler/steam=steam.desktop;\n")

    # Construct the steam URL with the encoded game name
    encoded_url = "steam://addnonsteamgame/{}".format(
        urllib.parse.quote(game_exe_path, safe=''))

    # Create a temporary file
    if not os.path.exists('/tmp/addnonsteamgamefile'):
        with open('/tmp/addnonsteamgamefile', 'w'):
            pass

    # Open the URL using xdg-open
    resultado = subprocess.run("xdg-open " + encoded_url, shell=True)
    # Wait 5 seconds
    time.sleep(5)
    all_games2 = get_all_games()
    if len(all_games) != len(all_games2):
        for i in range(len(all_games2)-1):
            id1 = all_games[i].get_appid_human()
            id2 = all_games2[i].get_appid_human()
            if id1 != id2:
                return id2
        return all_games2[-1].get_appid_human()
    return 0

def get_all_games(search_path=os.environ.get("HOME") + "/.local/share/Steam") -> Tuple[SteamGame]:

    # Establecemos la ruta donde están los compatdata
    path = search_path + "/userdata/"

    # Obtener la lista de carpetas en la ruta
    carpetas = [nombre for nombre in os.listdir(
        path) if os.path.isdir(os.path.join(path, nombre))]

    # A las carpetas le quitamos las excepciones
    carpetas = [item for item in carpetas if item != '0']
    juegos = []

    # Iterar sobre cada carpeta y realizar la acción deseada
    for carpeta in carpetas:
        path_shortcut = os.path.join(
            path, carpeta + "/config/shortcuts.vdf")
        if os.path.isfile(path_shortcut):
            SS = SteamShortcuts(path_shortcut)
            juegos += SS.get_games()

    return tuple(juegos)

def exe_in_games(games: Tuple[SteamGame], exe: str) -> bool:
    for g in games:
        if g.Exe == exe or g.Exe == f'"{exe}"':
            return True
    return False

def discard_installed_games(games: Tuple[SteamGame], jueguecitos: Tuple[SteamGame]) -> Tuple[SteamGame]:
    util.logger.debug("[RASCAL]Discarding the installed games from a list.")
    juegos = list(games)
    for i in games[:]:
        for j in jueguecitos:
            if i.Exe == j.Exe:
                juegos.remove(i)
            elif j.Exe.find(f'{i.AppName}.lnk') != -1: 
                juegos.remove(i)
    util.logger.info(
        "[RASCAL]Discarding the installed games from a list done.")
    return tuple(juegos)

def open_game_properties(id: int) -> None:
    util.logger.debug(f'[RASCAL]Opening game properties of {id}.)')
    subprocess.run("xdg-open steam://gameproperties/" + str(id), shell=True)