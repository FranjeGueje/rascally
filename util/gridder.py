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

from steamgrid import SteamGridDB
from typing import Tuple
import concurrent.futures
import os

from util.downloader import logger, download


class Grid():
    """ Class to instance a Grid
    """

    def __init__(
        self,
        id=0,
        icon=None,
        logo=None,
        hero=None,
        gridV=None,
        gridH=None,
        icon_t=None,
        logo_t=None,
        hero_t=None,
        gridV_t=None,
        gridH_t=None
    ) -> None:

        self.id = id
        self.icon = icon
        self.logo = logo
        self.hero = hero
        self.gridV = gridV
        self.gridH = gridH
        self.icon_t = icon_t
        self.logo_t = logo_t
        self.hero_t = hero_t
        self.gridV_t = gridV_t
        self.gridH_t = gridH_t
    
    def to_dict(self) -> dict:
        logger.debug(f'[GRID]Serialize a Grid to dict')
        return {
            'id': self.id,
            'icon': self.icon,
            'logo': self.logo,
            'hero': self.hero,
            'gridV': self.gridV,
            'gridH': self.gridH,
            'icon_t': self.icon_t,
            'logo_t': self.logo_t,
            'hero_t': self.hero_t,
            'gridV_t': self.gridV_t,
            'gridH_t': self.gridH_t,
        }
    
    @staticmethod
    def from_dict(item: dict) -> 'Grid':
        logger.debug(f'[GRID]Recover a Grid from a dict')
        try:
            return Grid(
                id=item['id'],
                icon=item['icon'],
                logo=item['logo'],
                hero=item['hero'],
                gridV=item['gridV'],
                gridH=item['gridH'],
                icon_t=item['icon_t'],
                logo_t=item['logo_t'],
                hero_t=item['hero_t'],
                gridV_t=item['gridV_t'],
                gridH_t=item['gridH_t']
            )
        except:
            logger.error(f'[GRID]Cannot recover a Grid from a dict')
            return Grid()


