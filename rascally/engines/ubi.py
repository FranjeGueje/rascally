import os
from typing import Tuple

from . import LauncherEngine
from . import BasicGame
from util import logger

class EngineUbisoft(LauncherEngine):
    
    def __init__(self):
        super().__init__('Ubisoft')
        
        #! Añandimos los directorios, ficheros, y enlaces EXTRAS
        self.copy_list = self.copy_list + \
            ('pfx/drive_c/users/steamuser/AppData/Local/Ubisoft Game Launcher',)
        
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
            ruta_ubi = os.path.join(
                path, carpeta + "/pfx/drive_c/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/UbisoftConnect.exe")
            path_exclude = os.path.join(path, carpeta + "/rascal_exclude")
            if os.path.isfile(ruta_ubi) and not os.path.isfile(path_exclude):
                prefix = path + carpeta
                
                logger.info(f'[EngineUbisoft]Found this prefix {prefix} with Ubisoft installed')

                with open(os.path.join(path, carpeta + "/pfx/system.reg"), 'r') as reg_file:
                    lines = reg_file.read()
                
                juegos_bruto = lines.split('[Software\\\\Wow6432Node\\\\Ubisoft\\\\Launcher\\\\Installs\\\\')
                
                for i in range(1, len(juegos_bruto)):
                    exe = juegos_bruto[i].split(']')[0]
                    exe_completed = "\"uplay://launch/" + exe + "/0\""
                    install_dir = juegos_bruto[i].split("\"")[3]
                    title = os.path.basename(install_dir[1:-1])
                    logger.info(f'[EngineUbisoft]Found the game {title} with Exe {exe_completed}')
                    g = BasicGame(
                        AppName=title,
                        Exe=exe_completed,
                        CompatData=prefix
                    )
                    juegos.append(g)
        logger.info(f'[EngineUbisoft]Found {len(juegos)} games')
        return tuple(juegos)