class GridManager():
    """ Class to instance a GridManager

    """

    def __init__(self, auth_key: str) -> None:
        self.sgdb = SteamGridDB(auth_key)


    def __get_image(self, name: str, img_type: callable, lista=None, MAX_TITLES=0) -> Tuple[str, str]:
        logger.debug(f'[GRIDMANAGER]Download information from {name} on {img_type}')
        nombres = lista if lista != None else self.sgdb.search_game(name)
        for r in nombres[:MAX_TITLES+1]:
            img = img_type([r.id])
            if img != None:
                return img[0].url, img[0].thumbnail
        return None, None

    def __get_grid(self, name: str, vertical: bool, lista=None, MAX_TITLES=0,MAX_GRID=5) -> Tuple[str, str]:
        logger.debug(f'[GRIDMANAGER]Download Grid information from {name} in vertical={vertical} position')
        nombres = lista if lista != None else self.sgdb.search_game(name)
        for r in nombres[:MAX_TITLES+1]:
            img = self.sgdb.get_grids_by_gameid([r.id])
            if img != None:
                for l in img[:MAX_GRID+1]:
                    if l.height > l.width and vertical:
                        return l.url, l.thumbnail
                    elif l.height < l.width and not vertical:
                        return l.url, l.thumbnail
        return None, None

    def get_hero(self, name: str, lista=None,MAX_TITLES=0) -> Tuple[str, str]:
        logger.debug(f'[GRIDMANAGER]Download hero information from {name}')
        try:
            return self.__get_image(name, self.sgdb.get_heroes_by_gameid, lista, MAX_TITLES)
        except:
            logger.warning("[GridManager]Not possible get the hero image.")
            return None, None

    def get_logo(self, name: str, lista=None,MAX_TITLES=0) -> Tuple[str, str]:
        logger.debug(f'[GRIDMANAGER]Download logo information from {name}')
        try:
            return self.__get_image(name, self.sgdb.get_logos_by_gameid, lista, MAX_TITLES)
        except:
            logger.warning("[GridManager]Not possible get the logo image.")
            return None, None

    def get_icon(self, name: str, lista=None,MAX_TITLES=0) -> Tuple[str, str]:
        logger.debug(f'[GRIDMANAGER]Download icon information from {name}')
        try:
            return self.__get_image(name, self.sgdb.get_icons_by_gameid, lista, MAX_TITLES)
        except:
            logger.warning("[GridManager]Not possible get the icon image.")
            return None, None

    def get_gridV(self, name: str, lista=None,MAX_TITLES=0,MAX_GRID=5) -> Tuple[str, str]:
        logger.debug(f'[GRIDMANAGER]Download gridV information from {name}')
        try:
            return self.__get_grid(name, True, lista,MAX_TITLES,MAX_GRID)
        except:
            logger.warning("[GridManager]Not possible get the gridVertical image.")
            return None, None

    def get_gridH(self, name: str, lista=None,MAX_TITLES=0,MAX_GRID=5) -> Tuple[str, str]:
        logger.debug(f'[GRIDMANAGER]Download gridH information from {name}')
        try:
            return self.__get_grid(name, False, lista,MAX_TITLES,MAX_GRID)
        except:
            logger.warning("[GridManager]Not possible get the hero image.")
            return None, None

    def get_all_images(self, name: str,MAX_TITLES=0,MAX_GRID=3) -> Grid:
        logger.debug(f'[GRIDMANAGER]Download all information about {name}')
        try:
            nombres = self.sgdb.search_game(name)
            id = nombres[0].id
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Enviar la función al ThreadPoolExecutor y obtener un objeto Future
                h1 = executor.submit(self.get_gridH, name, nombres,MAX_TITLES,MAX_GRID)
                h2 = executor.submit(self.get_gridV, name, nombres,MAX_TITLES,MAX_GRID)
                h3 = executor.submit(self.get_logo, name, nombres,MAX_TITLES)
                h4 = executor.submit(self.get_icon, name, nombres,MAX_TITLES)
                h5 = executor.submit(self.get_hero, name, nombres,MAX_TITLES)

                # Obtener el resultado cuando esté listo
                gridH, gridH_t = h1.result()
                gridV, gridV_t = h2.result()
                logo, logo_t = h3.result()
                icon, icon_t = h4.result()
                hero, hero_t = h5.result()
            
            logger.info("[GridManager]Localizated all images.")
            return Grid(
                icon=icon, logo=logo, hero=hero, gridH=gridH, gridV=gridV,
                icon_t=icon_t, logo_t=logo_t, hero_t=hero_t, gridH_t=gridH_t,
                gridV_t=gridV_t, id=id)
                
        except:
            logger.warning("[GridManager]Not possible search all images.")
            return Grid()
    
    @staticmethod
    def download_thumbnails(grid: Grid, path:str, name='') -> None:
        logger.debug(f'[GRIDMANAGER]Download all thumbnails about {name}')
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Enviar la función al ThreadPoolExecutor y obtener un objeto Future
                if grid.gridV_t:
                    name_file,ext = os.path.splitext(grid.gridV_t)
                    h2 = executor.submit(download,grid.gridV_t,f'{path}/{name}{ext}')
            logger.debug("[GridManager]Download all thumbnail images.")
                
        except:
            logger.warning("[GridManager]Not possible downloads all thumbnail.")
        
    @staticmethod
    def download_images(grid: Grid, path:str, name:str) -> None:
        logger.debug(f'[GRIDMANAGER]Download all big images about {name}')
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Enviar la función al ThreadPoolExecutor y obtener un objeto Future
                if grid.gridV:
                    name_file,ext = os.path.splitext(grid.gridV)
                    h2 = executor.submit(download,grid.gridV,f'{path}/{name}p{ext}')
                if grid.gridH:
                    name_file,ext = os.path.splitext(grid.gridH)
                    h1 = executor.submit(download,grid.gridH,f'{path}/{name}{ext}')
                if grid.hero:
                    name_file,ext = os.path.splitext(grid.hero)
                    h3 = executor.submit(download,grid.hero,f'{path}/{name}_hero{ext}')
                if grid.icon:
                    name_file,ext = os.path.splitext(grid.icon)
                    h4 = executor.submit(download,grid.icon,f'{path}/{name}_icon{ext}')
                if grid.logo:
                    name_file,ext = os.path.splitext(grid.logo)
                    h5 = executor.submit(download,grid.logo,f'{path}/{name}_logo{ext}')
            
            logger.debug("[GridManager]Download all big images.")
                
        except:
            logger.warning("[GridManager]Not possible downloads all big images.")
